/* 
 * File:   newmain.c
 * Author: Evelyn
 *
 * Created on September 11, 2024, 5:11 PM
 * 
 * MISC NOTES
 * 
 *  adc related:
 * 
 *      unsigned integer 16
 *      8VPP -> 0 to 3116
 *      2VPP -> 0 to 774
 * 
 *      signed integer 16
 *      8VPP -> -2048 to 1066
 *      2VPP -> -2048 to -1
 */

// <editor-fold defaultstate="collapsed" desc="preprocessing config">

#pragma config GWRP = OFF
#pragma config FNOSC = PRI
#pragma config POSCMD = HS
#pragma config OSCIOFNC = OFF
#pragma config FWDTEN = OFF
#pragma config PWMLOCK = OFF 

// </editor-fold>

// <editor-fold defaultstate="collapsed" desc="defines">

#ifndef IMPORTANT_CONSTANTS
#define IMPORTANT_CONSTANTS
    #define FCY 8000000UL                   //CLOCK FREQUENCY
    #define SAMPLING_FREQUENCY_HZ  7500     //ADC SAMPLING FREQUENCY
    #define FFT_SIZE 1024                   //FFT WINDOW SIZE
    #define FFT_SIZE_LOG2 10                //FFT WINDOW SIZE LOG2
#endif

#define OVERLAP_SIZE 512

// </editor-fold>

// <editor-fold defaultstate="collapsed" desc="public library includes">

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>
#include <time.h>
#include <libpic30.h>
#include <p33EV256GM002.h>
#include <xc.h>
#include <dsp.h>
//#include <dsp_factors_32b.h>
#include <libq.h>
//#include <math.h>

// </editor-fold>

// <editor-fold defaultstate="collapsed" desc="private library includes">

#include "profile_config.h"
#include "user.h"
#include "register_utils.h"
#include "fft_utils.h"
#include "time_detection.h"
#include "peripheral_utils.h"
#include "state.h"

// </editor-fold>

// <editor-fold defaultstate="collapsed" desc="function prototypes">

/**
 * prints a string to uart
 * @param s C string ending with null terminator character '\0'
 */
void send_str(char * s);

/**
 * 
 * @param count number of notes to send
 * @param pitches integer numeric pitches of notes
 * @param onsets note onsets timings (milliseconds)
 * @param releases note release timings (milliseconds)
 */
void send_note_data(uint8_t count, uint8_t * pitches, uint32_t * onsets, uint32_t * releases);

/**
 * 
 * @param tempo integer tempo in BPM
 * @param time_sig integer time signature as 2, 3, or 4 (for 2/4, 3/4, and 4/4)
 */
void send_attr_data(uint8_t tempo, uint8_t time_sig);

// </editor-fold>

// <editor-fold defaultstate="collapsed" desc="global variables">
   


// </editor-fold>

// <editor-fold defaultstate="collapsed" desc="main programs">

#ifdef PRODUCTION_CODE
int main() {
    
    INIT();
    __delay_ms(500);
    
    send_str("\rInit Complete!\n\0");
    
    fractional squared_magnitude[FFT_SIZE];
    uint16_t sample_buffer[FFT_SIZE];
    uint16_t adc_max;
    int16_t peak_bin;
    uint16_t peak;
    uint16_t rms;
    
    
    // 64 is temp max note count (avoid dyn mem))
    uint64_t onsets[64], releases[64], onset, release;
    uint8_t onset_size = 0, release_size = 0;
    
    uint64_t sample_num = 0;
    time_t t1_samp=0,t2_samp=0;
    time_t t1_fft=0,t2_fft=0;
    uint64_t delta;
    while (1) {
        
        // 1. fill fftBuffer array with 512 samples (for now assuming step size = window size)
        // 2. perform fft and get peak freq hz
        // 3. call timing detection to find onset and/or release
        // 4. be happy
        
        uint16_t adc_val, center;
        
        for (int i=0; i<FFT_SIZE; i++) {
        time(&t1_samp);
            
                    
            adc_val = analog_read();
            
            if (adc_val > adc_max) { adc_max = adc_val; }
            center = (2*adc_val)/(adc_max - 1);
            
            sample_buffer[i] = adc_val;
            fftBuffer[i].real = Q15(center);
        time(&t2_samp);
        }
        
        time(&t1_fft);
        
        rms = rms_energy(sample_buffer);
        FFTComplexIP(9, (fractcomplex*)&fftBuffer[0], &twiddleFactors[0], factPage);
        BitReverseComplex(9,(fractcomplex*)&fftBuffer[0]);
        SquareMagnitudeCplx(FFT_SIZE, (fractcomplex*)&fftBuffer[0], (fractional*)&squared_magnitude[0]); 
        for (int i=0; i<8; i++) { squared_magnitude[i] = 0; }
        for (int i=18; i<512; i++) { squared_magnitude[i] = 0; } 
        fractional peak_height = VectorMax((FFT_SIZE/2), (fractional*)&squared_magnitude[0], (int16_t*)&peak_bin);
        peak = peak_bin * (SAMPLING_FREQUENCY_HZ/FFT_SIZE);
        detect_timings(sample_num, peak, rms, onset, release);
        
        time(&t2_fft);
        
        sample_num += FFT_SIZE;
        
        delta = (t2_samp-t1_samp)*10/8;
        char buffer_samp[40];
        sprintf(buffer_samp,"\rt_samp = %llu us,\t\0",delta);
        send_str(buffer_samp);
        
        delta = (t2_fft-t1_fft)/8;
        char buffer_fft[40];
        sprintf(buffer_fft,"t_fft = %llu us\n\0",delta);
        send_str(buffer_fft);
    }
    
    int breakpoint = 0;
    int STOP = 0;
    
    return 0;
}
#endif

