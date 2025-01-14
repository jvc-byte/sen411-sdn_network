#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import sys

def custom_tree_topology():
    """
    Create a custom tree-based topology with three layers:
    - Core Layer (1 switch)
    - Aggregation Layer (2 switches)
    - Access Layer (4 switches)
    - 8 hosts total (4 in each subnet)
    """
    try:
        # Initialize Mininet with RemoteController and TCLink
        net = Mininet(
            controller=RemoteController,
            switch=OVSSwitch,
            link=TCLink,
            autoSetMacs=True
        )

        info('*** Adding controller\n')
        controller = net.addController(
            name='ryuController',
            controller=RemoteController,
            ip='10.0.2.15',  # Using localhost for development
            port=6633
        )

        info('*** Adding switches\n')
        # Core layer
        core = net.addSwitch('s1', protocols='OpenFlow13')
        
        # Aggregation layer
        aggr = [
            net.addSwitch(f's{i}', protocols='OpenFlow13')
            for i in range(2, 4)
        ]
        
        # Access layer
        access = [
            net.addSwitch(f's{i}', protocols='OpenFlow13')
            for i in range(4, 8)
        ]

        info('*** Adding hosts\n')
        # First subnet (10.0.0.0/24)
        hosts_subnet1 = [
            net.addHost(
                f'h{i}',
                ip=f'10.0.0.{i}/24',
                defaultRoute='via 10.0.0.254'
            )
            for i in range(1, 5)
        ]
        
        # Second subnet (10.0.1.0/24)
        hosts_subnet2 = [
            net.addHost(
                f'h{i}',
                ip=f'10.0.1.{i-4}/24',
                defaultRoute='via 10.0.1.254'
            )
            for i in range(5, 9)
        ]

        info('*** Creating links\n')
        # Core to Aggregation links
        for sw in aggr:
            net.addLink(
                core, sw,
                bw=50,
                delay='2ms',
                loss=0,
                use_htb=True
            )

        # Aggregation to Access links
        net.addLink(aggr[0], access[0], bw=30, delay='5ms', use_htb=True)
        net.addLink(aggr[0], access[1], bw=30, delay='5ms', use_htb=True)
        net.addLink(aggr[1], access[2], bw=30, delay='5ms', use_htb=True)
        net.addLink(aggr[1], access[3], bw=30, delay='5ms', use_htb=True)

        # Connect hosts to access switches
        for i, host in enumerate(hosts_subnet1):
            sw_index = i // 2
            net.addLink(host, access[sw_index], bw=10, delay='1ms', use_htb=True)

        for i, host in enumerate(hosts_subnet2):
            sw_index = (i // 2) + 2
            net.addLink(host, access[sw_index], bw=10, delay='1ms', use_htb=True)

        info('*** Starting network\n')
        net.build()
        controller.start()
        
        # Start all switches
        for switch in net.switches:
            switch.start([controller])

        info('*** Running basic connectivity tests\n')
        net.pingAll()

        info('*** Running CLI\n')
        CLI(net)

    except Exception as e:
        info(f'*** Error: {str(e)}\n')
        sys.exit(1)
    
    finally:
        info('*** Stopping network\n')
        if 'net' in locals():
            net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    custom_tree_topology()