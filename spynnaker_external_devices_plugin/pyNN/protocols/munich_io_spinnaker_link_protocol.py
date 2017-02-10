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
_KEY_MASK = 0xFFFFF800
_I_MASK = 0x7F0
_F_MASK = 0x8
_D_MASK = 0x7


# UART masks and shifts
RETINA_UART_SHIFT = 3 + _OFFSET_TO_I
RETINA_WITHOUT_UART_MASK = 0x670
PUSH_BOT_LASER_LED_SPEAKER_FREQUENCY_UART_SHIFT = 1 + _OFFSET_TO_D
PUSH_BOT_MOTOR_WITHOUT_UART_MASK = 0x7C0
PUSH_BOT_MOTOR_UART_SHIFT = 0 + _OFFSET_TO_I


def MUNICH_KEY(I, F, D):
    return (I << _OFFSET_TO_I) | (F << _OFFSET_TO_F) | (D << _OFFSET_TO_D)


def MUNICH_KEY_I_D(I, D):
    return MUNICH_KEY(I, 0, D)


def MUNICH_KEY_I(I):
    return MUNICH_KEY(I, 0, 0)


def GET_MUNICH_I(key):
    return key & _I_MASK


def GET_MUNICH_F(key):
    return key & _F_MASK


def GET_MUNICH_D(key):
    return key & _D_MASK


def GET_RETINA_I(key):
    return key & RETINA_WITHOUT_UART_MASK


def GET_PUSH_BOT_LASER_LED_SPEAKER_FREQUENCY_I(key):
    return GET_MUNICH_I(key)


def GET_PUSH_BOT_MOTOR_I(key):
    return key & PUSH_BOT_MOTOR_WITHOUT_UART_MASK


# Specific fields in the key
_SENSOR_OUTGOING_OFFSET_TO_D = 2
_SENSOR_OUTGOING_OFFSET_TO_I = 7

# Payload fields
_PAYLOAD_OFFSET_FOR_TIMESTAMPS = 29
_PAYLOAD_OFFSET_FOR_RETINA_SIZE = 26
_PAYLOAD_SENSOR_ID_OFFSET = 27
_PAYLOAD_OFFSET_FOR_SENSOR_TIME = 0

# command key for setting up the master key of the board
CONFIGURE_MASTER_KEY = MUNICH_KEY_I_D(127, 0)

# command key for setting up what mode of device running on the board
CHANGE_MODE = MUNICH_KEY_I_D(127, 1)

# command for turning off retina output
DISABLE_RETINA_EVENT_STREAMING = MUNICH_KEY_I_D(0, 0)

# command for retina where payload is events
ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION = MUNICH_KEY_I_D(0, 1)

# command for retina where events are the key
ACTIVE_RETINA_EVENT_STREAMING_SET_KEY = MUNICH_KEY_I_D(0, 2)

# set timer / counter for timestamps
SET_TIMER_COUNTER_FOR_TIMESTAMPS = MUNICH_KEY_I_D(0, 3)

# handle master / slave time sync
MASTER_SLAVE_KEY = MUNICH_KEY_I_D(0, 4)

# command for setting bias (whatever the check that is)
BIAS_KEY = MUNICH_KEY_I_D(0, 5)

# reset retina key.
RESET_RETINA_KEY = MUNICH_KEY_I_D(0, 7)

# request on-board sensor data
SENSOR_REPORTING_OFF_KEY = MUNICH_KEY_I_D(1, 0)

# poll sensors once
POLL_SENSORS_ONCE_KEY = MUNICH_KEY_I_D(1, 1)

# poll sensors continuously
POLL_SENSORS_CONTINUOUSLY_KEY = MUNICH_KEY_I_D(1, 2)

# disable motor
ENABLE_DISABLE_MOTOR_KEY = MUNICH_KEY_I_D(2, 0)

# run motor for total period
MOTOR_RUN_FOR_PERIOD_KEY = MUNICH_KEY_I_D(2, 1)

# raw output for motor 0 (permanent)
MOTOR_0_RAW_PERM_KEY = MUNICH_KEY_I_D(2, 4)

