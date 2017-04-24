from pacman.model.decorators.overrides import overrides
from spinn_front_end_common.abstract_models. \
    abstract_send_me_multicast_commands_vertex \
    import AbstractSendMeMulticastCommandsVertex
from spinn_front_end_common.abstract_models.impl. \
    provides_key_to_atom_mapping_impl import \
    ProvidesKeyToAtomMappingImpl
from spinn_front_end_common.utilities.exceptions import ConfigurationException
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot \
    .push_bot_ethernet.push_bot_ethernet_device import PushBotEthernetDevice
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot.push_bot_parameters.push_bot_speaker import \
    PushBotSpeaker


class PushBotEthernetSpeakerDevice(
        AbstractSendMeMulticastCommandsVertex, ProvidesKeyToAtomMappingImpl,
        PushBotEthernetDevice):
    """ The Speaker of a PushBot
    """

    def __init__(
            self, speaker, protocol, start_active_time=0,
            start_total_period=0, start_frequency=0, start_melody=None,
            timesteps_between_send=None):
        """

        :param speaker: The PushBotSpeaker value to control
        :param protocol: The protocol instance to get commands from
        :param start_active_time: The "active time" to set at the start
        :param start_total_period: The "total period" to set at the start
        :param start_frequency: The "frequency" to set at the start
        :param start_melody: The "melody" to set at the start
        :param timesteps_between_send:\
            The number of timesteps between sending commands to the device,\
            or None to use the default
        """
        if not isinstance(speaker, PushBotSpeaker):
            raise ConfigurationException(
                "speaker parameter must be a PushBotSpeaker value")

        ProvidesKeyToAtomMappingImpl.__init__(self)
        PushBotEthernetDevice.__init__(
            self, protocol, speaker, True, timesteps_between_send)

        # protocol specific data items
        self._command_protocol = protocol
        self._start_active_time = start_active_time
        self._start_total_period = start_total_period
        self._start_frequency = start_frequency
        self._start_melody = start_melody

    def set_command_protocol(self, command_protocol):
        self._command_protocol = command_protocol

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.start_resume_commands)
    def start_resume_commands(self):
        commands = list()

        # add mode command if not done already
        if not self.protocol.sent_mode_command():
            commands.append(self.protocol.set_mode())

        # device specific commands
        commands.append(
            self._command_protocol.push_bot_speaker_config_total_period(
                total_period=self._start_total_period))
        commands.append(
            self._command_protocol.push_bot_speaker_config_active_time(
                active_time=self._start_active_time))
        if self._start_frequency is not None:
            commands.append(self._command_protocol.push_bot_speaker_set_tone(
                frequency=self._start_frequency))
        if self._start_melody is not None:
            commands.append(self._command_protocol.push_bot_speaker_set_melody(
                melody=self._start_melody))
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.pause_stop_commands)
    def pause_stop_commands(self):
        commands = list()
        commands.append(
            self._command_protocol.push_bot_speaker_config_total_period(
                total_period=0))
        commands.append(
            self._command_protocol.push_bot_speaker_config_active_time(
                active_time=0))
        commands.append(self._command_protocol.push_bot_speaker_set_tone(
            frequency=0))
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.timed_commands)
    def timed_commands(self):
        return []
