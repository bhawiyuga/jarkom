# Configure GNS3 Server

## Configure on Local VM (VirtualBox or VMWare)

Please follow this tutorial

https://docs.gns3.com/docs/getting-started/installation/download-gns3-vm

## Configure on Remote Server (Cloud/On Premise) using Ansible

1. Install Ansible in your local computer

    https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

2. Clone this repository

3. Enter **gns3-server** directory
```
cd gns3/gns3-server
```

4. Create your own **inventory.yaml** from sample file **inventory_sample.yaml** 

4. Specify the target server address, username and SSH private key path in your **inventory.yaml** file.

5. Execute server installation playbook.
```
ansible-playbook install.yaml
```

6. Once succeed, execute Docker host and router images preparation playbook.
```
ansible-playbook image.yaml
```

7. Open **GNS3 Desktop** apps on your local computer

8. Click ``Help -> Setup Wizard``

9. Choose option **Run appliances on a remote server (advanced usage)**

10. Specify remote server information
    - *Host* : address of remote GNS Server
    - *Port* : port of remote GNS Server (default 3080). Make sure your GNS server firewall allow incoming traffic to this port.
    -  Enable authentication
    - *User* : username for running GNS3 server (default : *gns3*)
    - *Password* : password of remote GNS Server user (default : *gns3*)

## Add Docker Template for Host and Router in GNS3 Desktop

1. Go to **Preferences** window

2. Click **Docker containers* in left navigation pane

3. Click **New** button. The wizard window will appear.

4. In **New Docker container template** window choose the existing image in server. For example *custom-frrouting*. Click **Next** button.

5. Specify name for your container. Click **Next** button.

6. Specify number of network adapters. For example 5 adapters. Click **Next** button.

7. Specify start command that will be executed on container execution. 
   - For **ubuntu** container use ``/bin/bash``
   - For **frrouting** container use ``/bin/sh``
   
   Click **Next** button.

8. Specify console type. For example **telnet**. Click **Next** button.

9. Click **Finish** button.

### Persistent Volume Configuration
Persistent volumes are useful to store configuration and/or output files permanently. 

1. Go to main window of GNS3 Desktop

2. On left pane navigate to **Browse all devices** to show all available appliances.

3. Right click on one of Docker based appliances that has been created. Choose **Configure template**.

4. Navigate to **Advanced** tab. In additional directories field, specify the volume directory name (one directory per line). As example, for **frrouting** we store the captured traffic on ``/data`` and router config on ``/etc/frr``.

5. The stored files can be accessed on project directory project of GNS Server VM/Cloud (through ssh/scp). The project directory location can be viewed by clicking in **Show in file manager** menu of each node.

## Sample Project

1. Simple dynamic routing with Docker and FRR

    https://www.gns3.com/community/blog/create-a-router-with-docker-and-free-range-routing

    ```
    /usr/lib/frr/watchfrr zebra eigrpd &
    vtysh
    frrouting-frr-1# conf t
    frrouting-frr-1(config)# router eigrp 10
    frrouting-frr-1(config-router)# network 192.168.0.0/24
    frrouting-frr-1(config-router)# network 10.0.0.0/30
    frrouting-frr-1(config-router)# exit
    frrouting-frr-1(config)# exit
    frrouting-frr-1# wr
    ```