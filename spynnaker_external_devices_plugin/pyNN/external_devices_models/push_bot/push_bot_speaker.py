from enum import Enum
from spynnaker_external_devices_plugin.pyNN\
    .protocols.munich_io_spinnaker_link_protocol \
    import MunichIoSpiNNakerLinkProtocol


class PushBotSpeaker(Enum):

    SPEAKER_TOTAL_PERIOD = (
        0,
        MunichIoSpiNNakerLinkProtocol.push_bot_speaker_config_total_period_key
    )

    SPEAKER_ACTIVE_TIME = (
        1,
        MunichIoSpiNNakerLinkProtocol.push_bot_speaker_config_active_time_key
    )

    SPEAKER_TONE = (
        2, MunichIoSpiNNakerLinkProtocol.push_bot_speaker_set_tone_key
    )

    SPEAKER_MELODY = (
        3, MunichIoSpiNNakerLinkProtocol.push_bot_speaker_set_melody_key
    )

    def __new__(cls, value, prop, doc=""):
        obj = object.__new__(cls)
        obj._value_ = value
        obj._prop_ = prop
        return obj

    @property
    def prop(self):
        return self._prop_