#ifdef TEST_CODE_1

int main() {

    // setup code
    // =========================================================================
    INIT();
    send_str("\rInit complete!\n\0");
    
    fractional squaredMagnitude[FFT_SIZE];
    fractional fftMaxValue;
    float fftMaxValueFloat;
    int16_t fftMaxValueBin;     
    float peakFrequencyHz;

    //FILLING THE FFT INPUT ARRAY
//    fractional adc_data[FFT_SIZE];
    int16_t v;
    uint16_t max = 2000;
    
    time_t t1,t2;
    uint64_t delta;
    //    double cycles = 0;
//    fractional window[FFT_SIZE];
//    fractional downsampledFF2[512];
//    fractional downsampledFF3[512];
//    fractional downsampledFF4[512];
//    fractional tempMult[512];
    
    fractional rms;
    
    
//    HammingInit(FFT_SIZE, (fractional*)&window[0]);
    TwidFactorInit(10, &twiddleFactors[0], 0);
    
    int i;

    // loop code
    // =========================================================================
    while (1) {

time(&t1);
        for (i=0; i<128; i++) {
            AD1CON1bits.SAMP = 0x01;            //tells it to start sampling
            __delay_us(2);
            AD1CON1bits.SAMP = 0x00;            //stop sampling, start converting
            while(AD1CON1bits.DONE == 0x00) {}
            v = ADC1BUF0;
            
            if (v > max) { max = v; }

            // mapped_value = (original_value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow
            
//            rms = sliding_rms_energy(v + (fractional)0x4000);
//            adc_data[i] = v;
            fftBuffer[i].real = v + (fractional)0x4000; // temporary accommodation for voltage offset
        } // crash -> PC=0x0306, normal exit -> PC=0x0238
time(&t2);
        memmove(&fftBuffer[128], &fftBuffer[0], sizeof fftBuffer - sizeof *fftBuffer);

//        send_str("\rsampling loop complete!\n\0");
//        __delay_ms(10);

        //IMPLEMENT A HANNING WINDOW FOR PREFILTERING
//        VectorWindow(FFT_SIZE, (fractcomplex*)&fftBuffer[0], (fractcomplex*)&fftBuffer[0], (fractional*)&window[0]);

        //COMPUTE THE FFT
        FFTComplexIP(10, (fractcomplex*)&fftBuffer[0], &twiddleFactors[0], 0xFF00);
        BitReverseComplex(10,(fractcomplex*)&fftBuffer[0]);
        SquareMagnitudeCplx(FFT_SIZE, (fractcomplex*)&fftBuffer[0], (fractional*)&squaredMagnitude[0]);
    
    

        //IMPLEMENT HARMONIC PRODUCT SPECTRUM FOR POST FILTERING
    //            for(int x=0; x<512; x++){
    //                if((i%2)==1)
    //                {
    //                  downsampledFF2[x] = squaredMagnitude[x];
    //                }
    //                else if((i%3)==1)
    //                {
    //                  downsampledFF3[x] = squaredMagnitude[x];
    //                }
    //                else if((i%4)==1)
    //                {
    //                  downsampledFF4[x] = squaredMagnitude[x];
    //                }
    //                else
    //                {
    //                   downsampledFF2[x] = 0; 
    //                   downsampledFF3[x] = 0; 
    //                   downsampledFF4[x] = 0;
    //                }
    //                
    //                x++;
    //            }
    //            
    //            VectorMultiply(512, (fractional*)&tempMult[0], (fractional*)&downsampledFF2[0], (fractional*)&squaredMagnitude[0]);
    //            VectorMultiply(512, (fractional*)&tempMult[0], (fractional*)&downsampledFF3[0], (fractional*)&tempMult[0]);
    //            VectorMultiply(512, (fractional*)&squaredMagnitude[0], (fractional*)&downsampledFF4[0], (fractional*)&tempMult[0]);

        //Band Pass Filter
        for (i=0;i<32;i++) { squaredMagnitude[i] = 0; }
        for (i=FFT_SIZE/5;i<FFT_SIZE;i++) { squaredMagnitude[i] = 0; }

        //ONLY LOOK FOR THE PEAK FREQUENCY WITHIN THE DESIRED RANGE
        // ~523Hz TO 1046Hz
        fftMaxValue = VectorMax((FFT_SIZE/2), (fractional*)&squaredMagnitude[0], (int16_t*)&fftMaxValueBin);
        fftMaxValueFloat = Fract2Float(fftMaxValue);

        if (fftMaxValueFloat>0.0001) {
            peakFrequencyHz = fftMaxValueBin * ((float)SAMPLING_FREQUENCY_HZ/(float)FFT_SIZE);
        } else {
            peakFrequencyHz = 0.0;
            fftMaxValueBin = 0;
        }
    
        char buffer[40];
        sprintf(buffer, "\r,%u,%f,%f,\n\0", fftMaxValueBin, (double)peakFrequencyHz, (double)fftMaxValueFloat);
        send_str(buffer);
        
//        delta = t2-t1;
//        char buffer[30];
//        sprintf(buffer, "\rdt = %llu us\n\0", delta/8);
//        send_str(buffer);
        
    } /* main loop */
    return 0;
}

