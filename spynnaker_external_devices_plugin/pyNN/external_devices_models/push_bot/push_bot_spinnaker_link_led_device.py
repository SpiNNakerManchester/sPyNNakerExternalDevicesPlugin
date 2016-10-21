

# pynn imports
from spynnaker_external_devices_plugin.pyNN.external_devices_models.\
    push_bot.push_bot_led_device import \
    PushBotLEDDevice

from spynnaker_external_devices_plugin.pyNN.protocols.\
    munich_io_spinnaker_link_protocol import MunichIoSpiNNakerLinkProtocol

UART_ID = 0


class PushBotSpiNNakerLinkLEDDevice(PushBotLEDDevice):

    _N_LEDS = 0

    def __init__(
            self, spinnaker_link_id, uart_id=0, start_active_time=0,
            start_total_period=0, start_frequency=0, front_led=True,
            label=None, n_neurons=1,
            board_address=None):

        # munich protocol
        protocol = MunichIoSpiNNakerLinkProtocol(
            mode=MunichIoSpiNNakerLinkProtocol.MODES.PUSH_BOT)
        PushBotLEDDevice.__init__(
            self, spinnaker_link_id, uart_id, start_active_time,
            start_total_period, start_frequency, front_led,
            label, n_neurons, board_address, command_sender_protocol=protocol)
