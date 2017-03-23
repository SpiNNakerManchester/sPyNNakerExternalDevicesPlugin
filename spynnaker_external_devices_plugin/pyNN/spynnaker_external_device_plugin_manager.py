from pacman.model.graphs.application.impl.application_edge \
    import ApplicationEdge
from spinnman.messages.eieio.eieio_type import EIEIOType
from spynnaker.pyNN import get_spynnaker
from spynnaker_external_devices_plugin.pyNN.utility_models.\
    live_spike_gather import LiveSpikeGather
from spynnaker.pyNN.utilities import constants
from spinn_front_end_common.utility_models.live_packet_gather \
    import LivePacketGather


class SpynnakerExternalDevicePluginManager(object):
    """
    main entrance for the external device plugin manager
    """

    def __init__(self):
        self._live_spike_recorders = dict()

    @staticmethod
    def add_socket_address(socket_address):
        """ Add a socket address to the list to be checked by the\
            notification protocol

        :param socket_address: the socket address
        :type socket_address:
        :rtype: None:
        """
        _spinnaker = get_spynnaker()
        _spinnaker._add_socket_address(socket_address)

    def add_edge_to_recorder_vertex(
            self, population_to_get_live_output_from, port, hostname,
            database_notify_port_num, database_notify_host,
            database_ack_port_num, tag=None, board_address=None,
            strip_sdp=True, use_prefix=False, key_prefix=None,
            prefix_type=None, message_type=EIEIOType.KEY_32_BIT,
            right_shift=0, payload_as_time_stamps=True,
            use_payload_prefix=True, payload_prefix=None,
            payload_right_shift=0, number_of_packets_sent_per_time_step=0):
        """
        adds a edge from a vertex to the LPG object, builds as needed and has
        all the parameters for the creation of the LPG if needed

        :param population_to_get_live_output_from:
        the source pop for live output
        :param port: the port number used for live output
        :param hostname: the hostname to fire live out to
        :param database_notify_port_num: the notification port number for
        the notification protocol.
        :param database_notify_host: the hostname for the notification protocol.
        :param database_ack_port_num: the port for where the notification
        protocol will receive its read database message from
        :param tag: the tag id for this live output
        :param board_address: the board address to target
        :param strip_sdp: if the messages coming out of the machine should
        have their sdp header taken away
        :param use_prefix: If the message is going to use EIEIO prefix
        :param key_prefix: The key prefix for the EIEIO message
        :param prefix_type: The prefix type of the EIEIO message
        :param message_type: The EIEIO message type for live output
        :param right_shift: The right shift of the key for the EIEIO message
        :param payload_as_time_stamps: If the EIEIO message is using the
        payload field for timestamps.
        :param use_payload_prefix: If the EIEIO message is using a
        payload prefix
        :param payload_prefix: The payload prefix for the EIEIO message
         if required.
        :param payload_right_shift: the right shift for the payload for
        the EIEIO message
        :param number_of_packets_sent_per_time_step: the number of UDP
        packets to send per timertick (band width limiter)
        :return: None
        """

        # get global spinnaker
        _spinnaker = get_spynnaker()

        # locate the live spike recorder
        if (port, hostname) in self._live_spike_recorders:
            live_spike_recorder = self._live_spike_recorders[(port, hostname)]
        else:
            # build a live spike gatherer population and add edge

            # build cell params for the population
            cellparams = {
                #'machine_time_step': _spinnaker.machine_time_step,
                #'time_scale_factor': _spinnaker.timescale_factor,
                #'database_notification_port_number': database_notify_port_num,
                #'database_notify_host': database_notify_host,
                #'database_ack_port_number': database_ack_port_num,
                'ip_address': hostname, 'port': port,
                'board_address': board_address, 'tag': tag,
                'strip_sdp': strip_sdp, 'use_prefix': use_prefix,
                'key_prefix': key_prefix, 'prefix_type': prefix_type,
                'message_type': message_type, 'right_shift': right_shift,
                'payload_as_time_stamps': payload_as_time_stamps,
                'use_payload_prefix': use_payload_prefix,
                'payload_prefix': payload_prefix,
                'payload_right_shift': payload_right_shift,
                'number_of_packets_sent_per_time_step':
                    number_of_packets_sent_per_time_step}

            # create population
            # live_spike_recorder = _spinnaker.create_population(
            #     size=1, cellclass=LiveSpikeGather, cellparams=cellparams,
            #     structure=None, label="LiveSpikeReceiver")

            # record pop for later usage
            live_spike_recorder = LivePacketGather(
                label="LiveSpikeReceiver", **cellparams)
            self._live_spike_recorders[(port, hostname)] = live_spike_recorder
            _spinnaker.add_application_vertex(live_spike_recorder)

        # create the edge and add
        edge = ApplicationEdge(
            population_to_get_live_output_from, live_spike_recorder,
            label="recorder_edge")
        _spinnaker.add_application_edge(edge, constants.SPIKE_PARTITION_ID)

    def add_edge(self, vertex, device_vertex, partition_id):
        """
        adds a edge between two vertices (often a vertex and a external device)
        on a given partition

        :param vertex: the pre vertex to connect the edge from
        :param device_vertex: the post vertex to connect the edge to
        :param partition_id: the partition identifier for making nets
        :rtype: None
        """
        _spinnaker = get_spynnaker()

        edge = ApplicationEdge(vertex, device_vertex)
        _spinnaker.add_application_edge(edge, partition_id)

    def machine_time_step(self):
        _spinnaker = get_spynnaker()
        return _spinnaker.machine_time_step

    def time_scale_factor(self):
        _spinnaker = get_spynnaker()
        return _spinnaker.timescale_factor
