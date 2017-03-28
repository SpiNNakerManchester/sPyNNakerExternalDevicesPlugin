from spynnaker8.utilities.data_holder import DataHolder
from spynnaker_external_devices_plugin.pyNN.external_devices_models \
    .munich_spinnaker_link_retina_device import MunichRetinaDevice


class MunichRetinaDeviceDataHolder(DataHolder):
    def __init__(
            self, retina_key, spinnaker_link_id, position,
            label=MunichRetinaDevice.default_parameters['label'],
            polarity=MunichRetinaDevice.default_parameters['polarity'],
            board_address=MunichRetinaDevice.default_parameters[
                'board_address']):
        DataHolder.__init__(
            self, {
                'retina_key': retina_key,
                'spinnaker_link_id': spinnaker_link_id,
                'position': position, 'label': label, 'polarity': polarity,
                'board_address': board_address})

    @staticmethod
    def build_model():
        return MunichRetinaDevice
