# pacman imports
from pacman.model.graphs.application.impl.application_fpga_vertex \
    import ApplicationFPGAVertex


class ArbitraryFPGADevice(ApplicationFPGAVertex):

    default_parameters = {
        'board_address': None, 'label': "ArbitraryFPGADevice"}

    def __init__(
            self, n_neurons, fpga_link_id, fpga_id,
            board_address=default_parameters['board_address'],
            label=default_parameters['label']):
        ApplicationFPGAVertex.__init__(
            self, n_neurons, fpga_id, fpga_link_id, board_address, label)
