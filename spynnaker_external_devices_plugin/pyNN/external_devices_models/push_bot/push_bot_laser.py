from enum import Enum
from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol


class PushBotLaser(Enum):

    LASER_TOTAL_PERIOD = (
        0, MunichIoSpiNNakerLinkProtocol.push_bot_laser_config_total_period_key
    )

    LASER_ACTIVE_TIME = (
        1, MunichIoSpiNNakerLinkProtocol.push_bot_laser_config_active_time_key
    )

    LASER_FREQUENCY = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_laser_set_frequency_key
    )

    def __new__(cls, value, prop, doc=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._prop_ = prop
        return obj

    @property
    def prop(self):
        return self._prop_
