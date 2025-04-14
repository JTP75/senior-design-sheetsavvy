/* 
 * File:   profile_config.h
 * Author: pacel
 *
 * Created on October 30, 2024, 6:37 PM
 */

#ifndef PROFILE_CONFIG_H
#define	PROFILE_CONFIG_H

/*
 * There are multiple main functions in main.c
 * These defines determine which main function to run
 * 
 * MAKE SURE ONLY ONE LINE IS UNCOMMENTED
 * 
 * To run the production main, uncomment the production
 * To run any of the test mains, uncomment the corresponding line
 * 
 * Add more as needed
 */

//#define PRODUCTION_CODE     // system production code
//#define TEST_CODE_1         // ev's fft test code
//#define TEST_CODE_2         // serial interface testing
//#define TEST_CODE_3         // justin fft test code
#define TEST_CODE_4         // ev implements peripherals over serial // tdm test

#endif	/* PROFIILE_CONFIG_H */

