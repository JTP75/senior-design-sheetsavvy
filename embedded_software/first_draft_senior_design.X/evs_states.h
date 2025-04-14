/* 
 * File:   evs_states.h
 * Author: Evelyn
 *
 * Created on November 8, 2024, 11:42 AM
 */

#ifndef EVS_STATES_H
#define	EVS_STATES_H

#ifdef	__cplusplus
extern "C" {
#endif

#ifndef State                    /* [ */
typedef struct {
  //Here you'll change the outputs in each state
    //BPM value
    int bpm;
    
    //Recording Light
    int recordingLED;
    
    //Time Signature
    int TimeSig;
    
} State;
#endif  /* state */


#ifdef	__cplusplus
}
#endif

#endif	/* EVS_STATES_H */

