from spinnman.connections.udp_packet_connections \
    import UDPIpAddressesConnection
from spinnman.messages.eieio.data_messages.specialized_message_types \
    import EIEIO32DataMessage
from spynnaker7 import config

udp_connection = UDPIpAddressesConnection(
    remote_host=config.get("Machine", "machineName"), remote_port=12345)

key = 0x70800
# key = 0x800
payload = 1


message = EIEIO32DataMessage()
message.add_key(key)
udp_connection.send_eieio_message(message)
