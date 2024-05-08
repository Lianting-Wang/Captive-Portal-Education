import json
import atexit
import socket
import logging
import threading
from datetime import datetime, timedelta
import configparser

# Read configuration from an INI file.
config = configparser.ConfigParser()
config.read('/home/mininet/Captive-Portal/config.ini')

# Extract configuration settings from the 'DEFAULT' section.
TCP_server_ip = config['DEFAULT']['TCP_server_ip']
TCP_server_port = int(config['DEFAULT']['TCP_server_port'])
captive_portal_mac = config['DEFAULT']['captive_portal_mac']
internet_mac = config['DEFAULT']['internet_mac']
server_log = config['DEFAULT']['server_log']

# Set up logging to file with a specific format.
logging.basicConfig(filename=server_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the validity duration for MAC addresses.
valid_time = timedelta(days=1)

class MACSet:
    def __init__(self):
        self.approved_macs = {}  # Dictionary to store approved MAC addresses.

    def add_mac(self, mac):
        # Add a MAC address to the set and log the addition.
        pass

    def remove_mac(self, mac):
        # Remove a MAC address from the set and log the removal.
        pass

    def check_mac(self, mac):
        # Check if a MAC address is in the approved set and log the check.
        pass

class Server:
    def __init__(self, hMAC=captive_portal_mac, iMAC=internet_mac, host=TCP_server_ip, port=TCP_server_port):
        self.host = host  # IP address of the server.
        self.port = port  # Port on which the server listens.
        self.hMAC = hMAC  # MAC address of the captive portal.
        self.iMAC = iMAC  # MAC address to route to the internet.
        self.MACSet = MACSet()  # Instance of MACSet to manage MAC addresses.
        self.server_socket = None  # To hold the socket object.
        self.lock = threading.Lock()  # Lock for thread-safe operations.
        self.stop_event = threading.Event()  # Event to signal server stop.
    
    def handle_client(self, conn, addr):
        # Handle client connections and interactions.
        pass

    def run_tcp_server(self):
        # Start the TCP server, setting up the socket and listening for connections.
        pass

    def stop_server(self):
        # Cleanly stop the TCP server and close all resources.
        pass

if __name__ == '__main__':
    server = Server()
    server.run_tcp_server()
    atexit.register(server.stop_server)  # Ensure the server is stopped cleanly on script exit.
