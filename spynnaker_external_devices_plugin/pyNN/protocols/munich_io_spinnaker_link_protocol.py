from spinn_front_end_common.utility_models.multi_cast_command \
    import MultiCastCommand
from spinn_front_end_common.utilities import exceptions

from enum import Enum
import logging

logger = logging.getLogger(__name__)

# structure of command is KKKKKKKKKKKKKKKKKKKKK-IIIIIII-F-DDD
# K = ignored key at the top of the command
# I = instruction
# F = format
# D = device
_OFFSET_TO_IGNORED_KEY = 11
_OFFSET_TO_I = 4
_OFFSET_TO_F = 3
_OFFSET_TO_D = 0


def MUNICH_KEY(I, F, D):
    return (I << _OFFSET_TO_I) | (F << _OFFSET_TO_F) | (D << _OFFSET_TO_D)


def MUNICH_KEY_I_D(I, D):
    return MUNICH_KEY(I, 0, D)


def MUNICH_KEY_I(I):
    return MUNICH_KEY(I, 0, 0)

# Specific fields in the key
_OFFSET_FOR_UART_ID = 29
_PUSH_BOT_UART_OFFSET_SPEAKER_LED_LASER = 1
_SENSOR_OUTGOING_OFFSET_TO_D = 2
_SENSOR_OUTGOING_OFFSET_TO_I = 7

# Payload fields
_PAYLOAD_OFFSET_FOR_TIMESTAMPS = 29
_PAYLOAD_OFFSET_FOR_RETINA_SIZE = 26
_PAYLOAD_SENSOR_ID_OFFSET = 27
_PAYLOAD_OFFSET_FOR_SENSOR_TIME = 0

# command key for setting up the master key of the board
_CONFIGURE_MASTER_KEY = MUNICH_KEY_I_D(127, 0)

# command key for setting up what mode of device running on the board
_CHANGE_MODE = MUNICH_KEY_I_D(127, 1)

# command for turning off retina output
_DISABLE_RETINA_EVENT_STREAMING = MUNICH_KEY_I_D(0, 0)

# command for retina where payload is events
_ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION = \
    MUNICH_KEY_I_D(0, 1)

# command for retina where events are the key
_ACTIVE_RETINA_EVENT_STREAMING_SET_KEY = MUNICH_KEY_I_D(0, 2)

# set timer / counter for timestamps
_SET_TIMER_COUNTER_FOR_TIMESTAMPS = MUNICH_KEY_I_D(0, 3)

# handle master / slave time sync
_MASTER_SLAVE_KEY = MUNICH_KEY_I_D(0, 4)

# command for setting bias (whatever the check that is)
_BIAS_KEY = MUNICH_KEY_I_D(0, 5)

# reset retina key.
_RESET_RETINA_KEY = MUNICH_KEY_I_D(0, 7)

# request on-board sensor data
_SENSOR_REPORTING_OFF_KEY = MUNICH_KEY_I_D(1, 0)

# poll sensors once
_POLL_SENSORS_ONCE_KEY = MUNICH_KEY_I_D(1, 1)

# poll sensors continuously
_POLL_SENSORS_CONTINUOUSLY_KEY = MUNICH_KEY_I_D(1, 2)

# disable motor
_DISABLE_MOTOR_KEY = MUNICH_KEY_I_D(2, 0)

# run motor for total period
_MOTOR_RUN_FOR_PERIOD_KEY = MUNICH_KEY_I_D(2, 1)

# raw output for motor 0 (permanent)
_MOTOR_0_RAW_PERM_KEY = MUNICH_KEY_I_D(2, 4)

# raw output for motor 1 (permanent)
_MOTOR_1_RAW_PERM_KEY = MUNICH_KEY_I_D(2, 5)

# raw output for motor 0 (leak towards 0)
_MOTOR_0_RAW_LEAK_KEY = MUNICH_KEY_I_D(2, 6)

