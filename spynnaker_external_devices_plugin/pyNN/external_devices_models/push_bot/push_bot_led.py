from enum import Enum
from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol


class PushBotLED(Enum):

    LED_TOTAL_PERIOD = (
        0, MunichIoSpiNNakerLinkProtocol.push_bot_led_total_period_key
    )

    LED_FRONT_ACTIVE_TIME = (
        1, MunichIoSpiNNakerLinkProtocol.push_bot_led_front_active_time_key
    )

    LED_BACK_ACTIVE_TIME = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_led_back_active_time_key
    )

    LED_FREQUENCY = (
        3, MunichIoSpiNNakerLinkProtocol.push_bot_led_set_frequency_key
    )

    def __new__(cls, value, prop, doc=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._prop_ = prop
        return obj

    @property
    def prop(self):
        return self._prop_
