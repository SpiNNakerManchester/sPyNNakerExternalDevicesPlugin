from enum import Enum
from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol


class PushBotMotor(Enum):

    MOTOR_0_PERMANENT = (
        0, MunichIoSpiNNakerLinkProtocol.push_bot_motor_0_permanent_key
    )

    MOTOR_0_LEAKY = (
        1,
        MunichIoSpiNNakerLinkProtocol.push_bot_motor_0_leaking_towards_zero_key
    )

    MOTOR_1_PERMANENT = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_motor_1_permanent_key
    )

    MOTOR_1_LEAKY = (
        3,
        MunichIoSpiNNakerLinkProtocol.push_bot_motor_1_leaking_towards_zero_key
    )

    def __new__(cls, value, prop, doc=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._prop_ = prop
        return obj

    @property
    def prop(self):
        return self._prop_
