import networkx as nx

def run_load_analysis(graph):
    """Analyzes link capacity vs. a predefined traffic load."""
    print("\n--- Running Load Analysis ---")

    # Define a sample traffic demand in kilobits per second (kbps)
    # R1's bandwidth is 100,000 kbps (100 Mbps), so this should pass.
    traffic_demands = {
        ('R1', 'R3'): 50000  # 50,000 kbps = 50 Mbps demand
    }

    for (source, target), demand in traffic_demands.items():
        print(f"\nAnalyzing demand from {source} to {target} ({demand} kbps)...")

        if not graph.has_node(source) or not graph.has_node(target):
            print(f"[FAIL] Source {source} or Target {target} not in topology.")
            continue

        try:
            # Find the shortest path for the traffic
            path = nx.shortest_path(graph, source=source, target=target)
            print(f"  - Primary path found: {' -> '.join(path)}")

            is_sufficient = True
            # Check each link in the path
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                
                # To find the link's bandwidth, we need to find the connected interfaces
                # This logic assumes the first found connected interface represents the link
                link_bw = 0
                for if_name, if_data in graph.nodes[u]['interfaces'].items():
                    # This is a simplified check. A more robust solution would store
                    # interface details on the graph edges themselves.
                    if 'bandwidth' in if_data:
                        link_bw = if_data['bandwidth']
                        break
                
                if link_bw < demand:
                    print(f"  - [FAIL] Link {u}->{v} cannot support demand. (Capacity: {link_bw} kbps, Demand: {demand} kbps)")
                    is_sufficient = False
                else:
                    print(f"  - [PASS] Link {u}->{v} can support demand. (Capacity: {link_bw} kbps, Demand: {demand} kbps)")
            
            if is_sufficient:
                print(f"Result: Primary path can handle the traffic demand.")
            else:
                # TODO: Recommend a secondary path if one exists
                print(f"Result: Primary path is INSUFFICIENT for the traffic demand.")


        except nx.NetworkXNoPath:
            print(f"[FAIL] No path exists between {source} and {target}.")

    print("\n--- Analysis Complete ---\n")