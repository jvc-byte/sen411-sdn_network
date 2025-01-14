# sdn_network
A basic Software-defined network  data plane
# Mininet SDN Topology

This project demonstrates how to use Mininet to simulate different network topologies and integrate them with an SDN controller, such as Ryu. It includes simple, complex, and tree-based topologies, designed to illustrate the flexibility of Software-Defined Networking (SDN).

## Features

- **Simple Topology**: A basic network with a single switch, a router, and multiple hosts.
- **Complex Topology**: A multi-switch and multi-host network with configurable link properties.
- **Tree-Based Topology**: A hierarchical network with core, aggregation, and access layers.
- **Controller Integration**: The topologies are designed to work seamlessly with the Ryu SDN controller.

## Prerequisites

Ensure the following tools and libraries are installed on your system:

- **Python 3.9+**
- **Mininet (2.3.0.dev6)**

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:imosudi/sdn_network.git
   cd sdn_network
   ```

2. Set up a Python virtual environment:
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure Mininet and the Ryu controller are installed on your system:
   ```bash
   sudo apt install mininet
   sudo pip install ryu
   ```

## Usage

### A simple SDN Controller 
You might want to make use of this basic SDN controller if you do not have a running controller  
https://github.com/imosudi/sdn_controller

### Running the Topology

1. Launch a desired topology from the `main.py` script:
   ```bash
   sudo mn -c
   sudo python3 main.py
   ```

   By default, this will run the tree-based topology.

2. To switch to a different topology, modify the last line in `main.py` to one of the following:
   ```python
   netType.simple_topology()
   netType.complex_topology()
   netType.tree_topology()
   ```

3. Start the Ryu controller in a separate terminal window:
   ```bash
   ryu-manager path/to/your_controller.py
   ```

4. Test connectivity using the Mininet CLI:
   ```bash
   mininet> pingall
   ```

### Modifying Topologies

Each topology is defined in the `infra.py` file. You can:

- Add or remove switches and hosts.
- Modify link properties such as bandwidth (`bw`), delay, and packet loss.
- Adjust IP address configurations.

## Project Structure

```
├── infra.py           # Contains topology definitions
├── main.py            # Entry point for running topologies
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
```

## Example Topology Descriptions

### Simple Topology
- One switch (`s1`), one router (`r0`), and 8 hosts (`h1` to `h8`).
- Hosts are divided into two subnets (`10.0.0.0/24` and `10.0.1.0/24`).
- The router connects the subnets and handles inter-network routing.

### Complex Topology
- Three switches (`s1`, `s2`, `s3`) interconnected with varying link properties.
- Four hosts (`h1` to `h4`) with different bandwidth and latency configurations.

### Tree-Based Topology
- A core switch (`s1`), two aggregation switches (`s2`, `s3`), and four access switches (`s4` to `s7`).
- Eight hosts (`h1` to `h8`) distributed across the access switches.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [Mininet Documentation](http://mininet.org/)
- [Ryu SDN Framework](https://osrg.github.io/ryu/)
- [OpenFlow Protocol](https://opennetworking.org/openflow/)



Feel free to contribute to this project by creating issues or submitting pull requests.
