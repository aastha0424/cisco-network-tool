# Note: This is a temporary file for testing the parser.
from src.parser import parse_config_files
import json # Use json for pretty-printing the dictionary

def test_parser():
    print("--- Testing Parser ---")
    device_configs = parse_config_files('./configs')
    
    if not device_configs:
        print("Parser did not find or process any config files.")
    else:
        # Pretty-print the output
        print(json.dumps(device_configs, indent=2))
        
if __name__ == "__main__":
    test_parser()