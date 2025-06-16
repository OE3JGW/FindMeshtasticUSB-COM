#!/usr/bin/env python3

from meshtastic.serial_interface import SerialInterface
import sys
from meshtastic.util import findPorts

def find_meshtastic_port():
    """
    Find the COM port where a Meshtastic device is connected.
    Returns the port name if found, None otherwise.
    """
    print("Scanning for Meshtastic devices...")
    
    # Use Meshtastic's built-in port detection
    ports = findPorts()
    
    if not ports:
        print("No Meshtastic devices found!")
        return None
    
    print("\nFound potential Meshtastic devices:")
    for port in ports:
        print(f"- {port}")
    
    # Try to connect to the first found port
    try:
        print(f"\nTrying to connect to {ports[0]}...")
        interface = SerialInterface(devPath=ports[0])
        
        # Try to get node info to verify it's a Meshtastic device
        node_info = interface.getMyNodeInfo()
        if node_info:
            print(f"✅ Found Meshtastic device on {ports[0]}")
            print(f"Device info: {node_info}")
            return ports[0]
            
    except Exception as e:
        print(f"❌ Error connecting to {ports[0]}: {str(e)}")
    
    print("\nNo working Meshtastic device found!")
    return None

def main():
    port = find_meshtastic_port()
    if port:
        print(f"\nMeshtastic device found on: {port}")
        # Update config file
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read('config.cfg')
            config.set('Serial', 'port', port)
            with open('config.cfg', 'w') as f:
                config.write(f)
            print(f"Updated config.cfg with port: {port}")
        except Exception as e:
            print(f"Error updating config file: {e}")
    else:
        print("\nNo Meshtastic device found. Please check your connections.")
        sys.exit(1)

if __name__ == "__main__":
    main() 