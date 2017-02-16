#ifndef _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_
#define _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_

#include "neuron/threshold_types/threshold_type.h"
#include <spin1_api.h>

typedef struct threshold_type_t {

    // The key to send to update the value
    uint32_t key;

    // True (1) if the value is to be sent as payload, False (0) if just the key
    uint32_t value_as_payload;

    // The minimum allowed value to send as the payload.
    // Values below are clipped to this value
    accum min_value;

    // The maximum allowed value to send as the payload.
    // Values above are clipped to this value
    accum max_value;

    // The time between sending the value
    uint32_t timesteps_between_sending;

    // The time until the next sending of the value (initially 0)
    uint32_t time_until_next_send;

} threshold_type_t;


static bool threshold_type_is_above_threshold(
        state_t value, threshold_type_pointer_t threshold_type) {

    if (threshold_type->time_until_next_send == 0) {

        if (threshold_type->value_as_payload) {

            accum value_to_send = value;
            if (value > threshold_type->max_value) {
                value_to_send = threshold_type->max_value;
            }
            if (value < threshold_type->min_value) {
                value_to_send = threshold_type->min_value;
            }

            while (!spin1_send_mc_packet(
                        threshold_type->key, value_to_send, WITH_PAYLOAD)) {
                spin1_delay_us(1);
            }
        } else {
            while (!spin1_send_mc_packet(
                        threshold_type->key, 0, NO_PAYLOAD)) {
                spin1_delay_us(1);
            }
        }

        threshold_type->time_until_next_send =
                threshold_type->timesteps_between_sending;
    } else {
        --threshold_type->time_until_next_send;
    }
    return false;
}

#endif // _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_