# raw output for motor 1 (leak towards 0)
_MOTOR_1_RAW_LEAK_KEY = MUNICH_KEY_I_D(2, 7)

# motor output duration timer period
_MOTOR_TIMER_A_TOTAL_PERIOD_KEY = MUNICH_KEY_I_D(3, 0)
_MOTOR_TIMER_B_TOTAL_PERIOD_KEY = MUNICH_KEY_I_D(3, 2)
_MOTOR_TIMER_C_TOTAL_PERIOD_KEY = MUNICH_KEY_I_D(3, 4)

# motor output ratio active period
_MOTOR_TIMER_A_CHANNEL_0_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 0)
_MOTOR_TIMER_A_CHANNEL_1_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 1)
_MOTOR_TIMER_B_CHANNEL_0_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 2)
_MOTOR_TIMER_B_CHANNEL_1_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 3)
_MOTOR_TIMER_C_CHANNEL_0_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 4)
_MOTOR_TIMER_C_CHANNEL_1_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 5)

# digital IO Signals
_QUERY_STATES_LINES_KEY = MUNICH_KEY_I_D(5, 0)

# set output pattern to payload
_SET_OUTPUT_PATTERN_KEY = MUNICH_KEY_I_D(5, 1)

# add payload (logic or (PL)) to current output
_ADD_PAYLOAD_TO_CURRENT_OUTPUT_KEY = MUNICH_KEY_I_D(5, 2)

# remove payload (logic or (PL)) to current output from current output
_REMOVE_PAYLOAD_TO_CURRENT_OUTPUT_KEY = MUNICH_KEY_I_D(5, 3)

# set payload pins to high impedance
_SET_PAYLOAD_TO_HIGH_IMPEDANCE_KEY = MUNICH_KEY_I_D(5, 4)

# set laser params for pushbot
_PUSH_BOT_LASER_CONFIG_TOTAL_PERIOD = MUNICH_KEY_I_D(4, 0)
_PUSH_BOT_LASER_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 0)
_PUSH_BOT_LASER_FREQUENCY = MUNICH_KEY_I_D(37, 1)

# set led params for pushbot
_PUSH_BOT_LED_CONFIG_TOTAL_PERIOD = MUNICH_KEY_I_D(4, 4)
_PUSH_BOT_LED_BACK_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 4)
_PUSH_BOT_LED_FRONT_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 5)
_PUSH_BOT_LED_FREQUENCY = MUNICH_KEY_I_D(37, 0)

# set speaker params for pushbot
_PUSH_BOT_SPEAKER_CONFIG_TOTAL_PERIOD = MUNICH_KEY_I_D(4, 2)
_PUSH_BOT_SPEAKER_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 2)
_PUSH_BOT_SPEAKER_TONE_BEEP = MUNICH_KEY_I_D(36, 0)
_PUSH_BOT_SPEAKER_TONE_MELODY = MUNICH_KEY_I_D(36, 1)

# pushbot motor control
_PUSH_BOT_MOTOR_0_PERMANENT_VELOCITY = MUNICH_KEY_I_D(32, 0)
_PUSH_BOT_MOTOR_1_PERMANENT_VELOCITY = MUNICH_KEY_I_D(32, 1)
_PUSH_BOT_MOTOR_0_LEAKY_VELOCITY = MUNICH_KEY_I_D(32, 2)
_PUSH_BOT_MOTOR_1_LEAKY_VELOCITY = MUNICH_KEY_I_D(32, 3)

# payloads for the different modes
_PAYLOAD_RESET_TO_DEFAULT_MODE = 0
_PAYLOAD_SET_TO_PUSH_BOT_MODE = 1
_PAYLOAD_SET_TO_SPOMNI_BOT_MODE = 2
_PAYLOAD_SET_TO_BALL_BALANCER_MODE = 3
_PAYLOAD_SET_TO_MY_OROBOTICS_PROJECT_MODE = 4
_PAYLOAD_SET_TO_FREE_MODE = 5

