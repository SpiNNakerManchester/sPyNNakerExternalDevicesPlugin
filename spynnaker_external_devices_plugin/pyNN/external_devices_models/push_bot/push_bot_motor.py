from enum import Enum
from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol


class PushBotMotor(Enum):

    MOTOR_0_PERMANENT = (
        0, MunichIoSpiNNakerLinkProtocol.push_bot_motor_0_permanent_key,
        -100, 100, 40
    )

    MOTOR_0_LEAKY = (
        1,
        (MunichIoSpiNNakerLinkProtocol
         .push_bot_motor_0_leaking_towards_zero_key),
        -100, 100, 40
    )

    MOTOR_1_PERMANENT = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_motor_1_permanent_key,
        -100, 100, 40
    )

    MOTOR_1_LEAKY = (
        3,
        (MunichIoSpiNNakerLinkProtocol
         .push_bot_motor_1_leaking_towards_zero_key),
        -100, 100, 40
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
