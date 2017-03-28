from spynnaker8.utilities.data_holder import DataHolder
from spynnaker_external_devices_plugin.pyNN.external_devices_models \
    .external_spinnaker_link_cochlea_device import ExternalCochleaDevice


class ExternalCochleaDeviceDataHolder(DataHolder):

    def __init__(
            self, spinnaker_link,
            label=ExternalCochleaDevice.default_parameters['label'],
            board_address=ExternalCochleaDevice.default_parameters[
                'board_address']):
        DataHolder.__init__(
            self, {'spinnaker_link': spinnaker_link,
                   'board_address': board_address, 'label': label})

    @staticmethod
    def build_model():
        return ExternalCochleaDevice
