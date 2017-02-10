from six import add_metaclass
from abc import ABCMeta
from abc import abstractmethod


@add_metaclass(ABCMeta)
class AbstractEthernetTranslator(object):
    """ A module that can translate packets received over Ethernet into\
        control of an external device
    """

    @abstractmethod
    def translate_control_packet(self, multicast_packet):
        """ Translate a multicast packet received over Ethernet and send\
            appropriate messages to the external device

        :param multicast_packet: A received multicast packet
        :type multicast_packet:\
            :py:class:`spinnman.messages.eieio.data_messages.abstract_eieio_data_element.AbstractEIEIODataElement`
        """
