from spinn_front_end_common.abstract_models.impl.\
    provides_key_to_atom_mapping_impl \
    import ProvidesKeyToAtomMappingImpl
from spinn_front_end_common.abstract_models.\
    abstract_send_me_multicast_commands_vertex \
    import AbstractSendMeMulticastCommandsVertex

from pacman.model.decorators.overrides import overrides

from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .abstract_ethernet_sensor import AbstractEthernetSensor
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_ethernet.push_bot_translator import PushBotTranslator
from spynnaker_external_devices_plugin.pyNN.connections\
    .push_bot_wifi_connection import get_pushbot_wifi_connection
from spynnaker_external_devices_plugin.pyNN.connections\
    .push_bot_retina_connection import PushBotRetinaConnection


class PushBotEthernetRetinaDevice(
        AbstractSendMeMulticastCommandsVertex, ProvidesKeyToAtomMappingImpl,
        AbstractEthernetSensor):

    def __init__(
            self, protocol, resolution, pushbot_ip_address, pushbot_port=56000,
            injector_port=None, local_host=None, local_port=None,
            retina_injector_label="PushBotRetinaInjector"):
        ProvidesKeyToAtomMappingImpl.__init__(self)
        self._protocol = protocol
        pushbot_wifi_connection = get_pushbot_wifi_connection(
            pushbot_ip_address, pushbot_port)
        self._translator = PushBotTranslator(protocol, pushbot_wifi_connection)
        self._resolution = resolution
        self._injector_port = injector_port
        self._retina_injector_label = retina_injector_label

        self._database_connection = PushBotRetinaConnection(
            self._retina_injector_label, pushbot_wifi_connection,
            local_host, local_port)

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.start_resume_commands)
    def start_resume_commands(self):

        commands = list()

        # add mode command if not done already
        if not self._protocol.sent_mode_command():
            commands.append(self._protocol.set_mode())

        # device specific commands
        commands.append(self._protocol.disable_retina())
        commands.append(self._protocol.set_retina_transmission(
            retina_key=self._resolution.value))

        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.pause_stop_commands)
    def pause_stop_commands(self):
        commands = list()
        commands.append(self._protocol.disable_retina())
        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.timed_commands)
    def timed_commands(self):
        return []

    @overrides(AbstractEthernetSensor.get_n_neurons)
    def get_n_neurons(self):
        return self._resolution.value.n_neurons

    @overrides(AbstractEthernetSensor.get_injector_parameters)
    def get_injector_parameters(self):
        return {"port": self._injector_port}

    @overrides(AbstractEthernetSensor.get_injector_label)
    def get_injector_label(self):
        return self._retina_injector_label

    @overrides(AbstractEthernetSensor.get_translator)
    def get_translator(self):
        return self._translator

    @overrides(AbstractEthernetSensor.get_database_connection)
    def get_database_connection(self):
        return self._database_connection
