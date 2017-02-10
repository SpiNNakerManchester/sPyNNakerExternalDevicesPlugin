from six import add_metaclass
from abc import ABCMeta
from abc import abstractmethod


@add_metaclass(ABCMeta)
class AbstractEthernetSensor(object):

    @abstractmethod
    def get_n_neurons(self):
        """ Get the number of neurons that will be sent out by the device
        """

    @abstractmethod
    def get_injector_parameters(self):
        """ Get the parameters of the Spike Injector to use with this device
        """

    @abstractmethod
    def get_translator(self):
        """ Get a translator of multicast commands to Ethernet commands
        """
