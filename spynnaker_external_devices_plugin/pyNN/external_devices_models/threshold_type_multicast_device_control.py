from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter
from data_specification.enums.data_type import DataType
from spynnaker.pyNN.models.neuron.threshold_types.abstract_threshold_type \
    import AbstractThresholdType


class ThresholdTypeMulticastDeviceControl(AbstractThresholdType):
    """ A threshold type that can send multicast keys with the value of\
        membrane voltage as the payload
    """

    def __init__(self, keys, with_payload):
        AbstractThresholdType.__init__(self)
        self._keys = keys
        self._with_payload = [
            1 if is_with_payload else 0 for is_with_payload in with_payload
        ]

        print "keys =", self._keys
        print "pl   =", self._with_payload

    def get_n_threshold_parameters(self):
        return 2

    def get_threshold_parameters(self):
        return [
            NeuronParameter(self._keys, DataType.UINT32),
            NeuronParameter(self._with_payload, DataType.UINT32)
        ]

    def get_n_cpu_cycles_per_neuron(self):

        # Just a comparison, but 2 just in case!
        return 2
