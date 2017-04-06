from enum import Enum
from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol
from data_specification.enums.data_type import DataType


class PushBotLED(Enum):

    LED_TOTAL_PERIOD = (
        0, MunichIoSpiNNakerLinkProtocol.push_bot_led_total_period_key,
        0, DataType.S1615.max, 20
    )

    LED_FRONT_ACTIVE_TIME = (
        1, MunichIoSpiNNakerLinkProtocol.push_bot_led_front_active_time_key,
        0, DataType.S1615.max, 20
    )

    LED_BACK_ACTIVE_TIME = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_led_back_active_time_key,
        0, DataType.S1615.max, 20
    )

    LED_FREQUENCY = (
        3, MunichIoSpiNNakerLinkProtocol.push_bot_led_set_frequency_key,
        0, DataType.S1615.max, 20
    )

    def __new__(
            cls, value, protocol_property, min_value, max_value,
            time_between_send):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._protocol_property = protocol_property
        obj._min_value = min_value
        obj._max_value = max_value
        obj._time_between_send = time_between_send
        return obj

    @property
    def protocol_property(self):
        return self._protocol_property

    @property
    def min_value(self):
        return self._min_value

    @property
    def max_value(self):
        return self._max_value

    @property
    def time_between_send(self):
        return self._time_between_send
