from ipaddress import IPv4Interface, IPv4Address
def run_validation_checks(graph):
    """Runs all validation checks and prints a report."""
    print("\n--- Running Validation Checks ---")
    
    errors_found = False
    
    # Check for duplicate IP addresses
    duplicate_ips = find_duplicate_ips(graph)
    if duplicate_ips:
        errors_found = True
        print("[FAIL] Duplicate IP addresses found:")
        for ip, devices in duplicate_ips.items():
            print(f"  - IP {ip} is used by: {', '.join(devices)}")

    # Check for MTU mismatches
    mtu_mismatches = find_mtu_mismatches(graph)
    if mtu_mismatches:
        errors_found = True
        print("[FAIL] MTU mismatches found:")
        for (d1, i1, m1), (d2, i2, m2) in mtu_mismatches:
            print(f"  - {d1}({i1}) MTU is {m1}, but {d2}({i2}) MTU is {m2}")
    
    # Check for incorrect gateway addresses
    gateway_errors = find_incorrect_gateways(graph)
    if gateway_errors:
        errors_found = True
        print("[FAIL] Incorrect gateway configurations found:")
        for device, gateway in gateway_errors:
            print(f"  - {device}'s default gateway {gateway} is not on a directly connected network.")

    if not errors_found:
        print("[PASS] No configuration issues found.")
        
    print("--- Validation Complete ---\n")

def find_duplicate_ips(graph):
    # ... (your existing code for this function)
    ip_map = {}
    duplicates = {}
    for device_name in graph.nodes():
        interfaces = graph.nodes[device_name].get('interfaces', {})
        for if_name, if_data in interfaces.items():
            if 'ip' in if_data:
                ip = if_data['ip']
                if ip not in ip_map:
                    ip_map[ip] = []
                ip_map[ip].append(device_name)
    for ip, devices in ip_map.items():
        if len(devices) > 1:
            duplicates[ip] = devices
    return duplicates

def find_mtu_mismatches(graph):
    """Finds MTU mismatches on connected interfaces."""
    mismatches = []
    # In your topology builder, you'll need to store which interfaces are connected.
    # For now, we'll find the interfaces based on shared subnets again.
    # A better long-term solution is to store interface names on the graph edges.
    
    nodes = list(graph.nodes())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            d1_name, d2_name = nodes[i], nodes[j]
            d1_data = graph.nodes[d1_name]
            d2_data = graph.nodes[d2_name]
            
            for i1, i1_data in d1_data.get('interfaces', {}).items():
                for i2, i2_data in d2_data.get('interfaces', {}).items():
                    if 'ip' in i1_data and 'ip' in i2_data:
                        # Check if they are in the same subnet to confirm they are linked
                        from ipaddress import IPv4Interface
                        net1 = IPv4Interface(f"{i1_data['ip']}/{i1_data['mask']}").network
                        net2 = IPv4Interface(f"{i2_data['ip']}/{i2_data['mask']}").network

                        if net1 == net2:
                            mtu1 = i1_data.get('mtu')
                            mtu2 = i2_data.get('mtu')
                            if mtu1 is not None and mtu2 is not None and mtu1 != mtu2:
                                mismatches.append(((d1_name, i1, mtu1), (d2_name, i2, mtu2)))
    return mismatches

def find_incorrect_gateways(graph):
    """Checks if a router's default gateway is on a connected subnet."""
    errors = []
    for device_name, device_data in graph.nodes(data=True):
        gateway_ip = device_data.get('default_gateway')
        if not gateway_ip:
            continue # No default gateway configured, so no error

        is_valid_gateway = False
        # Check all of the device's own interfaces/subnets
        for if_data in device_data.get('interfaces', {}).values():
            if 'ip' in if_data:
                try:
                    # Check if the gateway IP is in any of the connected subnets
                    network = IPv4Interface(f"{if_data['ip']}/{if_data['mask']}").network
                    if IPv4Address(gateway_ip) in network:
                        is_valid_gateway = True
                        break
                except ValueError:
                    continue
        
        if not is_valid_gateway:
            errors.append((device_name, gateway_ip))
            
    return errors