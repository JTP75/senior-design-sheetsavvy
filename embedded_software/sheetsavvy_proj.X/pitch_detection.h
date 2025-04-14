/* 
 * File:   pitch_detection.h
 * Author: pacel
 *
 * Created on October 7, 2024, 5:22 PM
 */

#ifndef PITCH_DETECTION_H
#define	PITCH_DETECTION_H

#ifndef IMPORTANT_CONSTANTS
#define IMPORTANT_CONSTANTS
    #define FCY 8000000UL                   //CLOCK FREQUENCY
    #define SAMPLING_FREQUENCY_HZ  7500     //ADC SAMPLING FREQUENCY
    #define FFT_SIZE 512                    //FFT WINDOW SIZE
    #define FFT_SIZE_LOG2 10                //FFT WINDOW SIZE LOG2
#endif
    
#include <math.h>
#include <dsp.h>

#ifdef	__cplusplus
extern "C" {
#endif

    // TODO define pitch detection functions

#ifdef	__cplusplus
}
#endif

#endif	/* PITCH_DETECTION_H */

