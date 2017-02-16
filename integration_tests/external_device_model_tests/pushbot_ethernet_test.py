import pyNN.spiNNaker as p
import spynnaker_external_devices_plugin.pyNN as e
from spynnaker_external_devices_plugin.pyNN.external_devices_models.push_bot\
    .push_bot_retina_viewer import PushBotRetinaViewer
from time import sleep

p.setup(1.0)

# Set up the PushBot devices
pushbot_protocol = e.MunichIoSpiNNakerLinkProtocol(
    mode=e.MunichIoSpiNNakerLinkProtocol.MODES.PUSH_BOT, uart_id=0)
# motor_0 = e.PushBotEthernetMotorDevice(
#     e.PushBotMotor.MOTOR_0_PERMANENT, pushbot_protocol)
# motor_1 = e.PushBotEthernetMotorDevice(
#     e.PushBotMotor.MOTOR_1_PERMANENT, pushbot_protocol)
# speaker = e.PushBotEthernetSpeakerDevice(
#     e.PushBotSpeaker.SPEAKER_TONE, pushbot_protocol)
# laser = e.PushBotEthernetLaserDevice(
#     e.PushBotLaser.LASER_ACTIVE_TIME, pushbot_protocol,
#     start_total_period=1000)
# led_front = e.PushBotEthernetLEDDevice(
#     e.PushBotLED.LED_FRONT_ACTIVE_TIME, pushbot_protocol,
#     start_total_period=1000)
# led_back = e.PushBotEthernetLEDDevice(
#     e.PushBotLED.LED_BACK_ACTIVE_TIME, pushbot_protocol,
#     start_total_period=1000)
#
# devices = [led_front, led_back]

# Set up the PushBot control
# pushbot = e.EthernetControlPopulation(
#     len(devices), e.PushBotLifEthernet,
#     {
#         "protocol": pushbot_protocol,
#         "devices": devices,
#         "pushbot_ip_address": "10.162.177.57",
#         # "pushbot_ip_address": "127.0.0.1",
#         "tau_syn_E": 1000.0
#     },
#     label="PushBot"
# )

# # Send in some spikes
# stimulation = p.Population(
#     len(devices), p.SpikeSourceArray,
#     {"spike_times": [[0], [5000]]},
#     label="input"
# )
#
# connections = [
#     (0, 0, 100, 1),
#     (1, 1, 100, 1)
# ]
# p.Projection(stimulation, pushbot, p.FromListConnector(connections))

pushbot_retina = e.EthernetSensorPopulation(
    e.PushBotEthernetRetinaDevice,
    {
        "protocol": pushbot_protocol,
        "resolution": e.PushBotRetinaResolution.NATIVE_128_X_128,
        # "pushbot_ip_address": "10.162.177.57"
        "pushbot_ip_address": "127.0.0.1"
    })

viewer = PushBotRetinaViewer(
    e.PushBotRetinaResolution.NATIVE_128_X_128.value, port=17895)
e.activate_live_output_for(pushbot_retina, port=viewer.local_port)

viewer.start()
p.run(10000)
p.end()
