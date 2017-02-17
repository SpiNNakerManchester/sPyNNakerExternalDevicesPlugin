import pyNN.spiNNaker as p
import spynnaker_external_devices_plugin.pyNN as e
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_retina_viewer import PushBotRetinaViewer

p.setup(1.0)

# Set up the PushBot devices
pushbot_protocol = e.MunichIoSpiNNakerLinkProtocol(
    mode=e.MunichIoSpiNNakerLinkProtocol.MODES.PUSH_BOT, uart_id=0)
spinnaker_link = 0
board_address = None
# motor_0 = e.PushBotSpiNNakerLinkMotorDevice(
#     e.PushBotMotor.MOTOR_0_PERMANENT, pushbot_protocol,
#     spinnaker_link, board_address=board_address)
# motor_1 = e.PushBotSpiNNakerLinkMotorDevice(
#     e.PushBotMotor.MOTOR_1_PERMANENT, pushbot_protocol,
#     spinnaker_link, board_address=board_address)
# speaker = e.PushBotSpiNNakerLinkSpeakerDevice(
#     e.PushBotSpeaker.SPEAKER_TONE, pushbot_protocol,
#     spinnaker_link, board_address=board_address)
# laser = e.PushBotSpiNNakerLinkLaserDevice(
#     e.PushBotLaser.LASER_ACTIVE_TIME, pushbot_protocol,
#     spinnaker_link, board_address=board_address, start_total_period=1000)
led_front = e.PushBotSpiNNakerLinkLEDDevice(
    e.PushBotLED.LED_FRONT_ACTIVE_TIME, pushbot_protocol,
    spinnaker_link, board_address=board_address,
    start_total_period=1000)
led_back = e.PushBotSpiNNakerLinkLEDDevice(
    e.PushBotLED.LED_BACK_ACTIVE_TIME, pushbot_protocol,
    spinnaker_link, board_address=board_address,
    start_total_period=1000)

devices = [led_front, led_back]

# Set up the PushBot control
pushbot = p.Population(
    len(devices), e.PushBotLifSpinnakerLink,
    {
        "protocol": pushbot_protocol,
        "devices": devices,
        "tau_syn_E": 1000.0
    },
    label="PushBot"
)

# Send in some spikes
stimulation = p.Population(
    len(devices), p.SpikeSourceArray,
    {"spike_times": [[0], [5000]]},
    label="input"
)

connections = [
    (0, 0, 100, 1),
    (1, 1, 100, 1)
]
p.Projection(stimulation, pushbot, p.FromListConnector(connections))

retina_resolution = e.PushBotRetinaResolution.DOWNSAMPLE_64_X_64
pushbot_retina = p.Population(
    retina_resolution.value.n_neurons,
    e.PushBotSpiNNakerLinkRetinaDevice,
    {
        "spinnaker_link_id": spinnaker_link,
        "board_address": board_address,
        "protocol": pushbot_protocol,
        "resolution": retina_resolution
    })

viewer = PushBotRetinaViewer(retina_resolution.value, port=17895)
e.activate_live_output_for(pushbot_retina, port=viewer.local_port)

viewer.start()
p.run(10000)
p.end()
