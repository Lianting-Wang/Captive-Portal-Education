import configparser
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool
from pox.lib.addresses import EthAddr
from tcp_client import tcp_client

log = core.getLogger()

class LearningSwitch(object):
    def __init__(self, connection, transparent):
        # Switch connection
        self.connection = connection
        self.transparent = transparent

        # Our MAC learning table
        self.macToPort = {}

        # Listen to the connection
        connection.addListeners(self)

        self.tcp_client = tcp_client()
        self.captive_portal_mac = EthAddr(self.tcp_client.get_host()['result'])
        self.internet_mac = EthAddr(self.tcp_client.get_internet()['result'])

    def check_valid(self, source_mac):
        return self.tcp_client.check_valid(str(source_mac))['result']

    def _handle_PacketIn(self, event):
        """
        Handles incoming packets at the switch. This function learns the source MAC addresses and decides whether to forward or drop packets based on their destination and type.
        """

        packet = event.parsed

        response = EthAddr(self.tcp_client.get_host()['result'])
        if response and self.captive_portal_mac != response:
            self.captive_portal_mac = response

        def flood():
            """
            Floods the packet to all ports except the one it arrived on. This is typically used for multicast packets or when the destination is unknown.
            """
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)

        def drop():
            """
            Drops the packet, essentially ignoring the packet and taking no further action. Used for handling LLDP packets or if specific conditions require dropping the packet.
            """
            if event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                self.connection.send(msg)
        
        def set_mod(port):
            """
            Sets a flow table modification message to handle packets with similar characteristics in the future.
            This function effectively programs the switch to automatically handle similar incoming packets.
            Args:
                port: The output port where packets matching this flow should be sent.
            """
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.idle_timeout = 1
            msg.hard_timeout = 3
            msg.actions.append(of.ofp_action_output(port = port))
            msg.data = event.ofp
            self.connection.send(msg)

        self.macToPort[packet.src] = event.port

        if not self.transparent:
          if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
            drop()
            return

        if packet.dst.is_multicast:
            flood()
        else:
            pass

class l2_learning (object):
    def __init__ (self, transparent):
        core.openflow.addListeners(self)
        self.transparent = transparent

    def _handle_ConnectionUp(self, event):
        log.debug("Connection %s" % (event.connection,))
        LearningSwitch(event.connection, self.transparent)

def launch (transparent=False):
    core.registerNew(l2_learning, str_to_bool(transparent))
