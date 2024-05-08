import os
import time
import configparser
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Intf

# Load configuration settings
config = configparser.ConfigParser()
config.read('/home/mininet/Captive-Portal/config.ini')

# These are placeholder values that students need to replace with actual data from config.ini
DNS_Server = config['DEFAULT']['DNS_Server']
internet_ip = config['DEFAULT']['internet_ip']
internet_mac = config['DEFAULT']['internet_mac']
captive_portal_ip = config['DEFAULT']['captive_portal_ip']
captive_portal_mac = config['DEFAULT']['captive_portal_mac']

bash_script = '''
# Bash script content goes here. Students should create this script based on requirements.
'''

bash_script_name = 'gateway_switch.sh'

def configure_network(host):
    # Disable potential conflicting services and configure DNS
    host.cmd('sudo systemctl disable --now systemd-resolved.service')
    host.cmd(f'echo "nameserver 127.0.0.53\\nnameserver {DNS_Server}" > /etc/resolv.conf')
    
    # Students should write the command to execute the bash script
    # Example: host.cmd(f'sudo ./{bash_script_name} &')

def configure_host_network(host):
    # Students should set up iptables rules for DNS and HTTP/HTTPS redirection
    pass

def customTree():
    "Create a network and add NAT to provide Internet access."
    net = Mininet(controller=RemoteController, switch=OVSSwitch)

    # Setting up the network components. Students should complete the missing details.
    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')

    info('*** Adding host\n')
    # Students should configure the host with IP and MAC from the config
    host = None  # Placeholder for student to create the host with required parameters

    info('*** Adding internet connectivity\n')
    internet = net.addNAT(name='internet')
    internet.configDefault()

    info('*** Creating links\n')
    # Students should complete the network topology by adding appropriate links

    info('*** Starting network\n')
    net.start()

    info('*** Configure NAT setting\n')
    # Students should configure the NAT's IP settings

    info('*** Start host service\n')
    # Students should write commands to start DNS and web server on the host

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    # Create a bash script to switch gateways
    with open(bash_script_name, "w") as file:
        file.write(bash_script)
    # Change file permissions, add execute permissions
    os.chmod(bash_script_name, 0o755)

    setLogLevel('info')
    customTree()
