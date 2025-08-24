import networkx as nx
import matplotlib.pyplot as plt
from ipaddress import IPv4Interface, AddressValueError

def create_topology(configs):
    """Creates a network graph and infers links from the parsed configurations."""
    G = nx.Graph()
    
    # Add all devices as nodes first
    for device_name, data in configs.items():
        G.add_node(device_name, **data)
    
    # Get a list of device names to iterate over
    device_names = list(configs.keys())
    
    # Compare each device with every other device to find links
    for i in range(len(device_names)):
        for j in range(i + 1, len(device_names)):
            dev1_name = device_names[i]
            dev2_name = device_names[j]
            
            dev1_interfaces = configs[dev1_name].get('interfaces', {})
            dev2_interfaces = configs[dev2_name].get('interfaces', {})

            # Check all interface pairs between the two devices
            for if1_name, if1_data in dev1_interfaces.items():
                for if2_name, if2_data in dev2_interfaces.items():
                    # Ensure both interfaces have IP and mask info
                    if 'ip' in if1_data and 'ip' in if2_data:
                        try:
                            # Create network objects using the ipaddress library
                            net1 = IPv4Interface(f"{if1_data['ip']}/{if1_data['mask']}").network
                            net2 = IPv4Interface(f"{if2_data['ip']}/{if2_data['mask']}").network
                            
                            # If the networks are the same, a link exists
                            if net1 == net2:
                                print(f"Found link between {dev1_name} ({if1_name}) and {dev2_name} ({if2_name})")
                                G.add_edge(dev1_name, dev2_name)
                        except AddressValueError:
                            # Handles cases where IP/mask might be invalid
                            continue
    return G

def draw_topology(graph):
    """Saves a visual representation of the graph."""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=2500, font_size=10, font_weight='bold')
    plt.title("Generated Network Topology")
    plt.savefig("topology.png")
    print("Topology saved to topology.png")