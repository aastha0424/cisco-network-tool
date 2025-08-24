Cisco Network Analysis and Simulation Tool
This project is a Python-based tool developed for the Cisco Networking Academy's Virtual Internship Program 2025. It automatically generates, validates, analyzes, and simulates a network topology from raw router configuration files.

✨ Core Features
Automatic Topology Generation: Constructs a network graph from a directory of router configuration files.

Configuration Validation: Detects critical network errors like duplicate IPs, MTU mismatches, and incorrect default gateways.

Performance Analysis: Checks if network links can handle predefined traffic loads.

Dynamic Network Simulation: Runs a stable, multithreaded simulation of the network with features like:

OSPF-like neighbor discovery.

Interactive command-line control (ping, pause, resume).

Real-time link failure simulation (fail link).

Dynamic routing updates based on link status.

🚀 Getting Started
Follow these steps to get the project running on your local machine.

Prerequisites
Python 3.x

pip (Python package installer)

Installation
Clone the repository:

git clone https://github.com/aastha0424/cisco-network-tool.git
cd cisco-network-tool

Install dependencies:

pip install -r requirements.txt

Populate Configurations:
Make sure your configs/ directory is populated with router configuration files (e.g., configs/R1/config.dump).
