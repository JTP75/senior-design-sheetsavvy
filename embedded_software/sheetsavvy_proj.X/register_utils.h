/* 
 * File:   register_utils.h
 * Author: pacel
 *
 * Created on October 30, 2024, 5:41 PM
 */

#ifndef REGISTER_UTILS_H
#define	REGISTER_UTILS_H

#ifndef IMPORTANT_CONSTANTS
#define IMPORTANT_CONSTANTS
    #define FCY 8000000UL                   //CLOCK FREQUENCY
    #define SAMPLING_FREQUENCY_HZ  7500     //ADC SAMPLING FREQUENCY
    #define FFT_SIZE 512                    //FFT WINDOW SIZE
    #define FFT_SIZE_LOG2 10                //FFT WINDOW SIZE LOG2
#endif

#include <stdint.h>

#include <libpic30.h>
#include <p33EV256GM002.h>
#include <xc.h>

#ifdef	__cplusplus
extern "C" {
#endif

    /**
     * reads the analog value from the ADC
     * @return 
     */
    uint16_t analog_read();

#ifdef	__cplusplus
}
#endif

#endif	/* REGISTER_UTILS_H */

