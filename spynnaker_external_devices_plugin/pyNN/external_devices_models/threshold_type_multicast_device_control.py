from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter
from data_specification.enums.data_type import DataType
from spynnaker.pyNN.models.neuron.threshold_types.abstract_threshold_type \
    import AbstractThresholdType


class ThresholdTypeMulticastDeviceControl(AbstractThresholdType):
    """ A threshold type that can send multicast keys with the value of\
        membrane voltage as the payload
    """

    def __init__(self, devices):
        AbstractThresholdType.__init__(self)
        self._devices = devices

    def get_n_threshold_parameters(self):
        return 6

    def get_threshold_parameters(self):
        return [
            NeuronParameter(
                [device.device_control_key for device in self._devices],
                DataType.UINT32),
            NeuronParameter(
                [1 if device.device_control_uses_payload else 0
                 for device in self._devices],
                DataType.UINT32),
            NeuronParameter(
                [device.device_control_min_value for device in self._devices],
                DataType.S1615),
            NeuronParameter(
                [device.device_control_max_value for device in self._devices],
                DataType.S1615),
            NeuronParameter(
                [device.device_control_timesteps_between_sending
                 for device in self._devices],
                DataType.UINT32),

            # This is the "state" variable that keeps track of how many
            # timesteps to go before a send is done
            NeuronParameter([0 for _ in self._devices], DataType.UINT32)
        ]

    def get_n_cpu_cycles_per_neuron(self):
        return 10
