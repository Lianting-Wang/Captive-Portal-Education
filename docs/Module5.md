## Guide for Mininet Implementation

### Implementation Steps for Bash Script Creation

*Develop a bash script to handle network gateway switching based on connectivity. This involves using basic scripting skills and understanding network routes.*

#### Step 1: Define the Variables
- Start by defining the necessary variables:
  - `PRIMARY_GW`: This should hold the IP address of the primary gateway (internet gateway).
  - `SECONDARY_GW`: This should be the IP address of the secondary gateway (captive portal).
  - `CURRENT_GW`: To keep track of the currently used gateway. Initially, this should be set to the primary gateway.

**Example:**
```bash
PRIMARY_GW="192.168.1.1"  # Replace with actual IP from config
SECONDARY_GW="192.168.2.1"  # Replace with actual IP from config
CURRENT_GW="$PRIMARY_GW"
```

#### Step 2: Create an Infinite Loop
- Use a `while true; do` loop to continuously check the network status. This loop will ensure the script keeps running to monitor gateway connectivity.

#### Step 3: Check Connectivity
- Inside the loop, use a `ping` command to check if the primary gateway is reachable.
- You should attempt to ping the primary gateway (`ping -c 1 $PRIMARY_GW`).
- Redirect the output to `/dev/null` to keep the script output clean.

#### Step 4: Conditional Switching
- Implement an `if` statement to check the result of the ping command.
  - If the primary gateway is reachable (`if ping -c 1 $PRIMARY_GW &> /dev/null; then`), and if `CURRENT_GW` is not `PRIMARY_GW`, switch back to the primary gateway using `sudo ip route replace default via $PRIMARY_GW`.
  - If the ping fails (else clause), and if `CURRENT_GW` is not `SECONDARY_GW`, switch to the secondary gateway using `sudo ip route replace default via $SECONDARY_GW`.

#### Step 5: Add a Delay
- Use `sleep 1` at the end of the loop to pause the script for one second before the next iteration. This prevents the script from consuming too much CPU by continuously running the loop without pause.

#### Example Script:
```bash
#!/bin/bash

PRIMARY_GW="192.168.1.1"
SECONDARY_GW="192.168.2.1"
CURRENT_GW="$PRIMARY_GW"

while true; do
    if ping -c 1 $PRIMARY_GW &> /dev/null; then
        if [ "$CURRENT_GW" != "$PRIMARY_GW" ]; then
            echo "Switching back to primary gateway $PRIMARY_GW..."
            sudo ip route replace default via $PRIMARY_GW
            CURRENT_GW="$PRIMARY_GW"
        fi
    else
        if [ "$CURRENT_GW" != "$SECONDARY_GW" ]; then
            echo "Primary gateway not reachable. Switching to secondary gateway $SECONDARY_GW..."
            sudo ip route replace default via $SECONDARY_GW
            CURRENT_GW="$SECONDARY_GW"
        fi
    fi
    sleep 1
done
```

### Detailed Implementation Steps for Network Setup

*Complete the creation of the Mininet network by adding hosts and configuring network settings correctly. Pay attention to MAC and IP settings.*

#### Step 1: Adding a Controller
- **Objective**: Add a remote controller to the network which will manage all the switches.
- **Tasks**:
  1. Add a controller named `c0` using Mininet's `RemoteController` class.
  2. Understand the role of the controller in a Software Defined Network (SDN).

#### Step 2: Adding Switches
- **Objective**: Set up switches to create network segments.
- **Tasks**:
  1. Add two switches named `s1` and `s2`.
  2. Learn about the role of switches in the network and how they differ from hubs.

#### Step 3: Adding Hosts
- **Objective**: Configure and add hosts to the network.
- **Tasks**:
  1. Create a host that will act as the captive portal. Configure this host with a specific MAC and IP address as specified in the configuration file.
     - Use `net.addHost('host', mac=captive_portal_mac, ip=captive_portal_ip, defaultRoute=f'via {internet_ip}')`.
  2. Add two user hosts (`h1` and `h2`) without specific configurations for initial testing.
     - Use `net.addHost('h1')` and `net.addHost('h2')`.
  3. Understand IP addressing and why the captive portal needs a static IP and MAC address.

#### Step 4: Adding Internet Connectivity
- **Objective**: Simulate internet connectivity using a NAT.
- **Tasks**:
  1. Add a NAT to the network and configure it with an appropriate MAC and IP.
     - Use `internet = net.addNAT(name='internet', mac=internet_mac).configDefault()`.
  2. Learn about NAT (Network Address Translation) and its uses in a network.

#### Step 5: Creating Links
- **Objective**: Connect all network devices.
- **Tasks**:
  1. Connect both switches `s1` and `s2`.
     - Use `net.addLink(s1, s2)`.
  2. Connect the host, NAT, and switches appropriately.
     - Ensure the captive portal host and NAT are connected to `s1`.
     - Connect user hosts `h1` and `h2` to `s2`.
  3. Understand how physical links are simulated in Mininet and their impact on network topology.