#endif

#ifdef TEST_CODE_2
int main() {
    
    INIT();
    __delay_ms(500);
    
    // state strings for desktop are:
    //      "IDLE"
    //      "COUNTOFF"
    //      "RECORDING"
    //      "SENDING"
    
    int i;
    
    uint8_t tempo = 120;
    uint8_t time_sig = 4; // 2 for 2/4, 3 for 3/4, etc.
    
    uint8_t note_count = 9;
    
    uint8_t pitches[9] = {60,62,64,65,67,65,64,62,60};
    uint32_t onsets[9] = {0,250,500,750,1000,1250,1500,1750,2000};
    uint32_t releases[9] = {240,490,740,990,1240,1490,1740,1990,3000};
    
    char serial_buffer[100];
    
    while (1) {
    
        send_str("\rSTATE: IDLE\n\0"); // user is selecting tempo / time signature
        __delay_ms(1000);

        send_str("\rSTATE: COUNTOFF\n\0"); // user pressed start and metronome begins
        __delay_ms(2000);

        send_str("\rSTATE: RECORDING\n\0"); // device begins recording and user plays
        __delay_ms(2000);

        send_str("\rSTATE: SENDING\n\0"); // user stops recording and device sends data
    
        send_attr_data(tempo, time_sig);
        send_note_data(note_count, pitches, onsets, releases);
    }
        
    
    return 0;
}
#endif

