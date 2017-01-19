
# pynn imports
from spinn_front_end_common.abstract_models.impl.\
    provides_key_to_atom_mapping_impl import \
    ProvidesKeyToAtomMappingImpl
from spinn_front_end_common.abstract_models.\
    abstract_send_me_multicast_commands_vertex \
    import AbstractSendMeMulticastCommandsVertex
from spynnaker_external_devices_plugin.pyNN.protocols.\
    munich_io_spinnaker_link_protocol import MunichIoSpiNNakerLinkProtocol
from pacman.model.decorators.overrides import overrides

UART_ID = 0


class PushBotMotorDevice(
        AbstractSendMeMulticastCommandsVertex, ProvidesKeyToAtomMappingImpl):

    n_motors = 0

    def __init__(self, motor_id=0, uart_id=0):

        # munich protocol
        self._protocol = MunichIoSpiNNakerLinkProtocol(
            mode=MunichIoSpiNNakerLinkProtocol.MODES.PUSH_BOT)

        self._motor_id = motor_id
        self._uart_id = uart_id
        self._this_motor_instance_id = PushBotMotorDevice.n_motors
        PushBotMotorDevice.n_motors += 1

        ProvidesKeyToAtomMappingImpl.__init__(self)

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.start_resume_commands)
    def start_resume_commands(self):
        commands = list()

        # add mode command if not done already
        if not self._protocol.sent_mode_command():
            commands.append(self._protocol.get_set_mode_command())

        # only the first motor instance needs to send the enable command
        if self._this_motor_instance_id == 0:
            # device specific commands
            commands.append(self._protocol.generic_motor_enable_disable(
                enable_disable=1, uart_id=self._uart_id))
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.pause_stop_commands)
    def pause_stop_commands(self):
        commands = list()

        # only the first motor instance needs to send the disable command
        if self._this_motor_instance_id == 0:
            commands.append(self._protocol.generic_motor_enable_disable(
                enable_disable=0, uart_id=self._uart_id))
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.timed_commands)
    def timed_commands(self):
        return []

    @property
    def uart_id(self):
        return self._uart_id

    @property
    def permanent_key(self):
        if self._motor_id == 0:
            return self._protocol.push_bot_motor_0_permanent(
                0, self._uart_id).key
        else:
            return self._protocol.push_bot_motor_1_permanent(
                0, self._uart_id).key

    @property
    def leaky_key(self):
        if self._motor_id == 0:
            return self._protocol.push_bot_motor_0_leaking_towards_zero(
                0, self._uart_id).key
        else:
            return self._protocol.push_bot_motor_1_leaking_towards_zero(
                0, self._uart_id).key

    @property
    def protocol_instance_key(self):
        return self._protocol.instance_key

    @property
    def enable_motor_key(self):
        return self._protocol.generic_motor_enable_disable(
            enable_disable=1, uart_id=self._uart_id).key

    @property
    def disable_motor_key(self):
        return self._protocol.generic_motor_enable_disable(
            enable_disable=0, uart_id=self._uart_id).key

    @property
    def model_name(self):
        return "push_bot_motor_device"
