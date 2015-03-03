from enum import Enum

from data_specification.data_specification_generator \
    import DataSpecificationGenerator
from pacman.model.constraints.key_allocator_constraints\
    .key_allocator_routing_constraint import KeyAllocatorRoutingConstraint
from pacman.model.partitionable_graph.abstract_partitionable_vertex \
    import AbstractPartitionableVertex
from pacman.model.constraints.tag_allocator_constraints \
    .tag_allocator_require_reverse_iptag_constraint \
    import TagAllocatorRequireReverseIptagConstraint
from pacman.model.constraints.placer_constraints\
    .placer_radial_placement_from_chip_constraint \
    import PlacerRadialPlacementFromChipConstraint
from spynnaker.pyNN.models.abstract_models.abstract_data_specable_vertex \
    import AbstractDataSpecableVertex
from spynnaker.pyNN import exceptions
from spynnaker.pyNN.utilities import constants
from spinnman.messages.eieio.eieio_prefix_type import EIEIOPrefixType
import math


class ReverseIpTagMultiCastSource(AbstractPartitionableVertex,
                                  AbstractDataSpecableVertex):

    # internal params
    _SPIKE_INJECTOR_REGIONS = Enum(
        value="SPIKE_INJECTOR_REGIONS",
        names=[('SYSTEM', 0),
               ('CONFIGURATION', 1)])

    _CONFIGURATION_REGION_SIZE = 28
    _max_atoms_per_core = 2048

    CORE_APP_IDENTIFIER = constants.SPIKE_INJECTOR_CORE_APPLICATION_ID

    def __init__(self, n_neurons, machine_time_step, timescale_factor,
                 spikes_per_second, ring_buffer_sigma, port,
                 label, board_address=None, virtual_key=None, check_key=True,
                 prefix=None, prefix_type=None, tag=None, key_left_shift=0,
                 sdp_port=1):

        AbstractDataSpecableVertex.__init__(
            self, n_neurons, label, machine_time_step,
            timescale_factor)
        AbstractPartitionableVertex.__init__(
            self, n_neurons, label,
            ReverseIpTagMultiCastSource._max_atoms_per_core)
        self.add_constraint(TagAllocatorRequireReverseIptagConstraint(
            port, sdp_port, board_address, tag))

        # set params
        self._host_port_number = port
        self._virtual_key = virtual_key
        self._prefix = prefix
        self._check_key = check_key
        self._prefix_type = prefix_type
        self._key_left_shift = key_left_shift

        # validate params
        if self._prefix is not None and self._prefix_type is None:
            raise exceptions.ConfigurationException(
                "To use a prefix, you must declaire which position to use the "
                "prefix in on the prefix_type parameter.")

        active_bits_of_mask = None
        if virtual_key is not None:
            self._mask, active_bits_of_mask = self._calculate_mask(n_neurons)

            # key =( key  ored prefix )and mask
            temp_vertial_key = virtual_key
            if self._prefix is not None:
                if temp_vertial_key is None:
                    temp_vertial_key = 0
                if self._prefix_type == EIEIOPrefixType.LOWER_HALF_WORD:
                    temp_vertial_key |= self._prefix
                if self._prefix_type == EIEIOPrefixType.UPPER_HALF_WORD:
                    temp_vertial_key |= (self._prefix << 16)
            else:
                if temp_vertial_key is None:
                    temp_vertial_key = 0

                if (self._prefix_type is None
                        or self._prefix_type
                        == EIEIOPrefixType.UPPER_HALF_WORD):
                    self._prefix = (self._virtual_key >> 16) & 0xFFFF
                elif self._prefix_type == EIEIOPrefixType.LOWER_HALF_WORD:
                    self._prefix = self._virtual_key & 0xFFFF

            if temp_vertial_key is not None:

                # check that mask key combo = key
                masked_key = temp_vertial_key & self._mask
                if self._virtual_key != masked_key:
                    raise exceptions.ConfigurationException(
                        "The mask calculated from your number of neurons has "
                        "the potential to interfere with the key, please "
                        "reduce the number of neurons or reduce the virtual "
                        "key")

                # check that neuron mask does not interfere with key
                if self._virtual_key < 0:
                    raise exceptions.ConfigurationException(
                        "Virtual keys must be positive")
                elif self._virtual_key == 0:
                    bits_of_key = 0
                else:
                    bits_of_key = int(math.ceil(math.log(
                                      self._virtual_key, 2)))
                if (32 - bits_of_key) < active_bits_of_mask:
                    raise exceptions.ConfigurationException(
                        "The mask calculated from your number of neurons has "
                        "the capability to interfere with the key due to its "
                        "size, please reduce the number of neurons or reduce "
                        "the virtual key")

                if self._key_left_shift > 16 or self._key_left_shift < 0:
                    raise exceptions.ConfigurationException(
                        "the key left shift must be within a range of 0"
                        " and 16. Please change this param and try again")

            # add routing constraint
            routing_key_constraint =\
                KeyAllocatorRoutingConstraint(self.generate_routing_info,
                                              self.get_key_with_neuron_id)
            self.add_constraint(routing_key_constraint)

        # add placement constraint
        placement_constraint = PlacerRadialPlacementFromChipConstraint(0, 0)
        self.add_constraint(placement_constraint)

    @staticmethod
    def _calculate_mask(n_neurons):
        temp_value = math.floor(math.log(n_neurons, 2))
        max_value = int(math.pow(2, 32))
        active_mask_bit_range = \
            int(math.log(int(math.pow(2, temp_value + 1)), 2)) + 1
        mask = max_value - int(math.pow(2, temp_value + 1))
        return mask, active_mask_bit_range

    def get_sdram_usage_for_atoms(self, vertex_slice, graph):

        # 3 words from the system region of the dsg/e,
        # 3 words for configuration and 6 *4 words for app pointer table
        return constants.SETUP_SIZE + self._CONFIGURATION_REGION_SIZE

    @property
    def model_name(self):
        return "ReverseIpTagMultiCastSource"

    def is_reverse_ip_tagable_vertex(self):
        return True

    def get_dtcm_usage_for_atoms(self, vertex_slice, graph):
        return self._CONFIGURATION_REGION_SIZE

    def get_binary_file_name(self):
        return 'reverse_iptag_multicast_source.aplx'

    def get_cpu_usage_for_atoms(self, vertex_slice, graph):
        return 1

    def generate_routing_info(self, subedge):
        """
        overloaded from component vertex
        """
        return self._virtual_key, self._mask

    def get_key_with_neuron_id(self, vertex_slice, vertex, placement, subedge):
        keys = dict()
        key, _ = self.generate_routing_info(None)
        for neuron_id in range(0, self._n_atoms):
            keys[neuron_id] = key
        return keys

    def generate_data_spec(self, subvertex, placement, sub_graph, graph,
                           routing_info, hostname, graph_mapper,
                           report_folder, ip_tags, reverse_ip_tags):
        # Create new DataSpec for this processor:
        data_writer, report_writer = \
            self.get_data_spec_file_writers(
                placement.x, placement.y, placement.p, hostname, report_folder)

        spec = DataSpecificationGenerator(data_writer, report_writer)

        spec.comment("\n*** Spec for block of {} neurons ***\n"
                     .format(self.model_name))

        spec.comment("\nReserving memory space for data regions:\n\n")

        # Reserve memory regions:
        spec.reserve_memory_region(
            region=self._SPIKE_INJECTOR_REGIONS.SYSTEM.value,
            size=constants.SETUP_SIZE, label='SYSTEM')
        spec.reserve_memory_region(
            region=self._SPIKE_INJECTOR_REGIONS.CONFIGURATION.value,
            size=self._CONFIGURATION_REGION_SIZE, label='CONFIGURATION')

        # set up system region writes
        self._write_basic_setup_info(
            spec, ReverseIpTagMultiCastSource.CORE_APP_IDENTIFIER)

        # set up configuration region writes
        spec.switch_write_focus(
            region=self._SPIKE_INJECTOR_REGIONS.CONFIGURATION.value)

        if self._virtual_key is None:
            subedge_routing_info = \
                routing_info.get_subedge_information_from_subedge(
                    sub_graph.outgoing_subedges_from_subvertex(subvertex)[0])
            self._mask = subedge_routing_info.mask
            self._virtual_key = subedge_routing_info.key

        # add prefix boolean value
        if self._prefix is None:
            spec.write_value(data=0)
        else:
            spec.write_value(data=1)

        # add prefix
        if self._prefix is None:
            spec.write_value(data=0)
        else:
            if self._prefix_type is EIEIOPrefixType.LOWER_HALF_WORD:
                spec.write_value(data=self._prefix)
            else:
                spec.write_value(data=self._prefix << 16)

        # key left shift
        spec.write_value(data=self._key_left_shift)

        # add key check
        if self._check_key:
            spec.write_value(data=1)
        else:
            spec.write_value(data=0)

        # add key and mask
        spec.write_value(data=self._virtual_key)
        spec.write_value(data=self._mask)

        # close spec
        spec.end_specification()
        data_writer.close()
