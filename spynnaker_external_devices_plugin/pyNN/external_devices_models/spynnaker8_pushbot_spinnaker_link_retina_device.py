from spynnaker8.utilities.data_holder import DataHolder
from spynnaker_external_devices_plugin.pyNN.external_devices_models \
    .pushbot_spinnaker_link_retina_device import PushBotRetinaDevice


class PushBotRetinaDeviceDataHolder(DataHolder):
    def __init__(
            self, fixed_key, spinnaker_link_id,
            label=PushBotRetinaDevice.default_parameters['label'],
            polarity=PushBotRetinaDevice.default_parameters['polarity'],
            resolution=PushBotRetinaDevice.default_parameters['resolution'],
            board_address=PushBotRetinaDevice.default_parameters[
                'board_address'],
            command_sender_top_bits_key=PushBotRetinaDevice.
            default_parameters['command_sender_top_bits_key']):
        DataHolder.__init__(
            self, {
                'fixed_key': fixed_key,
                'spinnaker_link_id': spinnaker_link_id,
                'label': label, 'polarity': polarity,
                'board_address': board_address, 'resolution': resolution,
                'command_sender_top_bits_key': command_sender_top_bits_key})

    @staticmethod
    def build_model():
        return PushBotRetinaDevice
