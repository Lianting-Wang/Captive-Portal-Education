## Guide for Switch Implementation

- **Objective**: Implement a LearningSwitch class that handles packet_in events by following the provided algorithm.
- **POX Framework Basics**:
  - Understand the relationship between events (like packet_in) and how your class should respond to them.
  - Get familiar with using the POX API for sending packets and interacting with the switch's flow table.
- **Understanding the Concept of a Switch**:
  - Understand the algorithmic basis of the switch and try to implement it using code.
- **Components**:
  - **`macToPort`**: A dictionary for learning source addresses and their ports.
  - **`_handle_PacketIn`**: Functions to analyze packets and make forwarding decisions based on the algorithm steps.
  - **`forward_packet`**: Methodology to send flow mod messages for known destinations.

###  Introduction to POX Framework

**What is POX?**
- POX is an open-source development platform for Python-based software-defined networking (SDN) controllers. It helps in managing network flow control and allows for rapid development and testing of new network protocols.

**Why use POX?**
- POX provides a flexible toolset that allows programmers to react to network events, automate tasks, and manage network behavior dynamically.

#### Understanding Events in POX

**What are Events?**
- In the context of the POX framework, events are notifications that something has occurred in the network, such as a new device connection or data packets needing routing decisions.

**Types of Events**
- **packet_in**: This event is triggered when a switch receives a packet that it does not know how to handle, and it needs instructions from the POX controller on what to do with the packet.

**Responding to Events**
- Your controller class should have methods to handle these events. For instance, the `packet_in` handler will typically check the type of packet and decide whether to forward it, drop it, or take another action.

#### Working with the POX API

##### Key Functions and Types

- **`of.ofp_packet_out()`**
    - **Purpose**: This function creates an OpenFlow packet-out message. Packet-out messages are used by the controller to instruct a switch to send a packet through a specific port or ports. This function is vital for implementing actions like forwarding a packet to its destination or flooding a packet across the network.
    - **Return Type**: An object of type `ofp_packet_out`, which can be populated with actions and data before being sent to the switch.

- **`of.ofp_flow_mod()`**
    - **Purpose**: The `of.ofp_flow_mod()` function is used to modify the flow table in an OpenFlow switch. This function is crucial for defining how switches handle packets based on predefined rules. By using this function, the controller can add, update, or delete flow entries in the switch. This allows for sophisticated management of network traffic, enabling actions such as routing, blocking, or even prioritizing certain types of packets without requiring further intervention from the controller for each packet.
    - **Return Type**: An object of type `ofp_flow_mod`, which contains several fields that define the flow entry's properties and actions. This object can be customized with match criteria, instructions, priorities, and timeouts before being sent to the switch.

- **`of.ofp_action_output()`**
    - **Purpose**: This function creates an action that can be attached to an `ofp_packet_out` message, specifying that the packet should be output through a particular port. This action is used both for forwarding packets to a specific port based on the MAC learning table and for flooding packets (by specifying a special flood port).
    - **Parameters**:
      - `port`: The port number through which the packet should be sent. Use `of.OFPP_FLOOD` for flooding the packet to all ports except the source port.
    - **Return Type**: An `ofp_action_output` object, representing the output action.

- **`Connection.send()`**
    - **Purpose**: Sends an OpenFlow message (like `ofp_packet_out`) from the controller to the switch. This method is called on the switch connection object, which is available in the event handler (e.g., `self.connection.send(msg)`).
    - **Parameters**:
      - The OpenFlow message to send, such as an `ofp_packet_out` message populated with actions and data.
    - **Important**: The argument to `send()` must be an OpenFlow message object. The type of this object depends on the specific action you're taking (e.g., `ofp_packet_out`, `ofp_flow_mod`).

**Key Functions of the POX API**
- **Sending Packets**: Use `ofp_packet_out` function to send packets through the network.
- **Interacting with the Flow Table**: Use `ofp_flow_mod` function to add entries to the switch’s flow table, which determines how packets should be handled in the future.

**Practical Examples**
1. **Handling a packet_in Event**
   ```python
   def _handle_PacketIn (self, event):
       packet = event.parsed  # Parse incoming packet
       if not packet.parsed:
           print("Ignoring incomplete packet")
           return

       packet_in = event.ofp  # The actual ofp_packet_in message.
       # Further processing
   ```
2.  **Forwarding a Packet**
    ```python
    def forward_packet(self, packet, port):
        msg = of.ofp_packet_out()  # Create a packet-out message
        action = of.ofp_action_output(port=port)  # Specify forwarding action
        msg.actions.append(action)  # Attach action to the message
        msg.data = packet  # Attach the original packet data
        self.connection.send(msg)  # Send the message to the switch
    ```
3.  **Adding a Flow**
    ```python
    def add_flow(self, src_port, dst_port, actions, data=None):
        msg = of.ofp_flow_mod()  # Create a new flow modification message
        msg.match = of.ofp_match.from_packet(packet, event.port)  # Match the packet using the packet and port information
        msg.idle_timeout = 1  # Set the idle timeout (seconds before idle flows are removed)
        msg.hard_timeout = 3  # Set the hard timeout (seconds before flows are removed, regardless of activity)
        msg.actions.append(of.ofp_action_output(port = port))  # Add an action to output packets to the specified port
        msg.data = event.ofp  # Attach the original packet data
        self.connection.send(msg)  # Send the flow modification message to the switch
    ```

### Understanding the Concept of a Switch

