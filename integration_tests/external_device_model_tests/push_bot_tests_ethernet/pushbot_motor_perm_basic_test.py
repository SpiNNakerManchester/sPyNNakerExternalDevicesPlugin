from collections import namedtuple

from enum import Enum

import spynnaker.pyNN as p
import spynnaker_external_devices_plugin.pyNN as q

# Named tuple bundling together configuration elements of a push bot resolution
# config
PushBotRetinaResolutionConfig = namedtuple("PushBotRetinaResolution",
                                           ["pixels", "enable_command",
                                            "coordinate_bits"])
n_neurons_per_command = 20
n_neurons_per_synapse_type = 10
n_commands = 4
n_neurons = n_neurons_per_command * n_commands

PushBotRetinaResolution = Enum(
    value="PushBotRetinaResolution",
    names=[("Native128",
            PushBotRetinaResolutionConfig(128, (1 << 26), 7)),
           ("Downsample64",
            PushBotRetinaResolutionConfig(64, (2 << 26), 6)),
           ("Downsample32",
            PushBotRetinaResolutionConfig(32, (3 << 26), 5)),
           ("Downsample16",
            PushBotRetinaResolutionConfig(16, (4 << 26), 4))])

# How regularity to display frames
FRAME_TIME_MS = 33

# Resolution to start retina with
RESOLUTION = \
    q.PushBotSpiNNakerLinkRetinaDevice.PushBotRetinaResolution.Downsample32
vis_data = PushBotRetinaResolution.Downsample32

# Time constant of pixel decay
DECAY_TIME_CONSTANT_MS = 100

# Value of brightest pixel to show
DISPLAY_MAX = 33.0

# Setup
p.setup(timestep=1.0)

push_bot_control_module = p.Population(
    2,
    q.PushBotLifSpinnakerLink,
    {
        'spinnaker_link_id': 0, 'speaker_start_frequency': 0,
        'motor_0_permanent_velocity_neuron_id': 0,
        'motor_1_permanent_velocity_neuron_id': 1,
        'tau_syn_E': 100,
        'uart_id': 0
    })

timer_ticks_between_test = 1000
spike_times = list()

# handle neurons
for command in range(0, n_commands):
    # inhib
    for neuron_id in range(0, n_neurons_per_synapse_type):
        data = list()
        start_time = \
            command * (n_neurons_per_command * timer_ticks_between_test)
        for time in range(0 + neuron_id, n_neurons_per_synapse_type):
            data.append(start_time + (time * timer_ticks_between_test))
        spike_times.append(data)
    # excit
    for neuron_id in range(0, n_neurons_per_synapse_type):
        data = list()
        start_time = \
            (command * (n_neurons_per_command * timer_ticks_between_test)) + \
            (n_neurons_per_synapse_type * timer_ticks_between_test)
        for time in range(0 + neuron_id, n_neurons_per_synapse_type):
            data.append(start_time + (time * timer_ticks_between_test))
        spike_times.append(data)


ssa = p.Population(n_neurons, p.SpikeSourceArray, {'spike_times': spike_times})

# 4 neurons per
connection_list_inhib = list()
connection_list_excit = list()

for motor_behaviour in range(0, 2):
    for neuron in range(0, n_neurons_per_command):
        if neuron > n_neurons_per_synapse_type - 1:
            connection_list_excit.append(
                [neuron + (motor_behaviour * n_neurons_per_command),
                 motor_behaviour, 10, 1])
        else:
            connection_list_inhib.append(
                [neuron + (motor_behaviour * n_neurons_per_command),
                 motor_behaviour, 10, 1])

p.Projection(ssa, push_bot_control_module,
             p.FromListConnector(connection_list_inhib), target="inhibitory")
p.Projection(ssa, push_bot_control_module,
             p.FromListConnector(connection_list_excit), target="excitatory")

# Run infinite simulation (non-blocking)
p.run(20000)

# End simulation
p.end()