#### Step 6: Starting the Network
- **Objective**: Initialize the network setup and start all services.
- **Tasks**:
  1. Start the network using `net.start()`.
  2. Discuss the sequence of operations that Mininet performs during the start operation, including controller-switch interactions and host configurations.

#### Step 7: Additional Configurations
- **Objective**: Perform final network configurations.
- **Tasks**:
  1. Configure the NAT device's IP settings.
     - Use commands like `internet.cmd('ifconfig internet-eth0 <IP> netmask <Netmask>')`.
  2. Deploy scripts and commands to configure network settings on hosts, especially for DNS resolution and gateway management.

#### Step 8: Monitoring and Testing
- **Objective**: Use Mininet CLI to test and debug the network setup.
- **Tasks**:
  1. Enter the Mininet CLI mode using `CLI(net)`.
  2. Perform tests like pinging between hosts, checking connectivity to the internet, and verifying the functionality of the captive portal.
  3. Learn how to troubleshoot common network issues within Mininet.

### Implementing and Starting Network Services

*Set up, run, and manage DNS and web server services within a Mininet environment as part of their captive portal project. This will practice managing network services and applications in a simulated network.*

#### Step 1: Setup DNS Server
    - **Script Preparation**: Ensure that the `dns_server.py` script is correctly set up to handle DNS requests. This script should include functionality to resolve domain names to IP addresses, specifically handling the redirection of certain requests to the captive portal page.
    - **Starting the DNS Server**:
        - Use the `cmd` method of a Mininet host object to start the DNS server in the background.
        - Command: `host.cmd('python dns_server.py &')`
        - This command starts the DNS server script in the background, allowing it to handle requests without blocking other commands.

#### Step 2: Web Server Setup
    - **Script Preparation**: The `web_server.py` script should be ready to serve web pages. Typically, this script will use a lightweight HTTP server framework like Flask or a simple HTTP server module provided by Python.
    - **Starting the Web Server**:
        - Similarly, use the `cmd` method to start the web server in the background.
        - Command: `host.cmd('python web_server.py &')`
        - This ensures that the web server starts and runs in the background, ready to serve the captive portal page or other necessary web resources.

#### Step 3: Log and Error Management
    - It's good practice to redirect the output of these services to log files for debugging purposes.
    - Example Commands:
        - `host.cmd('python dns_server.py > dns_server.log 2>&1 &')`
        - `host.cmd('python web_server.py > web_server.log 2>&1 &')`
    - These commands redirect the standard output (stdout) and standard error (stderr) to log files (`dns_server.log` and `web_server.log`), making it easier to troubleshoot any issues that arise.

#### Step 4: Verification
    - After starting the services, students should verify that both servers are running as expected.
    - They can check the processes or view the logs to confirm that the servers started without errors.

#### Step 5: Integrating with Mininet Startup
    - Include these commands in the appropriate place in your Mininet setup script (within the `customTree` function) to ensure that they are executed each time the network is initialized.

### Detailed Implementation Steps for Firewall Rules

*Configure iptables to redirect DNS, HTTP, and HTTPS traffic to specific ports handled by your DNS server and web server.*

#### Step 1: Understand iptables
Before writing the rules, students should familiarize themselves with how iptables works. iptables is a command-line firewall utility that allows you to define rules for controlling network traffic.

#### Step 2: Identify Traffic Types
   - **DNS traffic** generally uses port 53.
   - **HTTP traffic** uses port 80.
   - **HTTPS traffic** uses port 443.

#### Step 3: Write Rules for DNS Redirection
   - Objective: Redirect all DNS requests to the local DNS server running on port 53.
   - Rule: `iptables -t nat -A PREROUTING -i <interface> -p udp --dport 53 -j REDIRECT --to-port 53`
   - Explanation: This rule intercepts all UDP packets destined for port 53 (DNS) and redirects them to the same port on the local machine where the DNS server is expected to listen.

#### Step 4: Write Rules for HTTP and HTTPS Redirection
   - Objective: Redirect all HTTP and HTTPS traffic to local web servers, potentially running on different ports for captive portal functionality.
   - HTTP Rule: `iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 80 -j REDIRECT --to-port <custom_port>`
   - HTTPS Rule: `iptables -t nat -A PREROUTING -i <interface> -p tcp --dport 443 -j REDIRECT --to-port <custom_port>`
   - Explanation: These rules intercept all TCP packets destined for ports 80 (HTTP) and 443 (HTTPS) and redirect them to a specified port on the local machine. This port should be where the captive portal web server is listening.

#### Step 5: Specify the Network Interface
   - In the rules above, `<interface>` needs to be replaced with the network interface that the traffic will be coming from. This could be `eth0`, `eth1`, etc., depending on the network setup in Mininet.

#### Step 6: Testing the Rules
   - After setting the rules, students should test them to ensure that traffic is being redirected correctly. This can be done by trying to access external websites from the client hosts in the Mininet environment and observing if they are redirected to the captive portal.

#### Step 7: Persisting iptables Rules
   - Optionally, discuss how these rules can be made persistent across reboots, as by default, iptables rules are not saved after a reboot. This step is more relevant in a real-world setup than in a Mininet simulation.
