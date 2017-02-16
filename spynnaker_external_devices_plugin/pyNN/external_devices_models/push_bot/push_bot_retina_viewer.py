from matplotlib import pyplot
from matplotlib import animation

from threading import Thread
import numpy
import socket
import math

# Value of brightest pixel to show
_DISPLAY_MAX = 33.0

# How regularity to display frames
_FRAME_TIME_MS = 10

# Time constant of pixel decay
_DECAY_TIME_CONSTANT_MS = 100


class PushBotRetinaViewer(Thread):

    def __init__(
            self, resolution, port=0, display_max=_DISPLAY_MAX,
            frame_time_ms=_FRAME_TIME_MS,
            decay_time_constant_ms=_DECAY_TIME_CONSTANT_MS):

        Thread.__init__(self, name="PushBotRetinaViewer")
        self._display_max = display_max
        self._frame_time_ms = frame_time_ms

        # Open socket to receive UDP
        self._spike_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._spike_socket.bind(("0.0.0.0", port))
        self._spike_socket.setblocking(False)

        self._local_host, self._local_port = self._spike_socket.getsockname()

        # Determine mask for coordinates
        self._coordinate_mask = (
            1 << (2 * resolution.bits_per_coordinate)) - 1

        # Set up the image
        self._image_data = numpy.zeros(resolution.n_neurons)
        self._image_data_view = self._image_data.view()
        self._image_data_view.shape = (
            resolution.pixels, resolution.pixels)

        # Calculate decay proportion each frame
        self._decay_proportion = math.exp(
            -float(self._frame_time_ms) / float(decay_time_constant_ms))

    @property
    def local_host(self):
        return self._local_host

    @property
    def local_port(self):
        return self._local_port

    def _updatefig(self, frame):

        # Read all UDP messages received during last frame
        while True:
            try:
                raw_data = self._spike_socket.recv(512)
            except socket.error:

                # Stop reading
                break
            else:
                # Slice off eieio header and timestamp, and convert to numpy
                # array of uint32
                payload = numpy.fromstring(raw_data[6:], dtype="uint32")

                # Mask out x, y coordinates
                payload &= self._coordinate_mask

                # Increment these pixels
                self._image_data[payload] += 1.0

        # Decay image data
        self._image_data *= self._decay_proportion

        # Set image data
        self._image.set_array(self._image_data_view)
        return [self._image]

    def run(self):

        # Create image plot of retina output
        fig = pyplot.figure()
        self._image = pyplot.imshow(
            self._image_data_view, cmap="jet", vmin=0.0,
            vmax=self._display_max)

        # Play animation
        self._ani = animation.FuncAnimation(
            fig, self._updatefig, interval=self._frame_time_ms,
            blit=True)
        pyplot.show()
