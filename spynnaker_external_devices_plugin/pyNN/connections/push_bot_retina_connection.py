from spynnaker_external_devices_plugin.pyNN.connections\
    .spynnaker_live_spikes_connection import SpynnakerLiveSpikesConnection
from spinnman.connections.connection_listener import ConnectionListener

import numpy
import logging

logger = logging.getLogger(__name__)


class PushBotRetinaConnection(SpynnakerLiveSpikesConnection):
    """ A connection that sends spikes from the PushBot retina to a\
        spike injector in SpiNNaker
    """

    def __init__(
            self, retina_injector_label, pushbot_wifi_connection,
            local_host=None, local_port=19999):
        SpynnakerLiveSpikesConnection.__init__(
            self, send_labels=[retina_injector_label], local_host=local_host,
            local_port=local_port)
        self._retina_injector_label = retina_injector_label
        self._pushbot_listener = ConnectionListener(pushbot_wifi_connection)
        self._pushbot_listener.add_callback(self._receive_retina_data)
        self._pushbot_listener.start()

    def _receive_retina_data(self, data):
        """ Receive retina packets from the pushbot and converts them into\
            neuron spikes within the spike injector system.

        :param data: Data to be processed
        """

        # combine it with any leftover data from last time through the loop
        if self._old_data is not None:
            data = self._old_data + data
            self._old_data = None

        if self._retina_packet_size is None:

            # no retina events, so everything should be ascii
            self._buffered_ascii += data
        else:

            # find the ascii events
            data_all = numpy.fromstring(data, numpy.uint8)
            ascii_index = numpy.where(
                data_all[::self._retina_packet_size] < 0x80)[0]

            offset = 0
            while len(ascii_index) > 0:

                # if there's an ascii event, remove it from the data
                index = ascii_index[0] * self._retina_packet_size
                stop_index = numpy.where(data_all[index:] >= 0x80)[0]
                if len(stop_index) > 0:
                    stop_index = index + stop_index[0]
                else:
                    stop_index = len(data)

                # and add it to the buffered_ascii list
                self._buffered_ascii += \
                    data[offset + index:offset + stop_index]
                data_all = numpy.hstack(
                    (data_all[:index], data_all[stop_index:]))
                offset += stop_index - index
                ascii_index = numpy.where(
                    data_all[::self._retina_packet_size] < 0x80)[0]

            # handle any partial retina packets
            extra = len(data_all) % self._retina_packet_size
            if extra != 0:
                self._old_data = data[-extra:]
                data_all = data_all[:-extra]

            if len(data_all) > 0:

                # now process those retina events
                self._process_retina(data_all)

    def _process_retina(self, data_all):
        ys = data_all[::6] & 0x7f
        xs = data_all[1::6] & 0x7f
        polarity = numpy.where(data_all[1::6] >= 0x80, 1, -1)
        for x, y, local_polarity in zip(xs, ys, polarity):
            neuron_id = x + (y * 128)
            if local_polarity == -1:
                neuron_id += 128 * 128
            if neuron_id > 128 * 128 * 2:
                logger.error("Neuron id too big")
            if neuron_id < 0:
                logger.error("Neuron id too small")
            self.send_spike(self._retina_injector_label, neuron_id)
