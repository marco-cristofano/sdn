#!/usr/bin/python
from mininet.net import Mininet
from mininet.link import Intf
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.topolib import TreeTopo
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
# OpenDayLight controller
ODL_CONTROLLER_IP='192.168.56.101'
ODL_CONTROLLER_PORT=6633
# Define remote OpenDaylight Controller
info( 'OpenDaylight IP Addr:', ODL_CONTROLLER_IP, '\n' )
info( 'OpenDaylight Port:', ODL_CONTROLLER_PORT, '\n' )
def customNet():
    "Create a customNet and add devices to it."
    net = Mininet( topo=None, build=False, ipBase='185.0.0.0/24' )
    # Add controller
    info( 'Adding controller\n' )
    net.addController( 'c0', 
                       controller=RemoteController, 
                       ip=ODL_CONTROLLER_IP, 
                       port=ODL_CONTROLLER_PORT 
                     )
    #Add hosts 
    info( 'Adding hosts\n' )
    h1 = net.addHost( 'h1',cls=Host, ip='185.0.0.1' )
    #h2 = net.addHost( 'h2',cls=Host, ip='185.0.0.2' )
    #h3 = net.addHost( 'h3',cls=Host, ip='185.0.0.3' )
    #h4 = net.addHost( 'h4',cls=Host, ip='185.0.0.4' )
    h5 = net.addHost( 'h5',cls=Host, ip='185.0.0.65' )
    #h6 = net.addHost( 'h6',cls=Host, ip='185.0.0.66' )
    #h7 = net.addHost( 'h7',cls=Host, ip='185.0.0.67' )
    #h8 = net.addHost( 'h8',cls=Host, ip='185.0.0.68' )
    #h9 = net.addHost( 'h9',cls=Host, ip='185.0.0.129' )
    h10 = net.addHost( 'h10',cls=Host, ip='185.0.0.130' )
    #h11 = net.addHost( 'h11',cls=Host, ip='185.0.0.131' )
    #h12 = net.addHost( 'h12',cls=Host, ip='185.0.0.132' )
    h13 = net.addHost( 'h13',cls=Host, ip='185.0.0.193' )
    #h14 = net.addHost( 'h14',cls=Host, ip='185.0.0.194' )
    #h15 = net.addHost( 'h15',cls=Host, ip='185.0.0.195' )
    #h16 = net.addHost( 'h16',cls=Host, ip='185.0.0.196' )
    # Add switches
    info( 'Adding switches\n' )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )
    s4 = net.addSwitch( 's4' )
    s5 = net.addSwitch( 's5' )    
    #Add links
    info( 'Adding switch links\n' )
    net.addLink( s1, s5 )
    net.addLink( s2, s5 )
    net.addLink( s3, s5 )
    net.addLink( s4, s5 )
    info( 'Adding hosts links\n' )	
    net.addLink( h1, s1 )
    net.addLink( h5, s2 )
    net.addLink( h10, s3 )
    net.addLink( h13, s4 )
    info( '*** Starting network ***\n')
    net.start()
    info( '*** Running CLI ***\n' )
    CLI( net )
    info( '*** Stopping network ***' )
    net.stop()
if __name__ == '__main__':
    setLogLevel( 'info' )
    customNet()
