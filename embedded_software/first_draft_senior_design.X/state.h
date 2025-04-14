/* 
 * File:   state.h
 * Author: pacel
 *
 * Created on November 7, 2024, 7:42 PM
 */

#ifndef STATE_H
#define	STATE_H

#ifdef	__cplusplus
extern "C" {
#endif

    enum state_t {
        idle,
        countoff,
        recording,
        sending
    } state;

#ifdef	__cplusplus
}
#endif

#endif	/* STATE_H */

