#ifndef _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_
#define _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_

#include "neuron/threshold_types/threshold_type.h"
#include "../munich_protocol.h"
#include <spin1_api.h>

typedef struct threshold_type_t {

    // the command identifier
    uint32_t     command_id;

    // the UART to send to
    uint32_t     uart_id;

    // The ignored part of the key to add
    uint32_t     instance_key;
} threshold_type_t;

//! human readable definitions of each neuron id command
typedef enum atom_id_map {           // atom id from python
    MOTOR_0_PERM = 1,                // 0
    MOTOR_0_LEAKY = 2,               // 1
    MOTOR_1_PERM = 4,                // 2
    MOTOR_1_LEAKY = 8,               // 3
    LASER_TOTAL_PERIOD = 16,         // 4
    SPEAKER_TOTAL_PERIOD = 32,       // 5
    LED_TOTAL_PERIOD = 64,           // 6
    LASER_ACTIVE_TIME = 128,         // 7
    SPEAKER_ACTIVE_TIME = 256,       // 8
    LED_FRONT_ACTIVE_TIME = 512,     // 9
    LED_BACK_ACTIVE_TIME = 1024,     // 10
    SPEAKER_TONE_FREQUENCY = 2048,   // 11
    SPEAKER_MELODY = 4096,           // 12
    LED_FREQUENCY= 8192,             // 13
    LASER_FREQUENCY = 16384          // 14
} atom_id_map;


static void send_packet(multicast_packet packet){
    while (!spin1_send_mc_packet(
            packet.key, packet.payload, packet.payload_flag)) {
        spin1_delay_us(1);
    }
}

static bool threshold_type_is_above_threshold(
        state_t value, threshold_type_pointer_t threshold_type){

    // set the protocol mode for checks
    set_protocol_mode(MUNICH_PROTOCOL_PUSH_BOT, threshold_type->instance_key);

    // go through the types of messages are fire as needed
    switch (threshold_type->command_id) {

    case MOTOR_0_PERM:
        send_packet(munich_protocol_push_bot_motor_0_permanent(
            value, threshold_type->uart_id));
        break;

    case MOTOR_0_LEAKY:
        send_packet(munich_protocol_push_bot_motor_0_leaking_towards_zero(
            value, threshold_type->uart_id));
        break;

    case MOTOR_1_PERM:
        send_packet(munich_protocol_push_bot_motor_1_permanent(
            value, threshold_type->uart_id));
        break;

    case MOTOR_1_LEAKY:
        send_packet(munich_protocol_push_bot_motor_1_leaking_towards_zero(
            value, threshold_type->uart_id));
        break;

    case LASER_TOTAL_PERIOD:
        send_packet(munich_protocol_push_bot_laser_config_total_period(
            value, threshold_type->uart_id));
        break;

    case SPEAKER_TOTAL_PERIOD:
        send_packet(munich_protocol_push_bot_speaker_config_total_period(
            value, threshold_type->uart_id));
        break;

    case LED_TOTAL_PERIOD:
        send_packet(munich_protocol_push_bot_led_total_period(
            value, threshold_type->uart_id));
        break;

    case LASER_ACTIVE_TIME:
        send_packet(munich_protocol_push_bot_laser_config_active_time(
            value, threshold_type->uart_id));
        break;

    case SPEAKER_ACTIVE_TIME:
        send_packet(munich_protocol_push_bot_speaker_config_active_time(
            value, threshold_type->uart_id));
        break;

    case LED_FRONT_ACTIVE_TIME:
        send_packet(munich_protocol_push_bot_led_front_active_time(
            value, threshold_type->uart_id));
        break;

    case LED_BACK_ACTIVE_TIME:
        send_packet(munich_protocol_push_bot_led_back_active_time(
            value, threshold_type->uart_id));
        break;

    case SPEAKER_TONE_FREQUENCY:
        send_packet(munich_protocol_push_bot_speaker_set_tone(
            value, threshold_type->uart_id));
        break;

    case SPEAKER_MELODY:
        send_packet(munich_protocol_push_bot_speaker_set_melody(
            value, threshold_type->uart_id));
        break;

    case LED_FREQUENCY:
        send_packet(munich_protocol_push_bot_led_set_frequency(
            value, threshold_type->uart_id));
        break;

    case LASER_FREQUENCY:
        send_packet(munich_protocol_push_bot_laser_set_frequency(
            value, threshold_type->uart_id));
        break;

    default:
        break;
    }
    return false;
}

#endif // _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_