#ifdef TEST_CODE_3
int main() {

    // setup code
    // =========================================================================
    INIT();
    
    fractional squaredMagnitude[FFT_SIZE];
    fractional fftMaxValue;
    int16_t fftMaxValueBin;     
    uint16_t peakFrequencyHz;

    //FILLING THE FFT INPUT ARRAY
    uint16_t adc_data[FFT_SIZE];
    uint16_t v,vp;
    uint16_t max = 2000;
    
    time_t start = 0;
    time_t stop = 0;
    double cycles = 0;
    
    // loop code
    // =========================================================================
    int i=0;
    time(0); //start time
    
    //record for a second
    while(1)
    {
        for (i=0; i<512; i++) {

            v = analog_read();
            if (v > max) { max = v; }

            // mapped_value = (original_value - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

//            adc_data[i] = (2*v)/(max - 1);
//            fftBuffer[i].real = Q15(adc_data[i]);
            
            long center = (2*(long)v) / ((long)max - 1);
            fftBufferR[i] = center;

            vp=v;
        } // crash -> PC=0x0306, normal exit -> PC=0x0238

//        send_str("\rsampling loop complete!\n\0");
        __delay_ms(10);

//        FFTComplexIP(9, (fractcomplex*)&fftBuffer[0], &twiddleFactors[0], 0xFF00);
//        BitReverseComplex(9,(fractcomplex*)&fftBuffer[0]);
//        SquareMagnitudeCplx(FFT_SIZE, (fractcomplex*)&fftBuffer[0], (fractional*)&squaredMagnitude[0]);
        
        FFTReal32bIP(9-1, 512, fftBufferR, twiddleFactorsR, 0xFF00);
        

        // BANDPASS FILTER FOR THE OCTAVE OF C5 TO C6
//        squaredMagnitude[0] = 0;
//        squaredMagnitude[1] = 0;
//        squaredMagnitude[2] = 0;
//        while (x < 8)
//        {
//          squaredMagnitude[x] = 0;
//          x++;
//        }
//        x = 50;
//        while (x < 512)
//        {
//          squaredMagnitude[x] = 0;
//          x++;
//        }

        //ONLY LOOK FOR THE PEAK FREQUENCY WITHIN THE DESIRED RANGE
        // ~523Hz TO 1046Hz
//        fftMaxValue = VectorMax((FFT_SIZE/2), (fractional*)&squaredMagnitude[0], (int16_t*)&fftMaxValueBin);
//
//        //WITH SAMPLING FREQ = 31250 -> CAN READ 61Hz - 31,188Hz
//        if (fftMaxValue>0) {
//            peakFrequencyHz = fftMaxValueBin * (SAMPLING_FREQUENCY_HZ/FFT_SIZE);
//        } else {
//            peakFrequencyHz = 0;
//        }
        
        char buffer[40];
        sprintf(buffer, "\r, %5u, %5u, %5u, \n\0", fftMaxValueBin, peakFrequencyHz, fftMaxValue);
        send_str(buffer);

        time(&stop);
    }
    return 0;
}
#endif

#ifdef TEST_CODE_4
int main() {

    // setup code
    // =========================================================================
    
    INIT();
    __delay_ms(500);
    send_str("\rInit complete!\n\0");
    
    fractional sqm[FFT_SIZE];
    
    int i;
    uint64_t sample_num = 0;

    fractional adc_val;
    
    fractional sqm_peak_height;
    int16_t sqm_peak_bin;     
    float sqm_peak_height_float;
    float sqm_peak_freq;
    
    float rms = 1.0;
    
    time_t main_loop_start, onset, release;
    
    TwidFactorInit(FFT_SIZE_LOG2, &twiddleFactors[0], 0);

    // loop code
    // =========================================================================
    
    time(&main_loop_start);
    while (1) {
        
        memmove(&fftBuffer[OVERLAP_SIZE], &fftBuffer[0], sizeof fftBuffer - sizeof *fftBuffer);

        for (i=0; i<OVERLAP_SIZE; i++) {
            /**
             * this loop has to be fast:
             *      - avoid function calls
             *      - avoid subloops
             *      - ABSOLUTELY NO FLOATING POINTS IN HERE
             *  
             */
            AD1CON1bits.SAMP = 0x01;
            __delay_us(2);
            AD1CON1bits.SAMP = 0x00;
            while(AD1CON1bits.DONE == 0x00) {}
            adc_val = ADC1BUF0;
            
            fftBuffer[i].real = adc_val + (fractional)0x4000; // temporary accommodation for voltage offset
        } /* sampling loop */

        // shift fftBuffer right by 128
        sample_num += OVERLAP_SIZE;
        
        // perform fft to get square magnitude
        FFTComplexIP(FFT_SIZE_LOG2, 
                (fractcomplex*)&fftBuffer[0], 
                &twiddleFactors[0], 
                0xFF00);
        BitReverseComplex(FFT_SIZE_LOG2, 
                (fractcomplex*)&fftBuffer[0]);
        SquareMagnitudeCplx(FFT_SIZE, 
                (fractcomplex*)&fftBuffer[0], 
                (fractional*)&sqm[0]);
        
        // band pass the freq spectrum: range = (227Hz to 1500Hz)
        for (i=0;i<32;i++) { sqm[i] = 0; }
        for (i=FFT_SIZE/5;i<FFT_SIZE;i++) { sqm[i] = 0; }
        
        // extract peak and convert height to float
        sqm_peak_height = VectorMax((FFT_SIZE/2), (fractional*)&sqm[0], (int16_t*)&sqm_peak_bin);
        sqm_peak_height_float = Fract2Float(sqm_peak_height);

        // only keep peak if magnitude greater than threshold
        if (sqm_peak_height_float>0.000050) {
            sqm_peak_freq = sqm_peak_bin * ((float)SAMPLING_FREQUENCY_HZ/(float)FFT_SIZE);
        } else {
            sqm_peak_freq = 0.0;
            sqm_peak_bin = 0;
        }
        
        // timing detection call
        rms = 5.0;
        detect_timings(sample_num, sqm_peak_freq, rms, &onset, &release);

        if (onset!=0 || release!=0) {
            char buffer[60];
            if (onset!=0) {
                sprintf(buffer, "\r%6ld ms: attack\n\r\tfreq = %f Hz\n\0", 
                        (onset-main_loop_start)/1000/8, 
                        (double)sqm_peak_freq);
                send_str(buffer);
            } else if (release!=0) {
                sprintf(buffer, "\r%6ld ms: release\n\n\n\0", 
                        (release-main_loop_start)/1000/8);
                send_str(buffer);
            }
        }
        
    } /* main loop */
    return 0;
}

