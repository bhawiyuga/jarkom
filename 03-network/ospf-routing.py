#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller, Docker, Host
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import docker
from mininet.log import info, error, warn, debug
setLogLevel('info')

class PrivilegedDocker( Docker ):

	def __init__(self, name, dimage=None, dcmd=None, build_params={},
				 **kwargs):
		self.dimage = dimage
		self.dnameprefix = "mn"
		self.dcmd = dcmd if dcmd is not None else "/bin/bash"
		self.dc = None  # pointer to the dict containing 'Id' and 'Warnings' keys of the container
		self.dcinfo = None
		self.did = None # Id of running container
		#  let's store our resource limits to have them available through the
		#  Mininet API later on
		defaults = { 'cpu_quota': -1,
					 'cpu_period': None,
					 'cpu_shares': None,
					 'cpuset_cpus': None,
					 'mem_limit': None,
					 'memswap_limit': None,
					 'environment': {},
					 'volumes': [],  # use ["/home/user1/:/mnt/vol2:rw"]
					 'tmpfs': [], # use ["/home/vol1/:size=3G,uid=1000"]
					 'network_mode': None,
					 'publish_all_ports': True,
					 'port_bindings': {},
					 'ports': [],
					 'dns': [],
					 'ipc_mode': None,
					 'devices': [],
					 'cap_add': ['net_admin'],  # we need this to allow mininet network setup
					 'storage_opt': None,
					 'sysctls': {}
					 }
		defaults.update( kwargs )

		if 'net_admin' not in defaults['cap_add']:
			defaults['cap_add'] += ['net_admin']  # adding net_admin if it's cleared out to allow mininet network setup

		# keep resource in a dict for easy update during container lifetime
		self.resources = dict(
			cpu_quota=defaults['cpu_quota'],
			cpu_period=defaults['cpu_period'],
			cpu_shares=defaults['cpu_shares'],
			cpuset_cpus=defaults['cpuset_cpus'],
			mem_limit=defaults['mem_limit'],
			memswap_limit=defaults['memswap_limit']
		)

		self.volumes = defaults['volumes']
		self.tmpfs = defaults['tmpfs']
		self.environment = {} if defaults['environment'] is None else defaults['environment']
		# setting PS1 at "docker run" may break the python docker api (update_container hangs...)
		# self.environment.update({"PS1": chr(127)})  # CLI support
		self.network_mode = defaults['network_mode']
		self.publish_all_ports = defaults['publish_all_ports']
		self.port_bindings = defaults['port_bindings']
		self.dns = defaults['dns']
		self.ipc_mode = defaults['ipc_mode']
		self.devices = defaults['devices']
		self.cap_add = defaults['cap_add']
		self.sysctls = defaults['sysctls']
		self.storage_opt = defaults['storage_opt']

		# setup docker client
		# self.dcli = docker.APIClient(base_url='unix://var/run/docker.sock')
		self.d_client = docker.from_env()
		self.dcli = self.d_client.api

		_id = None
		if build_params.get("path", None):
			if not build_params.get("tag", None):
				if dimage:
					build_params["tag"] = dimage
			_id, output = self.build(**build_params)
			dimage = _id
			self.dimage = _id
			info("Docker image built: id: {},  {}. Output:\n".format(
				_id, build_params.get("tag", None)))
			info(output)

		# pull image if it does not exist
		self._check_image_exists(dimage, True, _id=None)

		# for DEBUG
		debug("Created docker container object %s\n" % name)
		debug("image: %s\n" % str(self.dimage))
		debug("dcmd: %s\n" % str(self.dcmd))
		info("%s: kwargs %s\n" % (name, str(kwargs)))

		# creats host config for container
		# see: https://docker-py.readthedocs.io/en/stable/api.html#docker.api.container.ContainerApiMixin.create_host_config
		hc = self.dcli.create_host_config(
			network_mode=self.network_mode,
			privileged=True,  # no longer need privileged, using net_admin capability instead
			binds=self.volumes,
			tmpfs=self.tmpfs,
			publish_all_ports=self.publish_all_ports,
			port_bindings=self.port_bindings,
			mem_limit=self.resources.get('mem_limit'),
			cpuset_cpus=self.resources.get('cpuset_cpus'),
			dns=self.dns,
			ipc_mode=self.ipc_mode,  # string
			devices=self.devices,  # see docker-py docu
			cap_add=self.cap_add,  # see docker-py docu
			sysctls=self.sysctls,   # see docker-py docu
			storage_opt=self.storage_opt,
			# Assuming Docker uses the cgroupfs driver, we set the parent to safely
			# access cgroups when modifying resource limits.
			cgroup_parent='/docker'
		)

		if kwargs.get("rm", False):
			container_list = self.dcli.containers(all=True)
			for container in container_list:
				for container_name in container.get("Names", []):
					if "%s.%s" % (self.dnameprefix, name) in container_name:
						self.dcli.remove_container(container="%s.%s" % (self.dnameprefix, name), force=True)
						break

		# create new docker container
		self.dc = self.dcli.create_container(
			name="%s.%s" % (self.dnameprefix, name),
			image=self.dimage,
			command=self.dcmd,
			entrypoint=list(),  # overwrite (will be executed manually at the end)
			stdin_open=True,  # keep container open
			tty=True,  # allocate pseudo tty
			environment=self.environment,
			#network_disabled=True,  # docker stats breaks if we disable the default network
			host_config=hc,
			ports=defaults['ports'],
			labels=['com.containernet'],
			volumes=[self._get_volume_mount_name(v) for v in self.volumes if self._get_volume_mount_name(v) is not None],
			hostname=name
		)

		# start the container
		self.dcli.start(self.dc)
		debug("Docker container %s started\n" % name)

		# fetch information about new container
		self.dcinfo = self.dcli.inspect_container(self.dc)
		self.did = self.dcinfo.get("Id")

		# call original Node.__init__
		Host.__init__(self, name, **kwargs)

		# let's initially set our resource limits
		self.update_resources(**self.resources)

		self.master = None
		self.slave = None

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.4/24', dimage="containernet:bionic")
d2 = net.addDocker('d2', ip='10.0.1.5/24', dimage="containernet:bionic")
d3 = net.addDocker('d3', ip='10.0.1.6/24', dimage="containernet:bionic")
info('*** Adding router\n')
#r1 = net.addDocker('r1', cls=LinuxRouter, ip=None, dimage="containernet:bionic")
r1 = net.addDocker('r1', ip=None, cls=PrivilegedDocker, dimage="bhawiyuga/frr-debian:latest", dcmd='/usr/lib/frr/docker-start')
info('*** Adding switches\n')
s1 = net.addSwitch('s1')
s2 = net.addSwitch('s2')
info('*** Creating links\n')
'''
net.addLink(d1, s1)
net.addLink(s1, s2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s2, d2)
'''
net.addLink(d1, s1)
net.addLink(d2, s2)
net.addLink(d3, s2)
net.addLink(r1,s1,params1={ 'ip' : '10.0.0.1/24' })
net.addLink(r1,s2,params1={ 'ip' : '10.0.1.1/24' })

info('*** Starting network\n')
net.start()
info('*** Config static routing\n')
#net["r1"].cmd("route add -net 10.0.0.0/24 gw 10.0.0.1 r1-eth0")
#net["r1"].cmd("route add -net 10.0.1.0/24 gw 10.0.1.1 r1-eth1")

info('*** Config gateway on host\n')
#net["d1"].cmd("ip route add 10.0.1.0/24 via 10.0.0.1")
#net["d2"].cmd("ip route add 10.0.0.0/24 via 10.0.1.1")
net["d1"].cmd("ip route change default via 10.0.0.1 dev d1-eth0")
net["d2"].cmd("ip route change default via 10.0.1.1 dev d2-eth0")

info('*** Testing connectivity\n')
#net.ping([d1, d2])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()