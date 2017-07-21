from spynnaker.pyNN.connections import SpynnakerLiveSpikesConnection

import warnings

warnings.warn(
    "Using sPyNNakerExternalDevicesPlugin in deprecated."
    " Please instead use"
    " sPyNNaker7.pyNN.external_devices.SpynnakerLiveSpikesConnection"
    " (or if you have import pyNN.spiNNaker as p in your script you can use"
    " p.external_devices.SpynnakerLiveSpikesConnection)")

__all__ = ["SpynnakerLiveSpikesConnection"]
