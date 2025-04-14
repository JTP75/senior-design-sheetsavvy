/* 
 * File:   user.h
 * Author: Evelyn
 *
 * Created on September 11, 2024, 5:12 PM
 */


#include "dsp.h"
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <xc.h>

void INIT(void);
void INIT_OSC(void);
void INIT_ADC(void);
void INIT_ADC_V2(void);
void IO_LED(void);
void INIT_UART(void);
void UART_SEND_ARRAY(char[], int);
void UART_SEND_CHAR(uint8_t);
void INIT_PPS(void);
void INIT_PWM(void);
void INIT_I2C(void);
void I2C_send(uint8_t);