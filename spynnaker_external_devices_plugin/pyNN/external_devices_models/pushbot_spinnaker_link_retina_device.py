# spinn front end common imports
from spinn_front_end_common.abstract_models.\
    abstract_provides_outgoing_partition_constraints import \
    AbstractProvidesOutgoingPartitionConstraints
from spinn_front_end_common.utility_models.multi_cast_command \
    import MultiCastCommand

# pynn imports
from spynnaker.pyNN.models.abstract_models\
    .abstract_send_me_multicast_commands_vertex \
    import AbstractSendMeMulticastCommandsVertex
from spynnaker.pyNN.exceptions import SpynnakerException

# pacman imports
from pacman.model.constraints.key_allocator_constraints\
    .key_allocator_fixed_key_and_mask_constraint \
    import KeyAllocatorFixedKeyAndMaskConstraint
from pacman.model.decorators.overrides import overrides
from pacman.model.routing_info.base_key_and_mask import BaseKeyAndMask
from pacman.model.graphs.application.application_spinnaker_link_vertex \
    import ApplicationSpiNNakerLinkVertex


# general imports
from collections import namedtuple
from enum import Enum, IntEnum

# Named tuple bundling together configuration elements of a pushbot resolution
# config
PushBotRetinaResolutionConfig = namedtuple("PushBotRetinaResolution",
                                           ["pixels", "enable_command",
                                            "coordinate_bits"])

PushBotRetinaResolution = Enum(
    value="PushBotRetinaResolution",
    names=[("Native128", PushBotRetinaResolutionConfig(128, (1 << 26), 7)),
           ("Downsample64", PushBotRetinaResolutionConfig(64, (2 << 26), 6)),
           ("Downsample32", PushBotRetinaResolutionConfig(32, (3 << 26), 5)),
           ("Downsample16", PushBotRetinaResolutionConfig(16, (4 << 26), 4))])

PushBotRetinaPolarity = IntEnum(
    value="PushBotRetinaPolarity",
    names=["Up", "Down", "Merged"])


class PushBotRetinaDevice(ApplicationSpiNNakerLinkVertex,
                          AbstractSendMeMulticastCommandsVertex,
                          AbstractProvidesOutgoingPartitionConstraints):

    # Mask for all SpiNNaker->Pushbot commands
    MANAGEMENT_MASK = 0xFFFFF800

    # Retina-specific commands
    RETINA_ENABLE = 0x1
    RETINA_DISABLE = 0x0
    RETINA_KEY_SET = 0x2
    RETINA_NO_TIMESTAMP = (0 << 29)

    # Sensor commands
    SENSOR = 0x7F0
    SENSOR_SET_KEY = 0x0
    SENSOR_SET_PUSHBOT = 0x1

    def __init__(
            self, fixed_key, spinnaker_link_id, label=None, n_neurons=None,
            polarity=PushBotRetinaPolarity.Merged,
            resolution=PushBotRetinaResolution.Downsample64,
            board_address=None, command_sender_top_bits_key=0x00000000):

        # Validate number of timestamp bytes
        if not isinstance(polarity, PushBotRetinaPolarity):
            raise SpynnakerException(
                "Pushbot retina polarity should be one of those defined in"
                " Polarity enumeration")
        if not isinstance(resolution, PushBotRetinaResolution):
            raise SpynnakerException(
                "Pushbot retina resolution should be one of those defined in"
                " Resolution enumeration")

        # Cache resolution
        self._resolution = resolution

        # Build standard routing key from virtual chip coordinates
        self._routing_key = fixed_key
        self._retina_source_key = self._routing_key

        # Calculate number of neurons
        fixed_n_neurons = resolution.value.pixels ** 2

        # If polarity is merged
        if polarity == PushBotRetinaPolarity.Merged:
            # Double number of neurons
            fixed_n_neurons *= 2

            # We need to mask out two coordinates and a polarity bit
            mask_bits = (2 * resolution.value.coordinate_bits) + 1
        # Otherwise
        else:
            # We need to mask out two coordinates
            mask_bits = 2 * resolution.value.coordinate_bits

            # If polarity is up, set polarity bit in routing key
            if polarity == PushBotRetinaPolarity.Up:
                polarity_bit = 1 << (2 * resolution.value.coordinate_bits)
                self._routing_key |= polarity_bit

        # Build routing mask
        self._routing_mask = ~((1 << mask_bits) - 1) & 0xFFFFFFFF

        ApplicationSpiNNakerLinkVertex.__init__(
            self, n_atoms=fixed_n_neurons, spinnaker_link_id=spinnaker_link_id,
            max_atoms_per_core=fixed_n_neurons, label=label,
            board_address=board_address)
        self._commands = self._get_commands(command_sender_top_bits_key)
        AbstractProvidesOutgoingPartitionConstraints.__init__(self)

        if n_neurons != fixed_n_neurons and n_neurons is not None:
            print "Warning, the retina will have {} neurons".format(
                fixed_n_neurons)

    def get_outgoing_partition_constraints(self, partition):
        return [KeyAllocatorFixedKeyAndMaskConstraint(
            [BaseKeyAndMask(self._routing_key, self._routing_mask)])]

    def _get_commands(self, command_top_bits_key):
        """
        method that returns the commands for the retina external device
        """
        # Set sensor key
        commands = list()
        commands.append(MultiCastCommand(
            0, (command_top_bits_key | PushBotRetinaDevice.SENSOR |
                PushBotRetinaDevice.SENSOR_SET_KEY),
            self._retina_source_key, 1, 100))

        # Set sensor to pushbot
        commands.append(MultiCastCommand(
            0, (command_top_bits_key | PushBotRetinaDevice.SENSOR |
                PushBotRetinaDevice.SENSOR_SET_PUSHBOT), 1, 1, 100))

        # Ensure retina is disabled
        commands.append(MultiCastCommand(
            0, (command_top_bits_key | PushBotRetinaDevice.RETINA_DISABLE),
            0, 1, 100))

        # Set retina key
        commands.append(MultiCastCommand(
            0, (command_top_bits_key | PushBotRetinaDevice.RETINA_KEY_SET),
            self._retina_source_key, 1, 100))

        # Enable retina
        commands.append(MultiCastCommand(
            0, (command_top_bits_key | PushBotRetinaDevice.RETINA_ENABLE),
            (PushBotRetinaDevice.RETINA_NO_TIMESTAMP +
             self._resolution.value.enable_command),
            1, 100))

        # At end of simulation, disable retina
        commands.append(MultiCastCommand(
            -1, (command_top_bits_key | PushBotRetinaDevice.RETINA_DISABLE),
            0, 1, 100))

        return commands

    @property
    @overrides(AbstractSendMeMulticastCommandsVertex.commands)
    def commands(self):
        return self._commands

    @property
    def model_name(self):
        return "pushbot retina device"
