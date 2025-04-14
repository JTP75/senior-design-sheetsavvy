#include "util.h"
#include <string.h>
#include <assert.h>

#define FLOAT_PRECISION 6

void float2str(float num, char buffer[9]) {
    float decimal_part;
    
    // sign
    if (num < 0) {
        buffer[0] = '-';
        num = -num;
    } else {
        buffer[0] = ' ';
    }

    // integer part
    buffer[1] = (int)num + '0';

    // decimal part
    buffer[2] = '.';
    decimal_part = num-(int)num;
    for (int i=3; i < FLOAT_PRECISION+3; i++) {
        decimal_part *= 10;
        buffer[i] = (int)decimal_part + '0';
        decimal_part -= (int)decimal_part;
    }
}

void fract2str(fractional val, char buffer[9]) {
    float2str(Fract2Float(val), buffer);
}

fractional __divf(fractional a, fractional b) {
    assert(b!=0);
    float af = Fract2Float(a), bf = Fract2Float(b), rf;
    rf = af / bf;
    assert(-1.0<rf && rf<1.0);
    return Float2Fract(rf);
}