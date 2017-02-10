#ifndef _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_
#define _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_

#include "neuron/threshold_types/threshold_type.h"
#include <spin1_api.h>

typedef struct threshold_type_t {

    // The key to send to update the value
    uint32_t key;

    // True (1) if the value is to be sent as payload, False (0) if just the key
    uint32_t value_as_payload;

} threshold_type_t;


static bool threshold_type_is_above_threshold(
        state_t value, threshold_type_pointer_t threshold_type){

    if (threshold_type->value_as_payload) {
        while (!spin1_send_mc_packet(
                    threshold_type->key, value, WITH_PAYLOAD)) {
            spin1_delay_us(1);
        }
    } else {
        while (!spin1_send_mc_packet(
                    threshold_type->key, 0, NO_PAYLOAD)) {
            spin1_delay_us(1);
        }
    }
    return false;
}

#endif // _THRESHOLD_TYPE_PUSH_BOT_CONTROL_MODULE_H_
