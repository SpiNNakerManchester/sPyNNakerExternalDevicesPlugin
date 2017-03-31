# general imports
from six import add_metaclass

# pacman imports
from pacman.model.graphs.application.application_fpga_vertex \
    import ApplicationFPGAVertex
from spinn_utilities.abstract_base import AbstractBase


@add_metaclass(AbstractBase)
class ArbitraryFPGADevice(ApplicationFPGAVertex):

    def __init__(
            self, n_neurons, fpga_link_id, fpga_id, board_address=None,
            label=None):
        ApplicationFPGAVertex.__init__(
            self, n_neurons, fpga_id, fpga_link_id, board_address, label)
