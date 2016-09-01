from pacman.model.constraints.partitioner_constraints.\
    partitioner_maximum_size_constraint import \
    PartitionerMaximumSizeConstraint
from pacman.model.graphs.application.impl.application_virtual_vertex import \
    ApplicationVirtualVertex


class ExternalCochleaDevice(ApplicationVirtualVertex):
    """ Cochlea device connected via spinnaker link
    """

    def __init__(
            self, n_neurons, spinnaker_link, label=None):
        ApplicationVirtualVertex.__init__(
            self, n_neurons, spinnaker_link, label,
            [PartitionerMaximumSizeConstraint(n_neurons)])
