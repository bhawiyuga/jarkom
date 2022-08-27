#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import Controller, Docker
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

class LinuxRouter( Docker ):
	"""A Node with IP forwarding enabled.
	Means that every packet that is in this node, comunicate freely with its interfaces."""

	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers\n')
d1 = net.addDocker('d1', ip='10.0.0.4/24', dimage="bhawiyuga/containernet:bionic")
d2 = net.addDocker('d2', ip='10.0.1.5/24', dimage="bhawiyuga/containernet:bionic")
d3 = net.addDocker('d3', ip='10.0.1.6/24', dimage="bhawiyuga/containernet:bionic")
info('*** Adding router\n')
r1 = net.addDocker('r1', cls=LinuxRouter, ip=None, dimage="bhawiyuga/containernet:bionic")
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