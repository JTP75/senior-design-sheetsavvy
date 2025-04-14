/* 
 * File:   fft_utils.h
 * Author: pacel
 *
 * Created on October 30, 2024, 6:10 PM
 */

#ifndef FFT_UTILS_H
#define	FFT_UTILS_H

#ifndef IMPORTANT_CONSTANTS
#define IMPORTANT_CONSTANTS
    #define FCY 8000000UL                   //CLOCK FREQUENCY
    #define SAMPLING_FREQUENCY_HZ  7500     //ADC SAMPLING FREQUENCY
    #define FFT_SIZE 1024                   //FFT WINDOW SIZE
    #define FFT_SIZE_LOG2 10                //FFT WINDOW SIZE LOG2
#endif

#include <stdint.h>

#include <libpic30.h>
#include <p33EV256GM002.h>
#include <xc.h>
#include <dsp.h>
#include <libq.h>

#ifdef	__cplusplus
extern "C" {
#endif
    
    // this is the address of the twiddle factors (points to x memory)
    extern const int factPage;  
    
    //window that needs to exist for either hamming or hanning window
//    extern fractional window[512];

    // twiddle factor array (const)
    extern fractcomplex twiddleFactors[FFT_SIZE] __attribute__ ((space(xmemory), aligned (1024*2)));

    // fft hardware buffer (volatile)
    extern fractcomplex fftBuffer[FFT_SIZE] __attribute__((space(ymemory), aligned(1024*2*2)));

    // real 32b twiddle factor array (const)
//    extern const long twiddleFactorsR[FFT_SIZE] __attribute__ ((space(xmemory), aligned (1024*2)));

    // real 32b fft hardware buffer (volatile)
//    extern long fftBufferR[FFT_SIZE] __attribute__((space(ymemory), aligned(1024*2*2)));
    
    
    
    
    
    // TODO maybe make inline wrappers for some FFT functions? idk
    

#ifdef	__cplusplus
}
#endif

#endif	/* FFT_UTILS_H */

