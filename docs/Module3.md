## Guide for DNS Server Implementation

**Objective:**
The goal of this assignment is to create a DNS interceptor that captures DNS queries and forwards them to a specified DNS server for resolution, then returns the response to the client. This helps students understand DNS protocols and the process of intercepting and handling network traffic.

### `forward_dns_query` Function
1. **Description:**
   - This function takes in raw DNS query data, forwards it to a specified DNS server, and returns the response.

2. **Implementation Steps:**
   - **Socket Creation:** Use a UDP socket to send the DNS query to the server.
   - **Set Timeout:** Set a timeout for the socket to avoid indefinite waiting for a response.
   - **Send Data:** Use `sock.sendto` to send the DNS query data to the specified server and port.
   - **Receive Response:** Use `sock.recvfrom` to receive the response data.
   - **Return Response:** Return the response data or `None` if the request times out.

#### `forward_dns_query` Detailed Implementation Steps

1. **Function Parameters:**
   - **data:** The raw DNS query data to be forwarded.
   - **server:** The DNS server IP to forward the query to. Default is `DNS_Server` (Google's DNS server: 8.8.8.8).
   - **port:** The port number of the DNS server. Default is 53.

2. **Socket Creation:**
   - **Objective:** Create a UDP socket for sending and receiving DNS queries.
   - **Steps:**
     - Use the `socket.socket` function with `AF_INET` (IPv4) and `SOCK_DGRAM` (UDP) parameters to create the socket.
     - This will be used to send DNS queries and receive responses from the DNS server.

   ```python
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   ```

3. **Set Timeout:**
   - **Objective:** Avoid waiting indefinitely for a response from the DNS server.
   - **Steps:**
     - Set a timeout on the socket using `sock.settimeout(seconds)`.
     - Choose a reasonable timeout value (e.g., 2 seconds).

   ```python
   sock.settimeout(2)
   ```

4. **Send DNS Query Data:**
   - **Objective:** Forward the DNS query data to the specified DNS server.
   - **Steps:**
     - Use `sock.sendto(data, (server, port))` to send the DNS query data to the server.
     - The destination is specified as a tuple containing the server IP and port number.

   ```python
   sock.sendto(data, (server, port))
   ```

5. **Receive Response:**
   - **Objective:** Receive the DNS response from the server.
   - **Steps:**
     - Use `sock.recvfrom(buffer_size)` to read the response data.
     - The buffer size should be large enough to accommodate the expected response size (e.g., 1024 bytes).
     - Enclose this step in a `try-except` block to handle `socket.timeout` exceptions.

   ```python
   try:
       response, _ = sock.recvfrom(1024)
   except socket.timeout:
       logging.warning(f"Timeout occurred while forwarding query to DNS server {server}:{port}")
       return None
   ```

6. **Return Response:**
   - **Objective:** Provide the DNS response back to the calling function.
   - **Steps:**
     - If the response is successfully received, return the response data.
     - Otherwise, return `None` to indicate a timeout or failure.

   ```python
   return response
   ```

7. **Socket Cleanup:**
   - **Objective:** Properly close the socket to free up resources.
   - **Steps:**
     - Ensure that the socket is closed after usage, whether the request was successful or not.
     - Using a `with` statement will automatically close the socket when the block ends.

   ```python
   with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
       ...
   ```

### `dns_interceptor` Function
1. **Description:**
   - This function intercepts DNS queries from clients, forwards them to the specified DNS server using `forward_dns_query`, and then returns the DNS response to the client.

2. **Implementation Steps:**
   - **DNS Query Detection:** Use `packet.haslayer(DNSQR)` to detect DNS queries.
   - **Check Source:** Ensure the query is not from or to the DNS server itself.
   - **Forward Query:** Extract the original query data and pass it to `forward_dns_query`.
   - **Construct Response:** If a response is received, construct a spoofed response packet with the appropriate fields.
   - **Send Response:** Use `send` to send the response back to the original client.

#### `dns_interceptor` Detailed Implementation Steps

1. **Check for DNS Query Layer:**
   - **Description:** The first step is to check if the incoming packet contains a DNS query (`DNSQR` layer). This ensures that only DNS queries are processed.
   - **Code Example:** 
     ```python
     if packet.haslayer(DNSQR):
     ```
   - **Explanation:** `packet.haslayer(DNSQR)` checks if the packet has a DNS query layer, which indicates that it's a DNS request.

2. **Exclude Certain IPs:**
   - **Description:** Filter out packets from or to specific IP addresses (like the DNS server itself or the interceptor itself) to avoid infinite loops or unnecessary handling.
   - **Code Example:** 
     ```python
     if packet[IP].src != captive_portal_ip and packet[IP].src != DNS_Server:
     ```
   - **Explanation:** This ensures that packets from/to these IPs are not handled by the interceptor.

3. **Extract Original DNS Query Data:**
   - **Description:** Extract the original DNS query data from the intercepted packet. This data will be forwarded to the DNS server.
   - **Code Example:** 
     ```python
     original_data = bytes(packet[UDP].payload)
     ```
   - **Explanation:** `packet[UDP].payload` retrieves the UDP payload, which contains the DNS query data. The `bytes` function converts it to a byte string.

4. **Forward DNS Query:**
   - **Description:** Call the `forward_dns_query` function to forward the DNS query to the actual DNS server and receive the response.
   - **Code Example:** 
     ```python
     response_data = forward_dns_query(original_data)
     ```
   - **Explanation:** The `forward_dns_query` function takes the DNS query data and forwards it to the specified DNS server, returning the response data.

5. **Check Response and Construct Spoofed Packet:**
   - **Description:** If a valid response is received, construct a spoofed response packet to send back to the original client. This step involves copying the DNS query ID, DNS question, and copying other relevant fields.
   - **Code Example:** 
     ```python
     if response_data:
         response_packet = DNS(response_data)
         spoofed_pkt = IP(dst=packet[IP].src, src=packet[IP].dst) /\
                       UDP(dport=packet[UDP].sport, sport=packet[UDP].dport) /\
                       DNS(id=packet[DNS].id, qr=1, aa=response_packet.aa, qd=response_packet.qd,
                           an=response_packet.an, ns=response_packet.ns, ar=response_packet.ar)
     ```
   - **Explanation:**
     - `response_packet = DNS(response_data)`: Convert the raw response data into a DNS packet.
     - `IP(dst=packet[IP].src, src=packet[IP].dst)`: Spoof the source and destination IP addresses.
     - `UDP(dport=packet[UDP].sport, sport=packet[UDP].dport)`: Spoof the source and destination UDP ports.
     - `DNS(...)`: Use relevant fields like `id`, `qr`, `aa`, etc., to craft a valid DNS response.

6. **Send Spoofed Packet to Client:**
   - **Description:** Send the crafted response packet back to the client using Scapy's `send` function.
   - **Code Example:** 
     ```python
     send(spoofed_pkt, verbose=0)
     ```
   - **Explanation:** The `send` function sends the packet over the network. The `verbose=0` suppresses output.

7. **Handle No Response:**
   - **Description:** Print an error message if the `forward_dns_query` function returns `None`, indicating that the DNS request timed out or no response was received.
   - **Code Example:** 
     ```python
     else:
         query_name = packet[DNSQR].qname.decode('utf-8').strip('.')
         logging.error(f"Failed to receive DNS response from server for query {query_name}")
     ```
   - **Explanation:** This message can be customized to include the intended DNS server's IP or any other useful information.

### Packet Sniffing
- Use the `sniff` function to capture UDP packets on port 53 and pass each packet to `dns_interceptor`.
- Consider limiting sniffing to specific interfaces for controlled environments.
- **Code Example:** 
   ```python
   sniff(filter="udp port 53", prn=dns_interceptor)
   ```
