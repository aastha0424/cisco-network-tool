import argparse
from src.parser import parse_config_files
from src.topology import create_topology, draw_topology
from src.validator import run_validation_checks
from src.analyzer import run_load_analysis
from src.simulator.engine import SimulationEngine # Import the engine

def main():
    parser = argparse.ArgumentParser(description="Network Analysis and Simulation Tool")
    parser.add_argument('action', choices=['topology', 'validate', 'analyze', 'simulate'], help="Action to perform.")
    args = parser.parse_args()

    device_configs = parse_config_files('./configs')
    network_graph = create_topology(device_configs)

    if args.action == 'topology':
        print("Generating and saving network topology...")
        draw_topology(network_graph)
    elif args.action == 'validate':
        run_validation_checks(network_graph)
    elif args.action == 'analyze':
        run_load_analysis(network_graph)
    elif args.action == 'simulate':
        # This section launches the simulation
        sim_engine = SimulationEngine(network_graph)
        sim_engine.run()

if __name__ == "__main__":
    main()