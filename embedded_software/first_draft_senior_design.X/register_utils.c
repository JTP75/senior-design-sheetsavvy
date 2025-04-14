#include "register_utils.h"

uint16_t analog_read() {
    static uint16_t value;
    AD1CON1bits.SAMP = 0x01;            //tells it to start sampling
    __delay_us(1);
    AD1CON1bits.SAMP = 0x00;            //stop sampling, start converting
    while(AD1CON1bits.DONE == 0x00) {}
    value = ADC1BUF0;
    return value;
}

