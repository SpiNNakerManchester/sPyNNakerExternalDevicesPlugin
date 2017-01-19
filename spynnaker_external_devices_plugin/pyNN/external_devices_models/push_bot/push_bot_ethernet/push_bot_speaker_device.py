
# pynn imports
from spinn_front_end_common.abstract_models.impl.\
    provides_key_to_atom_mapping_impl import \
    ProvidesKeyToAtomMappingImpl
from spinn_front_end_common.abstract_models.\
    abstract_send_me_multicast_commands_vertex \
    import AbstractSendMeMulticastCommandsVertex
from spinn_front_end_common.utilities import exceptions
from spynnaker_external_devices_plugin.pyNN.protocols.\
    munich_io_spinnaker_link_protocol import MunichIoSpiNNakerLinkProtocol
from pacman.model.decorators.overrides import overrides

UART_ID = 0


class PushBotSpeakerDevice(
        AbstractSendMeMulticastCommandsVertex, ProvidesKeyToAtomMappingImpl):

    def __init__(
            self, uart_id=0, start_active_time=0,
            start_total_period=0, start_frequency=None, melody_value=None,
            command_sender_protocol=None):

        # munich protocol
        self._control_module_protocol = MunichIoSpiNNakerLinkProtocol(
            mode=MunichIoSpiNNakerLinkProtocol.MODES.PUSH_BOT)
        if command_sender_protocol is None:
            self._protocol = self._control_module_protocol
        else:
            self._protocol = command_sender_protocol

        # protocol specific data items
        self._uart_id = uart_id
        self._start_active_time = start_active_time
        self._start_total_period = start_total_period
        self._start_frequency = start_frequency
        self._melody_value = melody_value

        ProvidesKeyToAtomMappingImpl.__init__(self)

        if self._start_frequency is None and self._melody_value is None:
            raise exceptions.ConfigurationException(
                "you must set a frequency or a melody value as start up "
                "state.")
        if (self._start_frequency is not None and
                self._melody_value is not None):
            raise exceptions.ConfigurationException(
                "you must select a frequency or a melody value as start up "
                "state. Not both")

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.start_resume_commands)
    def start_resume_commands(self):
        commands = list()

        # add mode command if not done already
        if not self._protocol.sent_mode_command():
            commands.append(self._protocol.get_set_mode_command())

        # device specific commands
        commands.append(self._protocol.push_bot_speaker_config_total_period(
            total_period=self._start_total_period, uart_id=self._uart_id))
        commands.append(self._protocol.push_bot_speaker_config_active_time(
            active_time=self._start_active_time, uart_id=self._uart_id))
        if self._start_frequency is not None:
            commands.append(self._protocol.push_bot_speaker_set_tone(
                frequency=self._start_frequency, uart_id=self._uart_id))
        if self._melody_value is not None:
            commands.append(self._protocol.push_bot_speaker_set_melody(
                melody=self._melody_value, uart_id=self._uart_id))
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.pause_stop_commands)
    def pause_stop_commands(self):
        commands = list()
        commands.append(self._protocol.push_bot_speaker_config_total_period(
            total_period=0, uart_id=self._uart_id))
        commands.append(self._protocol.push_bot_speaker_config_active_time(
            active_time=0, uart_id=self._uart_id))
        if self._start_frequency is not None:
            commands.append(self._protocol.push_bot_speaker_set_tone(
                frequency=0, uart_id=self._uart_id))
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.timed_commands)
    def timed_commands(self):
        return []

    @property
    def melody_key(self):
        return self._control_module_protocol.push_bot_speaker_set_melody(
            melody=0, uart_id=self._uart_id).key

    @property
    def frequency_key(self):
        return self._control_module_protocol.push_bot_speaker_set_tone(
            frequency=0, uart_id=self._uart_id).key

    @property
    def active_time_key(self):
        return self._control_module_protocol.\
            push_bot_speaker_config_active_time(
                active_time=0, uart_id=self._uart_id).key

    @property
    def total_period_key(self):
        return self._control_module_protocol.\
            push_bot_speaker_config_total_period(
                total_period=0, uart_id=self._uart_id).key

    @property
    def uart_id(self):
        return self._uart_id

    @property
    def protocol_instance_key(self):
        return self._control_module_protocol.instance_key

    @property
    def model_name(self):
        return "pushbot speaker device"
