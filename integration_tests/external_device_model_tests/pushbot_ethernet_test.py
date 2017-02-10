import pyNN.spiNNaker as p
import spynnaker_external_devices_plugin.pyNN as e

p.setup(1.0)

# Set up the PushBot devices
pushbot_protocol = e.MunichIoSpiNNakerLinkProtocol(
    mode=e.MunichIoSpiNNakerLinkProtocol.MODES.PUSH_BOT, uart_id=0)
motor_0 = e.PushBotEthernetMotorDevice(
    e.PushBotMotor.MOTOR_0_PERMANENT, pushbot_protocol)
motor_1 = e.PushBotEthernetMotorDevice(
    e.PushBotMotor.MOTOR_1_PERMANENT, pushbot_protocol)
speaker = e.PushBotEthernetSpeakerDevice(
    e.PushBotSpeaker.SPEAKER_TONE, pushbot_protocol)

devices = [motor_0, motor_1, speaker]

# Set up the PushBot control
pushbot = e.EthernetControlPopulation(
    len(devices), e.PushBotLifEthernet,
    {
        "protocol": pushbot_protocol,
        "devices": devices,
        "pushbot_ip_address": "10.162.177.57",
        # "pushbot_ip_address": "127.0.0.1",
        "tau_syn_E": 1000.0
    },
    label="PushBot"
)

# Send in some spikes
stimulation = p.Population(
    len(devices), p.SpikeSourceArray,
    {"spike_times": [[0], [2500], [5000]]},
    label="input"
)

connections = [
    (0, 0, 4, 1),
    (1, 1, 4, 1),
    (2, 2, 100, 1)
]
p.Projection(stimulation, pushbot, p.FromListConnector(connections))

p.run(10000)
p.end()
