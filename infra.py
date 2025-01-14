from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
#from mininet.log import setLogLevel, info

class netType(object):
    def __init__(self, *args):
        super(netType, self).__init__(*args)

    def simple_topology():
        """Set up a Mininet topology and attach it to the Ryu controller."""
        net = Mininet(controller=RemoteController, link=TCLink)

        # Add the Ryu controller
        ryu_controller = net.addController(
            'ryuController',
            controller=RemoteController,
            ip='127.0.0.1',  # IP address of the machine running the Ryu controller
            port=6633  # Default OpenFlow port
        )

        # Add switches
        switch1 = net.addSwitch('s1')
        switch2 = net.addSwitch('s2')
        switch3 = net.addSwitch('s3')

        # Add hosts
        host1 = net.addHost('h1', ip='10.0.0.1/24')
        host2 = net.addHost('h2', ip='10.0.0.2/24')
        host3 = net.addHost('h3', ip='10.0.0.3/24')
        host4 = net.addHost('h4', ip='10.0.1.4/24')
        host5 = net.addHost('h5', ip='10.0.1.5/24')
        host6 = net.addHost('h6', ip='10.0.1.6/24')
        host7 = net.addHost('h7', ip='10.0.1.7/24')
        host8 = net.addHost('h8', ip='10.0.0.8/24')

        # Add a router to connect the two network segments
        router = net.addHost('r0')

        # Create links for the first network segment (10.0.0.0/24)
        net.addLink(host1, switch1)
        net.addLink(host2, switch1)
        net.addLink(host3, switch1)
        net.addLink(host7, switch1)

        # Create links for the second network segment (10.0.1.0/24)
        net.addLink(host4, switch2)
        net.addLink(host5, switch2)
        net.addLink(host6, switch2)
        net.addLink(host8, switch2)

        # Connect the router to both switches
        net.addLink(router, switch1, intfName1='r0-eth0', params1={'ip': '10.0.0.254/24'})
        net.addLink(router, switch2, intfName1='r0-eth1', params1={'ip': '10.0.1.254/24'})

        # Start the network
        net.start()

        # Configure routing on the router
        router.cmd('sysctl -w net.ipv4.ip_forward=1')
        router.cmd('ip route add 10.0.1.0/24 dev r0-eth1 proto kernel scope link src 10.0.1.254')
        router.cmd('ip route add 10.0.0.0/24 dev r0-eth0 proto kernel scope link src 10.0.0.254')

        # Configure default gateways for hosts in both networks
        host1.cmd('ip route add default via 10.0.0.254')
        host2.cmd('ip route add default via 10.0.0.254')
        host3.cmd('ip route add default via 10.0.0.254')
        host4.cmd('ip route add default via 10.0.1.254')
        host5.cmd('ip route add default via 10.0.1.254')
        host6.cmd('ip route add default via 10.0.1.254')


        print("Network is up. Use 'pingall' in the CLI to test connectivity.")
        
        # Test connectivity automatically
        net.pingAll()

        # Enter the Mininet CLI
        CLI(net)

        # Stop the network
        net.stop()

    def complex_topology():
        """Set up a more complex Mininet topology with multiple switches and hosts."""
        net = Mininet(controller=RemoteController, link=TCLink)

        # Add the Ryu controller
        ryu_controller = net.addController(
            'ryuController',
            controller=RemoteController,
            ip='127.0.0.1',  # IP address of the machine running the Ryu controller -This configuration assumes ryu controller is running on the same machine
            port=6633  # Default OpenFlow port
        )

        # Add switches
        switch1 = net.addSwitch('s1')
        switch2 = net.addSwitch('s2')
        switch3 = net.addSwitch('s3')

        # Add hosts
        host1 = net.addHost('h1', ip='10.0.0.1/24')
        host2 = net.addHost('h2', ip='10.0.0.2/24')
        host3 = net.addHost('h3', ip='10.0.1.1/24')
        host4 = net.addHost('h4', ip='10.0.1.2/24')

        # Create links with bandwidth, delay, and loss configurations
        net.addLink(host1, switch1, bw=10, delay='5ms', loss=1)
        net.addLink(host2, switch1, bw=10, delay='5ms', loss=1)
        net.addLink(host3, switch2, bw=20, delay='10ms', loss=2)
        net.addLink(host4, switch2, bw=20, delay='10ms', loss=2)

        # Interconnect switches
        net.addLink(switch1, switch2, bw=50, delay='1ms', loss=0)
        net.addLink(switch2, switch3, bw=30, delay='3ms', loss=1)
        net.addLink(switch1, switch3, bw=40, delay='2ms', loss=0)

        # Start the network
        net.start()
        print("Network is up. Use 'pingall' in the CLI to test connectivity.")
        
        # Test connectivity automatically
        net.pingAll()

        # Enter the Mininet CLI
        CLI(net)

        # Stop the network
        net.stop()

    def tree_topology():
        """Set up a tree-based Mininet topology."""
        net = Mininet(controller=RemoteController, link=TCLink)

        # Add the Ryu controller
        ryu_controller = net.addController(
            'ryuController',
            controller=RemoteController,
            ip='127.0.0.1',  # IP address of the machine running the Ryu controller
            port=6633  # Default OpenFlow port
        )

        # Add core switch
        core_switch = net.addSwitch('s1')

        # Add aggregation layer switches
        agg_switch1 = net.addSwitch('s2')
        agg_switch2 = net.addSwitch('s3')

        # Add access layer switches
        access_switch1 = net.addSwitch('s4')
        access_switch2 = net.addSwitch('s5')
        access_switch3 = net.addSwitch('s6')
        access_switch4 = net.addSwitch('s7')

        # Interconnect core and aggregation switches
        net.addLink(core_switch, agg_switch1, bw=50, delay='2ms', use_htb=True, r2q=10)
        net.addLink(core_switch, agg_switch2, bw=50, delay='2ms', use_htb=True, r2q=10)

        # Interconnect aggregation and access switches
        net.addLink(agg_switch1, access_switch1, bw=30, delay='5ms', use_htb=True, r2q=10)
        net.addLink(agg_switch1, access_switch2, bw=30, delay='5ms', use_htb=True, r2q=10)
        net.addLink(agg_switch2, access_switch3, bw=30, delay='5ms', use_htb=True, r2q=10)
        net.addLink(agg_switch2, access_switch4, bw=30, delay='5ms', use_htb=True, r2q=10)

        # Add hosts to access layer switches
        host1 = net.addHost('h1', ip='10.0.0.1/24')
        host2 = net.addHost('h2', ip='10.0.0.2/24')
        host3 = net.addHost('h3', ip='10.0.1.1/24')
        host4 = net.addHost('h4', ip='10.0.1.2/24')
        host5 = net.addHost('h5', ip='10.0.2.1/24')
        host6 = net.addHost('h6', ip='10.0.2.2/24')
        host7 = net.addHost('h7', ip='10.0.3.1/24')
        host8 = net.addHost('h8', ip='10.0.3.2/24')

        # Connect hosts to access layer switches
        net.addLink(host1, access_switch1)
        net.addLink(host2, access_switch1)
        net.addLink(host3, access_switch2)
        net.addLink(host4, access_switch2)
        net.addLink(host5, access_switch3)
        net.addLink(host6, access_switch3)
        net.addLink(host7, access_switch4)
        net.addLink(host8, access_switch4)

        # Start the network
        net.start()
        print("Tree-based topology is up. Use 'pingall' in the CLI to test connectivity.")

        # Test connectivity automatically
        net.pingAll()

        # Enter the Mininet CLI
        CLI(net)

        # Stop the network
        net.stop()

        
