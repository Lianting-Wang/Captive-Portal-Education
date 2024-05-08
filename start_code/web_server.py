# Import required libraries and modules
import ssl
import json
import atexit
import logging
import threading
import configparser
from urllib.parse import parse_qs
from http.server import HTTPServer, SimpleHTTPRequestHandler
from scapy.all import ARP, Ether, srp

# Read configurations from an external file
config = configparser.ConfigParser()
config.read('/home/mininet/Captive-Portal/config.ini')
TCP_server_ip = config['DEFAULT']['internet_ip'] # TCP server IP address
TCP_server_port = int(config['DEFAULT']['TCP_server_port']) # TCP server port
ssl_enable = config['DEFAULT']['ssl_enable'] # Whether SSL is enabled or not
keyfile = config['DEFAULT']['keyfile'] # SSL key file
certfile = config['DEFAULT']['certfile'] # SSL certificate file
captive_portal_host = config['DEFAULT']['captive_portal_host'] # Captive portal host name
web_server_log = config['DEFAULT']['web_server_log'] # Log file for the web server

# Setup logging to record server events
logging.basicConfig(filename=web_server_log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variables to hold the HTTP and HTTPS server instances
httpd = None
httpsd = None

# Set the protocol based on SSL settings
protocol = 'http'
if (ssl_enable == 'True'):
    protocol = 'https'

# TCP Client class to communicate with the central server
class TCPClient:
    def __init__(self, host=TCP_server_ip, port=TCP_server_port):
        """Initialize a TCP client and connect to the server."""
        self.host = host
        self.port = port
        # Create a socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, port))

    def send_request(self, request):
        """Send a JSON request to the server and return the JSON response."""
        self.connection.sendall(json.dumps(request).encode()) # Send the JSON-encoded request
        return json.loads(self.connection.recv(1024).decode()) # Receive and decode the JSON response

    def set_valid(self, value):
        """Send the valid MAC address to the server."""
        return self.send_request({'command': 'add', 'value': value})

    def close_connection(self):
        """Close the connection to the server."""
        self.connection.close()

# Initialize a global TCP client instance to communicate with the server
global_tcp_client = TCPClient()

# Ensure the TCP client connection is closed when the program exits
def close_tcp_client():
    global_tcp_client.close_connection()

# HTTP request handler class for the captive portal
class RedirectHandler(SimpleHTTPRequestHandler):
    def get_mac(self, ip):
        """Use an ARP request to obtain the MAC address of a specified IP."""
        # Create ARP request with broadcast Ethernet frame
        arp_request = ARP(pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request

        # Send ARP request and receive response
        answered, _ = srp(arp_request_broadcast, timeout=2, verbose=False)
        # Extract and return MAC address from response
        return answered[0][1].hwsrc if answered else "Unknown"

    def redirect_handler(self, redirect_domain, host):
        """Redirect HTTP request to the specified domain."""
        logging.info(f"Redirecting to {redirect_domain} from host {host}")
        self.send_response(302) # HTTP 302 (redirect)
        self.send_header('Location', f'{protocol}://{redirect_domain}/?original_host={host}') # Set redirect URL
        self.end_headers()

    def request_handler(self):
        """Serve files from the web directory based on the requested path."""
        path = self.path.split('?', 1)[0]

        # Determine file path based on the request
        if path == '/':
            path = '/index.html'
        elif '.' not in path:
            path += '.html'

        # Determine the MIME type based on the file extension
        if path.endswith(".html"):
            mimetype = 'text/html'
        elif path.endswith(".css"):
            mimetype = 'text/css'
        elif path.endswith(".js"):
            mimetype = 'application/javascript'
        else:
            mimetype = 'text/plain'

        try:
            # Open and read the requested file, then send the content
            with open(f'../web/{path[1:]}', 'rb') as file:
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(file.read())
        except FileNotFoundError:
            # Send 404 error if file is not found
            self.send_error(404, 'File Not Found: %s' % path)

    def do_GET(self):
        """Handle GET requests for the captive portal."""
        # Retrieve the host from the request headers
        host = self.headers.get('Host')
        logging.info(f"Received GET request for {self.path} from {host}")

        # Define the target domain for the redirect
        redirect_domain = captive_portal_host

        # If the host is not the captive portal, redirect the request
        if host and host != redirect_domain:
            # Redirect the request to the captive portal (TODO: Implement)
            pass
        else:
            # Serve the requested content (TODO: Implement)
            pass

    def do_POST(self):
        """Handle POST requests for the captive portal."""
        # Retrieve the client's IP address and log the request
        request_ip = self.client_address[0]
        logging.info(f"Received POST request for {self.path} from IP {request_ip}")
        mac_address = self.get_mac(request_ip)

        # Read the POST data from the request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        path = self.path.split('?', 1)[0]

        if path == '/login':
            # Parse the JSON data from the request
            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                # Return a 400 error for invalid JSON
                self.send_error(400, 'Invalid JSON')
                return

            # Initialize the response
            response = {'success': False}
            if True: # TODO: Verify credentials (username: 'test', password: 'pass')
                try:
                    # Send an authentication request to the server (TODO: Implement)
                    data = {'result': False}
                    if data['result']:
                        response = {'success': True}
                    else:
                        response = {'success': False, 'error': 'MAC address not added correctly'}
                except Exception as e:
                    response = {'success': False, 'error': str(e)}

            # Send JSON response to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # Return a 404 error for unknown paths
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response = f'404 Not Found: {path}'
            self.wfile.write(response.encode('utf-8'))

# Function to initialize and run the HTTP server
def run(port):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, RedirectHandler)
    logging.info(f'Starting server on port {port}')
    return httpd

# Start the HTTP server in a separate thread
def start_http_server():
    global httpd
    httpd = run(port=80)
    httpd.serve_forever()

# Start the HTTPS server in a separate thread
def start_https_server():
    global httpsd
    httpsd = run(port=443)
    httpsd.socket = ssl.wrap_socket(httpsd.socket, 
                                    keyfile=keyfile, 
                                    certfile=certfile, 
                                    server_side=True)
    httpsd.serve_forever()

# Close both HTTP and HTTPS servers
def close_servers():
    logging.info("Closing HTTP and HTTPS servers...")
    if httpd:
        httpd.shutdown()
        httpd.server_close()
    if httpsd:
        httpsd.shutdown()
        httpsd.server_close()

# Register functions to be called on program exit
atexit.register(close_servers)
atexit.register(close_tcp_client)

# Start the HTTP server in a new thread
threading.Thread(target=start_http_server).start()

# Start the HTTPS server if SSL is enabled
if (ssl_enable == 'True'):
    threading.Thread(target=start_https_server).start()