// int main () {
//     INIT();
    
//     InitButtons();
    
//     //setting default values
//     int count = 0;      //if count is 0, state is idle, recording hasn't started
//     int bpm = 60;       //BPM starts at 60 (max is 120 then returns to 60)
//     int TS = 4;         //TS initializes at 4
//     int notes[10];
//     int onsets[10];
//     int releases[10];
    
//     char buffer[40];
    
//     //BEFORE THE USER STARTS RECORDING
//     while(count == 0){
        
//         bpm = BpmUpDown(bpm);
        
//         if(Time_TwoFour() == 1)
//         {
//             TS = 2;
//         }
//         else if(Time_ThreeFour() == 1)
//         {
//             TS = 2;
//         }
//         else if(Time_FourFour() == 1)
//         {
//             TS = 2;
//         }
    
//         if(StartStop() == 1){
//             count++;  
//         }    
        
//         sprintf(buffer, "\r BPM: %5u, Time Signature: %5u \n\0", bpm, TS);
//         send_str(buffer);
        
//     }
    
//     //WHEN THE USER SELECTS TO START RECORDING
//     while(count == 1){
        
//         //light up the LED
        
//         //run all of the ADC,FFT code
        
//         if(StartStop() == 1){
//             count++;  
//         }  
//     }
    
//     //WHEN THE USER SELECTS TO STOP RECORDING
//     while(count == 2){
        
//         //SEND BACK TO IDLE MODE AFTER IT FINISHES
//         if(StartStop() == 1){
//             count = 0;  
//         }  
        
//         for(int i=0; i<10; i++)
//         {
//             sprintf(buffer, "\r{\"pitch\": %5u, \"onset\": %5u, \"release\": %5u }\n\0", notes[i], onsets[i], releases[i]);
//             send_str(buffer);
//         }
//     }
    
//     return 0;
// }

#endif
// </editor-fold>

// <editor-fold defaultstate="collapsed" desc="function implementations">

void send_str(char * s) {
    int len=0;
    while (s[len] != '\0') { len++; }
    UART_SEND_ARRAY(s,len);
}

void send_note_data(uint8_t count, uint8_t * pitches, uint32_t * onsets, uint32_t * releases) {
    char buf[100];
    
    send_str("\rBEGIN NOTES\n\0");
    for (int i=0; i<count; i++) {
        sprintf(buf,
                "\r{\"pitch\": %u, \"onset\": %lu, \"release\": %lu}\n\0",
                pitches[i],
                onsets[i],
                releases[i]);
        send_str(buf);
    }
    send_str("\rEND NOTES\n\0");
}

void send_attr_data(uint8_t tempo, uint8_t time_sig) {
    char buf[100];
    
    send_str("\rBEGIN ATTRIBUTES\n\0");
    sprintf(buf,
            "\r{\"tempo\": %u, \"time\": {\"beats\": %u, \"beat-type\": 4}}\n\0",
            tempo,
            time_sig);
    send_str(buf);
    send_str("\rEND ATTRIBUTES\n\0");
}

// </editor-fold>
