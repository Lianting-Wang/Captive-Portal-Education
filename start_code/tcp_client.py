import json
import socket
import configparser

# Load the configuration parser
config = configparser.ConfigParser()
# Read the configuration file located at the specified path
config.read('/home/mininet/Captive-Portal/config.ini')

# Extract configuration settings for the TCP server from the config file
TCP_server_ip = config['DEFAULT']['TCP_server_pox_ip']   # IP address of the TCP server
TCP_server_port = int(config['DEFAULT']['TCP_server_port'])  # Port number for the TCP server (convert to integer)

class TCPClient:
    def __init__(self, host=TCP_server_ip, port=TCP_server_port):
        self.host = host  # Server IP address
        self.port = port  # Server port number
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a new socket using IPv4 and TCP
        self.connection.connect((host, port))  # Establish a connection to the server

    def send_request(self, request):
        # This method should send a JSON request to the server and handle the response
        # 'request' should be a dictionary that will be converted to JSON
        pass

    def get_host(self):
        # This method should request the host MAC address from the server
        # It might receive this data from the server in JSON format or as a simple string
        pass

    def set_host(self, value):
        # This method should send a request to set the host MAC address on the server
        # 'value' should be the MAC address to set
        pass

    def get_internet(self):
        # This method should request the internet MAC address from the server
        # This address might be used for routing or filtering purposes
        pass

    def set_internet(self, value):
        # This method should send a request to set the internet MAC address on the server
        # 'value' should be the MAC address to set
        pass

    def check_valid(self, value):
        # This method should check if the provided MAC address 'value' is valid or not
        # This might involve checking the format or querying a database
        pass

    def close_connection(self):
        # This method should properly close the connection to the server
        # It's important to close the connection to free up resources
        pass
