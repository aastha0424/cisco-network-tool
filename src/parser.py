import os
import re

def parse_config_files(directory):
    """Parses all config.dump files in a directory and returns a dictionary."""
    configs = {}
    for device_name in os.listdir(directory):
        config_path = os.path.join(directory, device_name, 'config.dump')
        if os.path.isdir(os.path.join(directory, device_name)) and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
                # The hostname from the file is the most reliable source
                hostname_match = re.search(r"hostname\s+(\S+)", content)
                if hostname_match:
                    hostname = hostname_match.group(1)
                    configs[hostname] = parse_single_config(content)
    return configs

def parse_single_config(content):
    """Uses regex to extract info from a single config file's content."""
    data = {'interfaces': {}}
    
    # Extract hostname
    hostname_match = re.search(r"hostname\s+(\S+)", content)
    if hostname_match:
        data['hostname'] = hostname_match.group(1)
    
    # Extract default gateway (static default route)
    gateway_match = re.search(r"ip route 0\.0\.0\.0 0\.0\.0\.0 (\S+)", content)
    if gateway_match:
        data['default_gateway'] = gateway_match.group(1)

    # Find all interface configuration blocks
    interface_blocks = re.findall(r"interface\s+(\S+)\n(.+?)(?=\n!|\Z)", content, re.DOTALL)
    
    for if_name, if_config in interface_blocks:
        data['interfaces'][if_name] = {}
        
        # Extract IP address and subnet mask
        ip_match = re.search(r"ip address\s+([\d\.]+)\s+([\d\.]+)", if_config)
        if ip_match:
            data['interfaces'][if_name]['ip'] = ip_match.group(1)
            data['interfaces'][if_name]['mask'] = ip_match.group(2)

        # Extract bandwidth
        bw_match = re.search(r"bandwidth\s+(\d+)", if_config)
        if bw_match:
            data['interfaces'][if_name]['bandwidth'] = int(bw_match.group(1))
        # Inside the 'for if_name, if_config in interface_blocks:' loop

        # Extract MTU
        mtu_match = re.search(r"mtu\s+(\d+)", if_config)
        if mtu_match:
            data['interfaces'][if_name]['mtu'] = int(mtu_match.group(1))

    return data