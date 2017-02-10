from pacman.model.decorators.overrides import overrides

from spynnaker_external_devices_plugin.pyNN.external_devices_models\
    .abstract_ethernet_translator import AbstractEthernetTranslator
from spynnaker_external_devices_plugin.pyNN.protocols\
    .munich_io_ethernet_protocol import MunichIoEthernetProtocol

import logging
logger = logging.getLogger(__name__)


class PushBotTranslator(AbstractEthernetTranslator):
    """ Translates packets between PushBot Multicast packets and PushBot\
        WiFi Commands
    """

    def __init__(self, protocol, pushbot_wifi_connection):
        """

        :param protocol: The instance of the PushBot protocol to get keys from
        :param pushbot_wifi_connection: A WiFi connection to the PushBot
        """
        self._protocol = protocol
        self._pushbot_wifi_connection = pushbot_wifi_connection

    @overrides(AbstractEthernetTranslator.translate_control_packet)
    def translate_control_packet(self, multicast_packet):

        key = multicast_packet.key

        print "Got key {}".format(hex(multicast_packet.key))

        # disable retina
        if key == self._protocol.disable_retina_key:
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.disable_retina())

        # set retina key (which doesn't do much for Ethernet)
        elif key == self._protocol.set_retina_key_key:
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.enable_retina())

        # motor 0 leaky velocity command
        elif key == self._protocol.push_bot_motor_0_leaking_towards_zero_key:
            logger.info("Sending Motor 0 Leaky Velocity = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.motor_0_leaky_velocity(
                    multicast_packet.payload))

        # motor 0 permanent velocity command
        elif key == self._protocol.push_bot_motor_0_permanent_key:
            logger.info("Sending Motor 0 Velocity = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.motor_0_permanent_velocity(
                    multicast_packet.payload))

        # motor 1 leaky velocity command
        elif key == self._protocol.push_bot_motor_1_leaking_towards_zero_key:
            logger.info("Sending Motor 1 Leaky Velocity = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.motor_1_leaky_velocity(
                    multicast_packet.payload))

        # motor 1 permanent velocity command
        elif key == self._protocol.push_bot_motor_1_permanent_key:
            logger.info("Sending Motor 1 Velocity = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.motor_1_permanent_velocity(
                    multicast_packet.payload))

        # laser total period command
        elif key == self._protocol.push_bot_laser_config_total_period_key:
            logger.info("Sending Laser Period = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.laser_total_period(
                    multicast_packet.payload))

        # laser active time
        elif key == self._protocol.push_bot_laser_config_active_time_key:
            logger.info("Sending Laser Active Time = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.laser_active_time(
                    multicast_packet.payload))

        # laser frequency
        elif key == self._protocol.push_bot_laser_set_frequency_key:
            logger.info("Sending Laser Frequency = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.laser_frequency(
                    multicast_packet.payload))

        # led total period command
        elif key == self._protocol.push_bot_led_total_period_key:
            logger.info("Sending LED Period = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.led_total_period(
                    multicast_packet.payload))

        # led active time
        elif (key == self._protocol.push_bot_led_front_active_time_key or
              key == self._protocol.push_bot_led_back_active_time_key):
            logger.info("Sending LED Active Time = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.led_active_time(
                    multicast_packet.payload))

        # led frequency
        elif key == self._protocol.push_bot_led_set_frequency_key:
            logger.info("Sending LED Frequency = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.led_frequency(
                    multicast_packet.payload))

        # speaker total period
        elif key == self._protocol.push_bot_speaker_config_total_period_key:
            logger.info("Sending Speaker Period = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.speaker_total_period(
                    multicast_packet.payload))

        # speaker active time
        elif key == self._protocol.push_bot_speaker_config_active_time_key:
            logger.info("Sending Speaker Active Time = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.speaker_active_time(
                    multicast_packet.payload))

        # speaker frequency
        elif key == self._protocol.push_bot_speaker_set_tone_key:
            logger.info("Sending Speaker Frequency = {}".format(
                multicast_packet.payload))
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.speaker_frequency(
                    multicast_packet.payload))

        # motor enable
        elif (key == self._protocol.enable_disable_motor_key and
              multicast_packet.payload == 1):
            logger.info("Sending Motor Enable")
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.enable_motor())

        # motor disable
        elif (key == self._protocol.enable_disable_motor_key and
              multicast_packet.payload == 0):
            logger.info("Sending Motor Disable")
            self._pushbot_wifi_connection.send(
                MunichIoEthernetProtocol.disable_motor())

        else:
            logger.warn("Unknown Pushbot command: {}".format(multicast_packet))
