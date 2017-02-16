from spynnaker_external_devices_plugin.pyNN.connections\
    .spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection

from spinnman.connections.connection_listener import ConnectionListener

import numpy
import logging
from threading import RLock

logger = logging.getLogger(__name__)

_RETINA_PACKET_SIZE = 2


class PushBotRetinaConnection(SpynnakerLiveSpikesConnection):
    """ A connection that sends spikes from the PushBot retina to a\
        spike injector in SpiNNaker.  Note that this assumes a packet format\
        of 16-bits per retina event.
    """

    def __init__(
            self, retina_injector_label, pushbot_wifi_connection,
            local_host=None, local_port=None):
        SpynnakerLiveSpikesConnection.__init__(
            self, send_labels=[retina_injector_label], local_host=local_host,
            local_port=local_port)
        self._retina_injector_label = retina_injector_label
        self._pushbot_listener = ConnectionListener(
            pushbot_wifi_connection, n_processes=1)
        self._pushbot_listener.add_callback(self._receive_retina_data)
        self._pushbot_listener.start()
        self._old_data = None
        self._lock = RLock()

    def _receive_retina_data(self, data):
        """ Receive retina packets from the pushbot and converts them into\
            neuron spikes within the spike injector system.

        :param data: Data to be processed
        """
        self._lock.acquire()

        # combine it with any leftover data from last time through the loop
        if self._old_data is not None:
            data = self._old_data + data
            self._old_data = None

        # Put the data in a numpy array
        data_all = numpy.fromstring(data, numpy.uint8).astype(numpy.uint32)

        # Extract the start of each retina packet
        retina_start_indices = numpy.where(data_all >= 0x80)[0]

        # Remove any partial retina data (can only be one extra index)
        extra_index = retina_start_indices[
            (retina_start_indices + _RETINA_PACKET_SIZE) > len(data_all)]
        if len(extra_index) > 0:
            self._old_data = data[-extra_index[0]:]
            retina_start_indices = retina_start_indices[
                (retina_start_indices + _RETINA_PACKET_SIZE) <= len(data_all)]

        # Get the retina packets
        retina_data = numpy.dstack([
            data_all[retina_start_indices + i]
            for i in range(_RETINA_PACKET_SIZE)
        ]).reshape(-1)

        if len(retina_data) > 0:

            # now process those retina events
            ys = retina_data[::_RETINA_PACKET_SIZE] & 0x7f
            xs = retina_data[1::_RETINA_PACKET_SIZE] & 0x7f
            polarity = numpy.where(
                retina_data[1::_RETINA_PACKET_SIZE] >= 0x80, 1, 0)
            neuron_ids = xs | (ys << 7) | (polarity << 14)
            self.send_spikes(self._retina_injector_label, neuron_ids)

        self._lock.release()
