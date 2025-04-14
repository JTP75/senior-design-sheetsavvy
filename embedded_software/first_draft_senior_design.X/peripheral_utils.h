/* 
 * File:   peripheral_utils.h
 * Author: Evelyn
 *
 * Created on November 4, 2024, 6:43 PM
 */

#ifndef PERIPHERAL_UTILS_H
#define	PERIPHERAL_UTILS_H

#ifdef	__cplusplus
extern "C" {
#endif

// <editor-fold defaultstate="collapsed" desc="defines">

#ifndef IMPORTANT_CONSTANTS
#define IMPORTANT_CONSTANTS
    #define FCY 8000000UL                   //CLOCK FREQUENCY
    #define SAMPLING_FREQUENCY_HZ  7500     //ADC SAMPLING FREQUENCY
    #define FFT_SIZE 512                    //FFT WINDOW SIZE
    #define FFT_SIZE_LOG2 10                //FFT WINDOW SIZE LOG2
#endif

// </editor-fold>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <libpic30.h>
#include <p33EV256GM002.h>
#include <xc.h>
    
    void InitButtons();
    
    int BpmUpDown(int);    

    bool Time_TwoFour();  
    
    bool Time_ThreeFour();
    
    bool Time_FourFour();
    
    bool StartStop();
    
    
#ifdef	__cplusplus
}
#endif

#endif	/* PERIPHERAL_UTILS_H */

