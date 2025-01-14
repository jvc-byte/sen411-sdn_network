from mininet.log import setLogLevel, info

from infra import netType

if __name__ == '__main__':
    setLogLevel('info')
    netType.tree_topology()