# raw output for motor 1 (permanent)
MOTOR_1_RAW_PERM_KEY = MUNICH_KEY_I_D(2, 5)

# raw output for motor 0 (leak towards 0)
MOTOR_0_RAW_LEAK_KEY = MUNICH_KEY_I_D(2, 6)

# raw output for motor 1 (leak towards 0)
MOTOR_1_RAW_LEAK_KEY = MUNICH_KEY_I_D(2, 7)

# motor output duration timer period
MOTOR_TIMER_A_TOTAL_PERIOD_KEY = MUNICH_KEY_I_D(3, 0)
MOTOR_TIMER_B_TOTAL_PERIOD_KEY = MUNICH_KEY_I_D(3, 2)
MOTOR_TIMER_C_TOTAL_PERIOD_KEY = MUNICH_KEY_I_D(3, 4)

# motor output ratio active period
MOTOR_TIMER_A_CHANNEL_0_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 0)
MOTOR_TIMER_A_CHANNEL_1_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 1)
MOTOR_TIMER_B_CHANNEL_0_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 2)
MOTOR_TIMER_B_CHANNEL_1_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 3)
MOTOR_TIMER_C_CHANNEL_0_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 4)
MOTOR_TIMER_C_CHANNEL_1_ACTIVE_PERIOD_KEY = MUNICH_KEY_I_D(4, 5)

# digital IO Signals
QUERY_STATES_LINES_KEY = MUNICH_KEY_I_D(5, 0)

# set output pattern to payload
SET_OUTPUT_PATTERN_KEY = MUNICH_KEY_I_D(5, 1)

# add payload (logic or (PL)) to current output
ADD_PAYLOAD_TO_CURRENT_OUTPUT_KEY = MUNICH_KEY_I_D(5, 2)

# remove payload (logic or (PL)) to current output from current output
REMOVE_PAYLOAD_TO_CURRENT_OUTPUT_KEY = MUNICH_KEY_I_D(5, 3)

# set payload pins to high impedance
SET_PAYLOAD_TO_HIGH_IMPEDANCE_KEY = MUNICH_KEY_I_D(5, 4)

# set laser params for pushbot
PUSH_BOT_LASER_CONFIG_TOTAL_PERIOD = MUNICH_KEY_I_D(4, 0)
PUSH_BOT_LASER_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 0)
PUSH_BOT_LASER_FREQUENCY = MUNICH_KEY_I_D(37, 1)

# set led params for pushbot
PUSH_BOT_LED_CONFIG_TOTAL_PERIOD = MUNICH_KEY_I_D(4, 4)
PUSH_BOT_LED_BACK_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 4)
PUSH_BOT_LED_FRONT_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 5)
PUSH_BOT_LED_FREQUENCY = MUNICH_KEY_I_D(37, 0)

# set speaker params for pushbot
PUSH_BOT_SPEAKER_CONFIG_TOTAL_PERIOD = MUNICH_KEY_I_D(4, 2)
PUSH_BOT_SPEAKER_CONFIG_ACTIVE_TIME = MUNICH_KEY_I_D(5, 2)
PUSH_BOT_SPEAKER_TONE_BEEP = MUNICH_KEY_I_D(36, 0)
PUSH_BOT_SPEAKER_TONE_MELODY = MUNICH_KEY_I_D(36, 1)

# pushbot motor control
PUSH_BOT_MOTOR_0_PERMANENT_VELOCITY = MUNICH_KEY_I_D(32, 0)
PUSH_BOT_MOTOR_1_PERMANENT_VELOCITY = MUNICH_KEY_I_D(32, 1)
PUSH_BOT_MOTOR_0_LEAKY_VELOCITY = MUNICH_KEY_I_D(32, 2)
PUSH_BOT_MOTOR_1_LEAKY_VELOCITY = MUNICH_KEY_I_D(32, 3)