A switch operates at the Data Link layer (Layer 2) of the OSI model. It uses MAC addresses to forward data to the correct destination. Initially, a switch does not know the MAC addresses on the network. It learns these by examining the source MAC address of incoming frames. If the destination MAC address of a frame is unknown, the switch floods the frame to all ports except the one it arrived on. Over time, it builds a MAC address table that maps MAC addresses to ports, allowing it to efficiently forward traffic.

The steps below outlines the basic logic a learning switch implements to learn MAC addresses and make forwarding decisions based on its learning table (also known as a MAC address table or forwarding database). This process helps in minimizing the broadcast traffic by ensuring that packets are only sent through the port leading to the destination device.

1. Update the address/port table using the packet's source address and the switch port.

2. If the packet's transmission is not transparent (`transparent = False`) and it meets one of the following criteria: the Ethertype is LLDP or the destination address is a Bridge Filtered address, then the packet should be dropped. This step prevents the forwarding of link-local traffic, such as LLDP and 802.1x.

3. Check if the packet is destined for a multicast address. If so, the packet should be broadcasted to all ports (flooded).

4. If the destination address does not have a corresponding port in the address/port table, the packet should also be flooded to all ports.

5. Prevent loopback by checking if the packet's output port matches the input port. If they are the same, drop the packet and any similar ones temporarily.

6. Finally, for efficient routing, add a flow table entry in the switch to ensure future packets of this flow are directed to the correct port. Then, dispatch the packet through the designated port.

By structuring the process in this manner, repetition is minimized, and the flow of actions is clearly outlined.

#### Explanation and Practical Implementation

1. Update Address/Port Table
    - **Functionality**: Maintain a table where each entry maps a MAC address to a switch port. When a packet arrives, update this table with the source MAC address and the port it was received on.
    - **Implementation Tip**: Use a Python dictionary where keys are source MAC addresses and values are the ports.

2. Handle Special Packets
    - **Functionality**: Drop specific packets such as LLDP or packets destined to a Bridge Filtered address if `transparent` is False. These packets are usually not meant to be forwarded by switches.
    - **Implementation Tip**: Implement a check for the Ethertype and destination address. If the conditions match, simply drop the packet.

3. Handle Multicast Destination
    - **Functionality**: If the packet is destined for a multicast address, flood it to all ports except the incoming port.
    - **Implementation Tip**: Use a function to send the packet out through all ports except the source port.

4. Flooding if Destination Unknown
    - **Functionality**: If the destination MAC address is not in the address/port table, flood the packet.
    - **Implementation Tip**: This is similar to handling multicast but triggered by a different condition (unknown destination).

5. Avoiding Packet Loops
    - **Functionality**: If the port where the packet needs to be forwarded is the same as the port where it was received, drop the packet to avoid loops.
    - **Implementation Tip**: A simple if-check will suffice here.

6. Installing Flow Table Entries
    - **Functionality**: For known destinations, install a flow in the switch to directly forward future packets to the appropriate port without involving the controller.
    - **Implementation Tip**: This requires interacting with the switch's flow table through the OpenFlow protocol. Use POX's API to send flow mod messages to the switch.

### Guide to Creating a Conditional Switch for Captive Portals

#### Objective
The objective of this guide is to help you implement a conditional switch that forwards traffic based on specific conditions involving MAC addresses and their validation using a TCP client.

#### Understanding the Problem
Before modifying the switch code, it's crucial to understand the requirements:
- You need to ensure that traffic to/from the captive portal and the internet is handled based on MAC address validation.
- The switch needs to differentiate between packets from the captive portal, the internet, and other sources, and handle each case appropriately.


#### Step-by-Step Guide

1. **Analyze the Existing Code**
   - Study the existing `LearningSwitch` code to understand how it currently handles packet forwarding.
   - Pay special attention to the `set_mod` function as it is the focus of the modification.

2. **Understand the Role of MAC Addresses**
   - **Captive Portal MAC:** Traffic originating from this MAC indicates packets from the captive portal.
   - **Internet MAC:** Traffic from this MAC should generally be forwarded to any destination that is not the captive portal.
   - **Other MACs:** Traffic from other sources needs to be validated before forwarding.

3. **Determine Conditions to Handle**
   - The following conditions should guide how packets are treated:
     - **Traffic from the Captive Portal:** If the packet is from the captive portal:
       - Allow packets to pass if they are destined for the internet.
       - Otherwise, drop packets if the destination MAC passes validation.

     - **Traffic from the Internet:** If the packet is from the internet:
       - Allow packets to pass if they are destined for the captive portal.
       - Otherwise, drop packets if the destination MAC does not pass validation.

     - **Traffic from Other MACs:** If the packet is from any other MAC address:
       - Validate the source MAC address using the TCP client.
       - If validated, forward traffic to the internet.
       - Otherwise, forward traffic to the captive portal.

     ![Flowchart of Conditional Switch](https://github.com/Lianting-Wang/Captive-Portal-Education/raw/main/diagrams/Conditional%20Switch.svg)

4. **Define Actions for Each Condition**
   - Translate the conditions into logical actions:
     - **Set Up Flow Modifications:** When the conditions are met for forwarding packets, configure the switch using flow modifications.
       - For example, use `set_mod(port)` to forward traffic to the appropriate port.

     - **Drop Packets:** In conditions where traffic should not be forwarded, use the `drop()` function to drop the packet.

5. **Implement the Modifications**
   - In the `LearningSwitch` class, modify the `_handle_PacketIn` function:
     - Carefully handle each condition and make sure you understand the intended forwarding behavior.
