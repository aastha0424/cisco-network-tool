---

# Cisco Network Analysis and Simulation Tool

A Python-based tool developed for the **Cisco Networking Academy Virtual Internship Program 2025**. This tool automatically generates, validates, analyzes, and simulates a network topology from raw router configuration files.

---

## ✨ Core Features

1. **Automatic Topology Generation**

   * Constructs a network graph from a directory of router configuration files.

2. **Configuration Validation**

   * Detects critical network errors such as duplicate IPs, MTU mismatches, and incorrect default gateways.

3. **Performance Analysis**

   * Verifies if network links can handle predefined traffic loads.

4. **Dynamic Network Simulation**

   * Runs a stable, multithreaded network simulation with:

     * OSPF-like neighbor discovery
     * Interactive command-line controls (`ping`, `pause`, `resume`)
     * Real-time link failure simulation (`fail link`)
     * Dynamic routing updates based on link status

---

## 🚀 Getting Started

Follow these steps to set up the project locally.

### Prerequisites

* Python 3.x
* `pip` (Python package installer)

### Installation

```bash
# Clone the repository
git clone https://github.com/aastha0424/cisco-network-tool.git
cd cisco-network-tool

# Install required dependencies
pip install -r requirements.txt
```

### Configuration Files

Populate the `configs/` directory with your router configuration files, for example:

```
configs/
├── R1/
│   └── config.dump
├── R2/
│   └── config.dump
...
```

---

## 💻 Usage

Run the main simulator script:

```bash
python src/simulator/main.py
```

Available interactive commands during simulation:

* `ping <source> <destination>` – Test connectivity between routers
* `pause` – Pause the simulation
* `resume` – Resume the simulation
* `fail link <router1> <router2>` – Simulate a link failure

---

## 🛠️ Project Structure

```
cisco-network-tool/
├── configs/          # Router configuration files
├── src/
│   ├── parser.py      # Parses router configs
│   ├── topology.py    # Builds network graph
│   ├── validator.py   # Validates network configs
│   ├── analyzer.py    # Performs performance analysis
│   └── simulator/     # Network simulation scripts
├── requirements.txt
└── README.md
```

---

## 📄 License

This project is licensed under the MIT License.

---

