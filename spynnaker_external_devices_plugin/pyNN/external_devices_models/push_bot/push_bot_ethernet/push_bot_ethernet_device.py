from pacman.model.decorators.overrides import overrides
from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .abstract_multicast_controllable_device \
    import AbstractMulticastControllableDevice


class PushBotEthernetDevice(AbstractMulticastControllableDevice):
    """ An arbitrary PushBot device
    """

    def __init__(self, protocol, device, uses_payload):
        """

        :param protocol: The protocol instance to get commands from
        :param device: The Enum instance of the device to control
        :param uses_payload: True if the device uses a payload for control
        """
        self._protocol = protocol
        self._device = device
        self._uses_payload = uses_payload

    @property
    @overrides(AbstractMulticastControllableDevice.device_control_key)
    def device_control_key(self):
        return self._device.prop.fget(self._protocol)

    @property
    @overrides(AbstractMulticastControllableDevice.device_control_partition_id)
    def device_control_partition_id(self):
        return "{}_PARTITION_ID".format(self._device.name)

    @property
    @overrides(AbstractMulticastControllableDevice.device_control_uses_payload)
    def device_control_uses_payload(self):
        return self._uses_payload

    @property
    def protocol(self):
        """ The protocol instance, for use in the subclass
        """
        return self._protocol
