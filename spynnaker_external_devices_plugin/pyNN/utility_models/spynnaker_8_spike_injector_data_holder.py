from spynnaker8.utilities.data_holder import DataHolder
from spynnaker_external_devices_plugin.pyNN.utility_models.spike_injector \
    import SpikeInjector


class SpikeInjectorDataHolder(DataHolder):

    def __init__(
            self, label=SpikeInjector.default_parameters['label'],
            port=SpikeInjector.default_parameters['port'],
            virtual_key=SpikeInjector.default_parameters['virtual_key']):
        DataHolder.__init__(
            self, {'label': label, 'port': port, 'virtual_key': virtual_key})

    @staticmethod
    def build_model():
        return SpikeInjector
