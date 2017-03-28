from pacman.model.graphs.application.impl.application_spinnaker_link_vertex \
    import ApplicationSpiNNakerLinkVertex


class ExternalCochleaDevice(ApplicationSpiNNakerLinkVertex):

    default_parameters = {
        'board_address': None, 'label': "ExternalCochleaDevice"}

    def __init__(
            self, n_neurons,
            spinnaker_link,
            label=default_parameters['label'],
            board_address=default_parameters['board_address']):
        ApplicationSpiNNakerLinkVertex.__init__(
            self, n_atoms=n_neurons, spinnaker_link_id=spinnaker_link,
            label=label, max_atoms_per_core=n_neurons,
            board_address=board_address)