# payload for setting different time stamp sizes
PAYLOAD_NO_TIMESTAMPS = (0 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
PAYLOAD_DELTA_TIMESTAMPS = (1 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
PAYLOAD_TWO_BYTE_TIME_STAMPS = (2 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
PAYLOAD_THREE_BYTE_TIME_STAMPS = (3 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)
PAYLOAD_FOUR_BYTE_TIME_STAMPS = (4 << _PAYLOAD_OFFSET_FOR_TIMESTAMPS)

# payload for retina size
PAYLOAD_RETINA_NO_DOWN_SAMPLING_IN_PAYLOAD = (
    0 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
PAYLOAD_RETINA_NO_DOWN_SAMPLING = (1 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
PAYLOAD_RETINA_64_DOWN_SAMPLING = (2 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
PAYLOAD_RETINA_32_DOWN_SAMPLING = (3 << _PAYLOAD_OFFSET_FOR_RETINA_SIZE)
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

    def __init__(self, mode, instance_key=None, uart_id=0):
        """

        :param mode: The mode of operation of the protocol
        :param instance_key: The optional instance key to use
        :param uart_id: The id of the UART when needed
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

        self._uart_id = uart_id

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

    def _get_key(self, command, offset_to_uart_id=None):
        if offset_to_uart_id is None:
            return command | self._instance_key
        return (
            command | self._instance_key |
            (self._uart_id << offset_to_uart_id)
        )

    @property
    def configure_master_key_key(self):
        return self._get_key(CONFIGURE_MASTER_KEY)

    def configure_master_key(self, new_key, time=None):
        return MultiCastCommand(
            key=self.configure_master_key_key, payload=new_key, time=time)

    @property
    def set_mode_key(self):
        return self._get_key(CHANGE_MODE)

    def set_mode(self, time=None):
        MunichIoSpiNNakerLinkProtocol.sent_mode_command = True
        return MultiCastCommand(
            key=self.set_mode_key, payload=self._mode.value(), time=time)

    @property
    def set_retina_key_key(self):
        return self._get_key(
            ACTIVE_RETINA_EVENT_STREAMING_SET_KEY, RETINA_UART_SHIFT)

    def set_retina_key(self, new_key, time=None):
        return MultiCastCommand(
            key=self.set_retina_key_key,
            payload=new_key, time=time)

    @property
    def disable_retina_key(self):
        return self._get_key(DISABLE_RETINA_EVENT_STREAMING, RETINA_UART_SHIFT)

    def disable_retina(self, time=None):
        return MultiCastCommand(key=self._disable_retina_key, time=time)

    @property
    def master_slave_key(self):
        return self._get_key(MASTER_SLAVE_KEY, RETINA_UART_SHIFT)

    def master_slave_use_internal_counter(self, time=None):
        return MultiCastCommand(
            key=self._master_slave_key,
            payload=_PAYLOAD_MASTER_SLAVE_USE_INTERNAL_COUNTER, time=time)

    def master_slave_set_slave(self, time=None):
        return MultiCastCommand(
            key=self._master_slave_key,
            payload=_PAYLOAD_MASTER_SLAVE_SET_SLAVE, time=time)

    def master_slave_set_master_clock_not_started(self, time=None):
        return MultiCastCommand(
            key=self._master_slave_key,
            payload=_PAYLOAD_MASTER_SLAVE_SET_MASTER_CLOCK_NOT_STARTED,
            time=time)

    def master_slave_set_master_clock_active(self, time=None):
        return MultiCastCommand(
            key=self._master_slave_key,
            payload=_PAYLOAD_MASTER_SLAVE_SET_MASTER_CLOCK_ACTIVE,
            time=time)

    @property
    def bias_values_key(self):
        return self._get_key(BIAS_KEY, RETINA_UART_SHIFT)

    def bias_values(self, bias_id, bias_value, time=None):
        return MultiCastCommand(
            key=self.bias_values_key,
            payload=((bias_id << 0) | (bias_value << 8)), time=time)

    @property
    def reset_retina_key(self):
        return self._get_key(RESET_RETINA_KEY, RETINA_UART_SHIFT)

    def reset_retina(self, uart_id=0, time=None):
        return MultiCastCommand(
            key=self.reset_retina_key(uart_id), time=time)

    @property
    def turn_off_sensor_reporting_key(self):
        return self._get_key(SENSOR_REPORTING_OFF_KEY)

    def turn_off_sensor_reporting(self, sensor_id, time=None):
        return MultiCastCommand(
            key=self.turn_off_sensor_reporting_key,
            payload=(sensor_id << _PAYLOAD_SENSOR_ID_OFFSET), time=time)

    @property
    def poll_sensors_once_key(self):
        return self._get_key(POLL_SENSORS_ONCE_KEY)

    def poll_sensors_once(self, sensor_id, time=None):
        return MultiCastCommand(
            key=self.poll_sensors_once_key,
            payload=(sensor_id << _PAYLOAD_SENSOR_ID_OFFSET), time=time)

    @property
    def poll_individual_sensor_continuously_key(self):
        return self._get_key(POLL_SENSORS_CONTINUOUSLY_KEY)

    def poll_individual_sensor_continuously(
            self, sensor_id, time_in_ms, time=None):
        return MultiCastCommand(
            key=self.poll_individual_sensor_continuously_key,
            payload=((sensor_id << _PAYLOAD_SENSOR_ID_OFFSET) |
                     (time_in_ms << _PAYLOAD_OFFSET_FOR_SENSOR_TIME)),
            time=time)

    @property
    def enable_disable_motor_key(self):
        return self._get_key(ENABLE_DISABLE_MOTOR_KEY, RETINA_UART_SHIFT)

    def generic_motor_enable(self, time=None):
        return MultiCastCommand(
            key=self.enable_disable_motor_key, payload=1, time=time)

    def generic_motor_disable(self, time=None):
        return MultiCastCommand(
            key=self.enable_disable_motor_key, payload=0, time=time)

    @property
    def generic_motor_total_period_key(self):
        return self._get_key(MOTOR_RUN_FOR_PERIOD_KEY, RETINA_UART_SHIFT)

    def generic_motor_total_period(
            self, time_in_ms, uart_id=0, time=None):
        return MultiCastCommand(
            key=self._generic_motor_total_period_key,
            payload=time_in_ms, time=time)

    @property
    def generic_motor0_raw_output_permanent_key(self):
        return self._get_key(MOTOR_0_RAW_PERM_KEY, RETINA_UART_SHIFT)

    def generic_motor0_raw_output_permanent(self, pwm_signal, time=None):
        return MultiCastCommand(
            key=self.generic_motor0_raw_output_permanent_key,
            payload=pwm_signal, time=time)

    @property
    def generic_motor1_raw_output_permanent_key(self):
        return self._get_key(MOTOR_1_RAW_PERM_KEY, RETINA_UART_SHIFT)

    def generic_motor1_raw_output_permanent(self, pwm_signal, time=None):
        return MultiCastCommand(
            key=self.generic_motor1_raw_output_permanent_key,
            payload=pwm_signal, time=time)

    @property
    def generic_motor0_raw_output_leak_to_0_key(self):
        return self._get_key(MOTOR_0_RAW_LEAK_KEY, RETINA_UART_SHIFT)

    def generic_motor0_raw_output_leak_to_0(self, pwm_signal, time=None):
        return MultiCastCommand(
            key=self.generic_motor0_raw_output_leak_to_0_key,
            payload=pwm_signal, time=time)

    @property
    def generic_motor1_raw_output_leak_to_0_key(self):
        return self._get_key(MOTOR_1_RAW_LEAK_KEY, RETINA_UART_SHIFT)

    def generic_motor1_raw_output_leak_to_0(self, pwm_signal, time=None):
        return MultiCastCommand(
            key=self.generic_motor1_raw_output_leak_to_0_key,
            payload=pwm_signal, time=time)

    @property
    def pwm_pin_output_timer_a_duration_key(self):
        return self._get_key(MOTOR_TIMER_A_TOTAL_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_a_duration(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_a_duration_key,
            payload=timer_period, time=time)

    @property
    def pwm_pin_output_timer_b_duration_key(self):
        return self._get_key(MOTOR_TIMER_B_TOTAL_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_b_duration(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_b_duration_key,
            payload=timer_period, time=time)

    @property
    def pwm_pin_output_timer_c_duration_key(self):
        return self._get_key(MOTOR_TIMER_C_TOTAL_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_c_duration(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_c_duration_key,
            payload=timer_period, time=time)

    @property
    def pwm_pin_output_timer_a_channel_0_ratio_key(self):
        return self._get_key(
            MOTOR_TIMER_A_CHANNEL_0_ACTIVE_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_a_channel_0_ratio(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_a_channel_0_ratio_key,
            payload=timer_period, time=time)

    @property
    def pwm_pin_output_timer_a_channel_1_ratio_key(self):
        return self._get_key(
            MOTOR_TIMER_A_CHANNEL_1_ACTIVE_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_a_channel_1_ratio(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_a_channel_1_ratio_key,
            payload=timer_period, time=time)

    def pwm_pin_output_timer_b_channel_0_ratio_key(self):
        return self._get_key(
            MOTOR_TIMER_B_CHANNEL_0_ACTIVE_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_b_channel_0_ratio(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_b_channel_0_ratio_key,
            payload=timer_period, time=time)

    @property
    def pwm_pin_output_timer_b_channel_1_ratio_key(self):
        return self._get_key(
            MOTOR_TIMER_B_CHANNEL_1_ACTIVE_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_b_channel_1_ratio(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_b_channel_1_ratio_key,
            payload=timer_period, time=time)

    @property
    def pwm_pin_output_timer_c_channel_0_ratio_key(self):
        return self._get_key(
            MOTOR_TIMER_C_CHANNEL_0_ACTIVE_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_c_channel_0_ratio(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_c_channel_0_ratio_key,
            payload=timer_period, time=time)

    def pwm_pin_output_timer_c_channel_1_ratio_key(self):
        return self._get_key(
            MOTOR_TIMER_C_CHANNEL_1_ACTIVE_PERIOD_KEY, RETINA_UART_SHIFT)

    def pwm_pin_output_timer_c_channel_1_ratio(self, timer_period, time=None):
        return MultiCastCommand(
            key=self.pwm_pin_output_timer_c_channel_1_ratio_key,
            payload=timer_period, time=time)

    @property
    def query_state_of_io_lines_key(self):
        return self._get_key(QUERY_STATES_LINES_KEY)

    def query_state_of_io_lines(self, time=None):
        return MultiCastCommand(
            key=self.query_state_of_io_lines_key, time=time)

    @property
    def set_output_pattern_for_payload_key(self):
        return self._get_key(SET_OUTPUT_PATTERN_KEY)

    def set_output_pattern_for_payload(self, payload, time=None):
        return MultiCastCommand(
            key=self.set_output_pattern_for_payload_key, payload=payload,
            time=time)

    @property
    def add_payload_logic_to_current_output_key(self):
        return self._get_key(ADD_PAYLOAD_TO_CURRENT_OUTPUT_KEY)

    def add_payload_logic_to_current_output(self, payload, time=None):
        return MultiCastCommand(
            key=self.add_payload_logic_to_current_output_key,
            payload=payload, time=time)

    @property
    def remove_payload_logic_to_current_output_key(self):
        return self._get_key(REMOVE_PAYLOAD_TO_CURRENT_OUTPUT_KEY)

    def remove_payload_logic_to_current_output(self, payload, time=None):
        return MultiCastCommand(
            key=self.remove_payload_logic_to_current_output_key,
            payload=payload, time=time)

    @property
    def set_payload_pins_to_high_impedance_key(self):
        return self._get_key(SET_PAYLOAD_TO_HIGH_IMPEDANCE_KEY)

    def set_payload_pins_to_high_impedance(self, payload, time=None):
        return MultiCastCommand(
            key=self.set_payload_pins_to_high_impedance_key,
            payload=payload, time=time)

    def _check_for_pushbot_mode(self):
        if self._mode is not self.MODES.PUSH_BOT:
            raise exceptions.ConfigurationException(
                "The mode you configured is not the pushbot, and so this "
                "message is invalid for mode {}".format(self._mode))

    @property
    def push_bot_laser_config_total_period_key(self):
        return self._get_key(
            PUSH_BOT_LASER_CONFIG_TOTAL_PERIOD, RETINA_UART_SHIFT)

    def push_bot_laser_config_total_period(self, total_period, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_laser_config_total_period_key,
            payload=total_period, time=time)

    @property
    def push_bot_laser_config_active_time_key(self):
        return self._get_key(
            PUSH_BOT_LASER_CONFIG_ACTIVE_TIME, RETINA_UART_SHIFT)

    def push_bot_laser_config_active_time(self, active_time, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_laser_config_active_time_key,
            payload=active_time, time=time)

    @property
    def push_bot_laser_set_frequency_key(self):
        return self._get_key(
            PUSH_BOT_LASER_FREQUENCY,
            PUSH_BOT_LASER_LED_SPEAKER_FREQUENCY_UART_SHIFT)

    def push_bot_laser_set_frequency(self, frequency, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_laser_set_frequency_key,
            payload=frequency, time=time)

    @property
    def push_bot_speaker_config_total_period_key(self):
        return self._get_key(
            PUSH_BOT_SPEAKER_CONFIG_TOTAL_PERIOD, RETINA_UART_SHIFT)

    def push_bot_speaker_config_total_period(
            self, total_period, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_speaker_config_total_period_key,
            payload=total_period, time=time)

    @property
    def push_bot_speaker_config_active_time_key(self):
        return self._get_key(
            PUSH_BOT_SPEAKER_CONFIG_ACTIVE_TIME, RETINA_UART_SHIFT)

    def push_bot_speaker_config_active_time(self, active_time, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_speaker_config_active_time_key,
            payload=active_time, time=time)

    @property
    def push_bot_speaker_set_tone_key(self):
        return self._get_key(
            PUSH_BOT_SPEAKER_TONE_BEEP,
            PUSH_BOT_LASER_LED_SPEAKER_FREQUENCY_UART_SHIFT)

    def push_bot_speaker_set_tone(self, frequency, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_speaker_set_tone_key,
            payload=frequency, time=time)

    @property
    def push_bot_speaker_set_melody_key(self):
        return self._get_key(
            PUSH_BOT_SPEAKER_TONE_MELODY,
            PUSH_BOT_LASER_LED_SPEAKER_FREQUENCY_UART_SHIFT)

    def push_bot_speaker_set_melody(self, melody, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_speaker_set_melody_key,
            payload=melody, time=time)

    @property
    def push_bot_led_total_period_key(self):
        return self._get_key(
            PUSH_BOT_LED_CONFIG_TOTAL_PERIOD, RETINA_UART_SHIFT)

    def push_bot_led_total_period(self, total_period, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_led_total_period_key,
            payload=total_period, time=time)

    @property
    def push_bot_led_back_active_time_key(self):
        return self._get_key(
            PUSH_BOT_LED_BACK_CONFIG_ACTIVE_TIME, RETINA_UART_SHIFT)

    def push_bot_led_back_active_time(self, active_time, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_led_back_active_time_key,
            payload=active_time, time=time)

    @property
    def push_bot_led_front_active_time_key(self):
        return self._get_key(
            PUSH_BOT_LED_FRONT_CONFIG_ACTIVE_TIME, RETINA_UART_SHIFT)

    def push_bot_led_front_active_time(self, active_time, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_led_front_active_time_key,
            payload=active_time, time=time)

    @property
    def push_bot_led_set_frequency_key(self):
        return self._get_key(
            PUSH_BOT_LED_FREQUENCY,
            PUSH_BOT_LASER_LED_SPEAKER_FREQUENCY_UART_SHIFT)

    def push_bot_led_set_frequency(self, frequency, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_led_set_frequency_key,
            payload=frequency, time=time)

    @property
    def push_bot_motor_0_permanent_key(self):
        return self._get_key(
            PUSH_BOT_MOTOR_0_PERMANENT_VELOCITY, PUSH_BOT_MOTOR_UART_SHIFT)

    def push_bot_motor_0_permanent(self, velocity, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_motor_0_permanent_key,
            payload=velocity, time=time)

    @property
    def push_bot_motor_1_permanent_key(self):
        return self._get_key(
            PUSH_BOT_MOTOR_1_PERMANENT_VELOCITY, PUSH_BOT_MOTOR_UART_SHIFT)

    def push_bot_motor_1_permanent(self, velocity, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_motor_1_permanent_key,
            payload=velocity, time=time)

    @property
    def push_bot_motor_0_leaking_towards_zero_key(self):
        return self._get_key(
            PUSH_BOT_MOTOR_0_LEAKY_VELOCITY, PUSH_BOT_MOTOR_UART_SHIFT)

    def push_bot_motor_0_leaking_towards_zero(self, velocity, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_motor_0_leaking_towards_zero_key,
            payload=velocity, time=time)

    @property
    def push_bot_motor_1_leaking_towards_zero_key(self):
        return self._get_key(
            PUSH_BOT_MOTOR_1_LEAKY_VELOCITY, PUSH_BOT_MOTOR_UART_SHIFT)

    def push_bot_motor_1_leaking_towards_zero(self, velocity, time=None):
        self._check_for_pushbot_mode()
        return MultiCastCommand(
            key=self.push_bot_motor_1_leaking_towards_zero_key,
            payload=velocity, time=time)

    def sensor_transmission_key(self, sensor_id):
        return ((sensor_id << _SENSOR_OUTGOING_OFFSET_TO_D) |
                (self._uart_id << _SENSOR_OUTGOING_OFFSET_TO_I))

    @property
    def set_retina_transmission_key(self):
        return self._get_key(
            ACTIVE_RETINA_EVENT_STREAMING_KEYS_CONFIGURATION,
            RETINA_UART_SHIFT)

    def set_retina_transmission(
            self, events_in_key=True, retina_pixels=128 * 128,
            payload_holds_time_stamps=False, size_of_time_stamp_in_bytes=None,
            time=None, repeat=0, delay=0):

        # if events in the key.
        if events_in_key:
            if not payload_holds_time_stamps:

                # not using payloads
                return self._key_retina(
                    retina_pixels, PAYLOAD_NO_TIMESTAMPS, time, repeat, delay)
            else:

                # using payloads
                if size_of_time_stamp_in_bytes == 0:
                    return self._key_retina(
                        retina_pixels, PAYLOAD_DELTA_TIMESTAMPS,
                        time, repeat, delay)
                if size_of_time_stamp_in_bytes == 2:
                    return self._key_retina(
                        retina_pixels, PAYLOAD_TWO_BYTE_TIME_STAMPS,
                        time, repeat, delay)
                if size_of_time_stamp_in_bytes == 3:
                    return self._key_retina(
                        retina_pixels, PAYLOAD_THREE_BYTE_TIME_STAMPS,
                        time, repeat, delay)
                if size_of_time_stamp_in_bytes == 4:
                    return self._key_retina(
                        retina_pixels, PAYLOAD_FOUR_BYTE_TIME_STAMPS,
                        time, repeat, delay)
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
                key=self.set_retina_transmission_key,
                payload=(PAYLOAD_NO_TIMESTAMPS |
                         PAYLOAD_RETINA_NO_DOWN_SAMPLING_IN_PAYLOAD),
                time=time, repeat=repeat, delay_between_repeats=delay)

    def _key_retina(
            self, retina_pixels, time_stamps, time, repeat, delay):
        if retina_pixels == 128 * 128:
            return MultiCastCommand(
                key=self.set_retina_transmission_key,
                payload=(time_stamps | PAYLOAD_RETINA_NO_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        if retina_pixels == 64 * 64:
            return MultiCastCommand(
                key=self.set_retina_transmission_key,
                payload=(time_stamps | PAYLOAD_RETINA_64_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        if retina_pixels == 32 * 32:
            return MultiCastCommand(
                key=self.set_retina_transmission_key,
                payload=(time_stamps | PAYLOAD_RETINA_32_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        if retina_pixels == 16 * 16:
            return MultiCastCommand(
                key=self.set_retina_transmission_key,
                payload=(time_stamps | _PAYLOAD_RETINA_16_DOWN_SAMPLING),
                time=time, repeat=repeat, delay_between_repeats=delay)
        else:
            raise exceptions.ConfigurationException(
                "The no of pixels is not supported in this protocol.")
