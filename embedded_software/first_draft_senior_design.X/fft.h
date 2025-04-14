/* 
 * File:   fft.h
 * Author: Evelyn
 *
 * Created on September 17, 2024, 4:54 PM
 */



#include "dsp.h"
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <xc.h>


void FFT_fft(int samples[1000], int sampling_rate, int * spectrum, int * frequencies);