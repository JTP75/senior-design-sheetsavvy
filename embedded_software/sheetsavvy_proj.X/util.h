/* 
 * File:   util.h
 * Author: pacel
 *
 * Created on October 11, 2024, 10:11 AM
 */

#ifndef UTIL_H
#define	UTIL_H

#include <dsp.h>

#ifdef	__cplusplus
extern "C" {
#endif

    /**
     * convert floating point value to char array
     * @param num float value to convert
     * @param buffer char array of length 9
     */
    void float2str(float num, char buffer[9]);
    
    /**
     * convert fixed point value to char array
     * @param fract value to convert
     * @param buffer char array of length 9
     */
    void fract2str(fractional val, char buffer[9]);
    
    /**
     * divides fractionals using integer arithmetic
     * @param a dividend
     * @param b divisor
     * @return quotient
     */
    fractional __divf(fractional a, fractional b);

#ifdef	__cplusplus
}
#endif

#endif	/* UTIL_H */

