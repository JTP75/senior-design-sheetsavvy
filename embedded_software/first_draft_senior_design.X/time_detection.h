/* 
 * File:   time_detection.h
 * Author: pacel
 *
 * Created on October 7, 2024, 5:17 PM
 */

#ifndef TIME_DETECTION_H
#define	TIME_DETECTION_H

#ifndef IMPORTANT_CONSTANTS
#define IMPORTANT_CONSTANTS
    #define FCY 8000000UL                   //CLOCK FREQUENCY
    #define SAMPLING_FREQUENCY_HZ  7500     //ADC SAMPLING FREQUENCY
    #define FFT_SIZE 1024
#endif

#define MIN_DURATION_SMPL 300
#define RMS_THRESHOLD 1.0

#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <dsp.h>
#include <libq.h>
#include <time.h>

#include "fft_utils.h"

#ifdef	__cplusplus
extern "C" {
#endif
    
    /**
     * 
     * @param sample_num
     * @param peak
     * @param rms
     * @param onset
     * @param release
     */
    void detect_timings(uint64_t sample_num, 
            float peak_freq, 
            float rms, 
            time_t * onset, 
            time_t * release);
    
    /**
     * obtains frequency tolerance band at given frequency 
     * 
     * @param frequency current peak frequency (IN DECIHERTZ)
     * @return +/- tolerance (DECIHERTZ)
     */
    float get_tolerance_at(float frequency);
    
    // dr youngblud : upsampling could help save computational power

#ifdef	__cplusplus
}
#endif

#endif	/* TIME_DETECTION_H */