# payload for setting different time stamp sizes
_PAYLOAD_NO_TIMESTAMPS = (0 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
_PAYLOAD_DELTA_TIMESTAMPS = (1 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
_PAYLOAD_TWO_BYTE_TIME_STAMPS = (2 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
_PAYLOAD_THREE_BYTE_TIME_STAMPS = (3 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
_PAYLOAD_FOUR_BYTE_TIME_STAMPS = (4 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)

# payload for retina size
_PAYLOAD_RETINA_NO_DOWN_SAMPLING_IN_PAYLOAD = (
    0 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
_PAYLOAD_RETINA_NO_DOWN_SAMPLING = (1 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
_PAYLOAD_RETINA_64_DOWN_SAMPLING = (2 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
_PAYLOAD_RETINA_32_DOWN_SAMPLING = (3 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
_PAYLOAD_RETINA_16_DOWN_SAMPLING = (4 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)

# payload for master slave
_PAYLOAD_MASTER_SLAVE_USE_INTERNAL_COUNTER = 0
_PAYLOAD_MASTER_SLAVE_SET_SLAVE = 1
_PAYLOAD_MASTER_SLAVE_SET_MASTER_CLOCK_NOT_STARTED = 2
_PAYLOAD_MASTER_SLAVE_SET_MASTER_CLOCK_ACTIVE = 4


class MunichIoSpiNNakerLinkProtocol(object):
    """ Provides Multicast commands for the Munich SpiNNaker-Link protocol
    """

    # types of modes supported by this protocol
    MODES = Enum(
        value="MODES",
        names=[('RESET_TO_DEFAULT', 0),
               ('PUSH_BOT', 1),
               ('SPOMNIBOT', 2),
               ('BALL_BALANCER', 3),
               ('MY_ORO_BOTICS', 4),
               ('FREE', 5)])

    # The instance of the protocol in use, to ensure that each vertex that is
    # to send commands to the pushbot uses a different outgoing key; the top
    # part of the key is ignored, so this works out!
    protocol_instance = 0

    # Keeps track of whether the mode has been configured already
    sent_mode_command = False

    def __init__(self, mode, instance_key=None):
        """

        :param mode: The mode of operation of the protocol
        :param instance_key: The optional instance key to use
        """
        self._mode = mode

        # Create a key for this instance of the protocol
        # - see above for reasoning
        if instance_key is None:
            self._instance_key = (
                MunichIoSpiNNakerLinkProtocol.protocol_instance <<
                _OFFSET_TO_IGNORED_KEY
            )
            MunichIoSpiNNakerLinkProtocol.protocol_instance += 1
        else:
            self._instance_key = instance_key

    @staticmethod
    def sent_mode_command():
        """ True if the mode command has ever been requested by any instance
        """
        return MunichIoSpiNNakerLinkProtocol.sent_mode_command

    @property
    def instance_key(self):
        """ The key of this instance of the protocol
        """
        return self._instance_key

    def get_configure_master_key_command(self, new_key, time=None):
        return MultiCastCommand(
            key=_CONFIGURE_MASTER_KEY | self._instance_key, payload=new_key,
            time=time)

    def get_set_mode_command(self, time=None):
        MunichIoSpiNNakerLinkProtocol.sent_mode_command = True
        return MultiCastCommand(
            key=_CHANGE_MODE | self._instance_key,
            payload=self._mode.value(), time=time)

    def set_retina_transmission_key(self, new_key, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_ACTIVE_RETINA_EVENT_STREAMING_SET_KEY |
                 uart_id << _OFFSET_FOR_UART_ID | self._instance_key),
            payload=new_key, time=time)

    def disable_retina_event_streaming(self, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_DISABLE_RETINA_EVENT_STREAMING |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            time=time)

    def master_slave_use_internal_counter(self, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MASTER_SLAVE_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=_PAYLOAD_MASTER_SLAVE_USE_INTERNAL_COUNTER,
            time=time)

    def master_slave_set_slave(self, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MASTER_SLAVE_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=_PAYLOAD_MASTER_SLAVE_SET_SLAVE, time=time)

    def master_slave_set_master_clock_not_started(self, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MASTER_SLAVE_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=_PAYLOAD_MASTER_SLAVE_SET_MASTER_CLOCK_NOT_STARTED,
            time=time)

    def master_slave_set_master_clock_active(self, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MASTER_SLAVE_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=_PAYLOAD_MASTER_SLAVE_SET_MASTER_CLOCK_ACTIVE,
            time=time)

    def bias_values(self, bias_id, bias_value, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_BIAS_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=((bias_id << 0) | (bias_value << 8)),
            time=time)

    def reset_retina(self, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_RESET_RETINA_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            time=time)

    def turn_off_sensor_reporting(self, sensor_id, time=None):
        return MultiCastCommand(
            key=_SENSOR_REPORTING_OFF_KEY | self._instance_key,
            payload=(sensor_id << _PAYLOAD_SENSOR_ID_OFFSET), time=time)

    def poll_sensors_once(self, sensor_id, time=None):
        return MultiCastCommand(
            key=_POLL_SENSORS_ONCE_KEY | self._instance_key,
            payload=(sensor_id << _PAYLOAD_SENSOR_ID_OFFSET), time=time)

    def poll_individual_sensor_continuously(
            self, sensor_id, time_in_ms, time=None):
        return MultiCastCommand(
            key=_POLL_SENSORS_CONTINUOUSLY_KEY | self._instance_key,
            payload=((sensor_id << _PAYLOAD_SENSOR_ID_OFFSET) |
                     (time_in_ms << _PAYLOAD_OFFSET_FOR_SENSOR_TIME)),
            time=time)

    def generic_motor_enable_disable(
            self, enable_disable, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_DISABLE_MOTOR_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=enable_disable, time=time)

    def generic_motor_total_period_duration(
            self, time_in_ms, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_RUN_FOR_PERIOD_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=time_in_ms, time=time)

    def generic_motor0_raw_output_permanent(
            self, pwm_signal, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_0_RAW_PERM_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=pwm_signal, time=time)

    def generic_motor1_raw_output_permanent(
            self, pwm_signal, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_1_RAW_PERM_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=pwm_signal, time=time)

    def generic_motor0_raw_output_leak_to_0(
            self, pwm_signal, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_0_RAW_LEAK_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=pwm_signal, time=time)

    def generic_motor1_raw_output_leak_to_0(
            self, pwm_signal, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_1_RAW_LEAK_KEY | (uart_id << _OFFSET_FOR_UART_ID) |
                 self._instance_key),
            payload=pwm_signal, time=time)

    def pwm_pin_output_timer_a_duration(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_A_TOTAL_PERIOD_KEY |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=timer_period, time=time)

    def pwm_pin_output_timer_b_duration(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_B_TOTAL_PERIOD_KEY | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)), payload=timer_period,
            time=time)

    def pwm_pin_output_timer_c_duration(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_C_TOTAL_PERIOD_KEY | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)), payload=timer_period,
            time=time)

    def pwm_pin_output_timer_a_channel_0_ratio(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_A_CHANNEL_0_ACTIVE_PERIOD_KEY |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=timer_period, time=time)

    def pwm_pin_output_timer_a_channel_1_ratio(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_A_CHANNEL_1_ACTIVE_PERIOD_KEY |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=timer_period, time=time)

    def pwm_pin_output_timer_b_channel_0_ratio(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_B_CHANNEL_0_ACTIVE_PERIOD_KEY |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=timer_period, time=time)

    def pwm_pin_output_timer_b_channel_1_ratio(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_B_CHANNEL_1_ACTIVE_PERIOD_KEY |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=timer_period, time=time)

    def pwm_pin_output_timer_c_channel_0_ratio(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_C_CHANNEL_0_ACTIVE_PERIOD_KEY |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=timer_period, time=time)

    def pwm_pin_output_timer_c_channel_1_ratio(
            self, timer_period, uart_id=0, time=None):
        return MultiCastCommand(
            key=(_MOTOR_TIMER_C_CHANNEL_1_ACTIVE_PERIOD_KEY |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=timer_period, time=time)

    def query_state_of_io_lines(self, time=None):
        return MultiCastCommand(
            key=_QUERY_STATES_LINES_KEY | self._instance_key, time=time)

    def set_output_pattern_for_payload(self, payload, time=None):
        return MultiCastCommand(
            key=_SET_OUTPUT_PATTERN_KEY | self._instance_key, payload=payload,
            time=time)

    def add_payload_logic_to_current_output(self, payload, time=None):
        return MultiCastCommand(
            key=_ADD_PAYLOAD_TO_CURRENT_OUTPUT_KEY | self._instance_key,
            payload=payload, time=time)

    def remove_payload_logic_to_current_output(self, payload, time=None):
        return MultiCastCommand(
            key=_REMOVE_PAYLOAD_TO_CURRENT_OUTPUT_KEY | self._instance_key,
            payload=payload, time=time)

    def set_payload_pins_to_high_impedance(self, payload, time=None):
        return MultiCastCommand(
            key=_SET_PAYLOAD_TO_HIGH_IMPEDANCE_KEY | self._instance_key,
            payload=payload, time=time)

    def push_bot_laser_config_total_period(
            self, total_period, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_LASER_CONFIG_TOTAL_PERIOD |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=total_period, time=time)

    def push_bot_laser_config_active_time(
            self, active_time, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_LASER_CONFIG_ACTIVE_TIME |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=active_time, time=time)

    def push_bot_laser_set_frequency(self, frequency, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_LASER_FREQUENCY | self._instance_key |
                 (uart_id << _PUSH_BOT_UART_OFFSET_SPEAKER_LED_LASER)),
            payload=frequency, time=time)

    def push_bot_speaker_config_total_period(
            self, total_period, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_SPEAKER_CONFIG_TOTAL_PERIOD |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=total_period, time=time)

    def push_bot_speaker_config_active_time(
            self, active_time, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_SPEAKER_CONFIG_ACTIVE_TIME |
                 (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
            payload=active_time, time=time)

    def push_bot_speaker_set_tone(self, frequency, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_SPEAKER_TONE_BEEP | self._instance_key |
                 (uart_id << _PUSH_BOT_UART_OFFSET_SPEAKER_LED_LASER)),
            payload=frequency, time=time)

    def push_bot_speaker_set_melody(self, melody, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_SPEAKER_TONE_MELODY | self._instance_key |
                 (uart_id << _PUSH_BOT_UART_OFFSET_SPEAKER_LED_LASER)),
            payload=melody, time=time)

    def push_bot_led_total_period(self, total_period, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_LED_CONFIG_TOTAL_PERIOD | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)),
            payload=total_period, time=time)

    def push_bot_led_back_active_time(
            self, active_time, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_LED_BACK_CONFIG_ACTIVE_TIME | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)),
            payload=active_time, time=time)

    def push_bot_led_front_active_time(
            self, active_time, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_LED_FRONT_CONFIG_ACTIVE_TIME | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)),
            payload=active_time, time=time)

    def push_bot_led_set_frequency(self, frequency, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_LED_FREQUENCY | self._instance_key |
                 (uart_id << _PUSH_BOT_UART_OFFSET_SPEAKER_LED_LASER)),
            payload=frequency, time=time)

    def push_bot_motor_0_permanent(self, velocity, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_MOTOR_0_PERMANENT_VELOCITY | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)),
            payload=velocity, time=time)

    def push_bot_motor_1_permanent(self, velocity, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_MOTOR_1_PERMANENT_VELOCITY | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)),
            payload=velocity, time=time)

    def push_bot_motor_0_leaking_towards_zero(
            self, velocity, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_MOTOR_0_LEAKY_VELOCITY | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)),
            payload=velocity, time=time)

    def push_bot_motor_1_leaking_towards_zero(
            self, velocity, uart_id=0, time=None):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))
        return MultiCastCommand(
            key=(_PUSH_BOT_MOTOR_1_LEAKY_VELOCITY | self._instance_key |
                 (uart_id << _OFFSET_FOR_UART_ID)),
            payload=velocity, time=time)

    @staticmethod
    def sensor_transmission_key(sensor_id, uart_id=0):
        return ((sensor_id << _SENSOR_OUTGOING_OFFSET_TO_D) |
                (uart_id << _SENSOR_OUTGOING_OFFSET_TO_I))

    def set_retina_transmission(
            self, events_in_key=True, retina_pixels=128 * 128,
            payload_holds_time_stamps=False, size_of_time_stamp_in_bytes=None,
            uart_id=0, time=None, repeat=0, delay=0):

        # if events in the key.
        if events_in_key:
            if not payload_holds_time_stamps:

                # not using payloads
                return self._key_retina(
                    retina_pixels, _PAYLOAD_NO_TIMESTAMPS, uart_id, time,
                    repeat, delay)
            else:

                # using payloads
                if size_of_time_stamp_in_bytes == 0:
                    return self._key_retina(
                        retina_pixels, _PAYLOAD_DELTA_TIMESTAMPS,
                        uart_id, time, repeat, delay)
                if size_of_time_stamp_in_bytes == 2:
                    return self._key_retina(
                        retina_pixels, _PAYLOAD_TWO_BYTE_TIME_STAMPS,
                        uart_id, time, repeat, delay)
                if size_of_time_stamp_in_bytes == 3:
                    return self._key_retina(
                        retina_pixels, _PAYLOAD_THREE_BYTE_TIME_STAMPS,
                        uart_id, time, repeat, delay)
                if size_of_time_stamp_in_bytes == 4:
                    return self._key_retina(
                        retina_pixels, _PAYLOAD_FOUR_BYTE_TIME_STAMPS,
                        uart_id, time, repeat, delay)
        else:

            # using payloads to hold all events

            # warn users about models
            logger.warning(
                "The current SpyNNaker models do not support the reception of"
                " packets with payloads, therefore you will need to add a "
                "adaptor model between the device and spynnaker models.")

            # verify that its what the end user wants.
            if (payload_holds_time_stamps or
                    size_of_time_stamp_in_bytes is not None):
                raise exceptions.ConfigurationException(
                    "If you are using payloads to store events, you cannot"
                    " have time stamps at all.")
            return MultiCastCommand(
                key=(_ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION |
                     (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
                payload=(_PAYLOAD_NO_TIMESTAMPS |
                         _PAYLOAD_RETINA_NO_DOWN_SAMPLING_IN_PAYLOAD),
                time=time, repeat=repeat, delay_between_repeats=delay)

    def _key_retina(
            self, retina_pixels, time_stamps, uart_id, time, repeat, delay):
        if retina_pixels == 128 * 128:
            return MultiCastCommand(
                key=(_ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION |
                     (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
                payload=(time_stamps | _PAYLOAD_RETINA_NO_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        if retina_pixels == 64 * 64:
            return MultiCastCommand(
                key=(_ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION |
                     (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
                payload=(time_stamps | _PAYLOAD_RETINA_64_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        if retina_pixels == 32 * 32:
            return MultiCastCommand(
                key=(_ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION |
                     (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
                payload=(time_stamps | _PAYLOAD_RETINA_32_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        if retina_pixels == 16 * 16:
            return MultiCastCommand(
                key=(_ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION |
                     (uart_id << _OFFSET_FOR_UART_ID) | self._instance_key),
                payload=(time_stamps | _PAYLOAD_RETINA_16_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        else:
            raise exceptions.ConfigurationException(
                "The no of pixels is not supported in this protocol.")
