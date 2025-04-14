#include "peripheral_utils.h"

    void InitButtons(){
        //MAKE ALL BUTTONS INPUTS
        TRISBbits.TRISB15 = 1;
        TRISBbits.TRISB14 = 1;
        TRISBbits.TRISB13 = 1;
        TRISBbits.TRISB12 = 1;
        TRISBbits.TRISB11 = 1;
        TRISBbits.TRISB10 = 1;
        
        //MAKE RECORDING LED OUTPUT
        TRISBbits.TRISB6 = 0;
        
    }

    int BpmUpDown(int bpm)
    {
        //if up button was pressed
        //  PIN 23
        if(LATBbits.LATB12 == 1)
        {
            return (bpm + 10);
        }
        //return (bpm+10);
        //if down button was pressed
        //  PIN 22
        else if(LATBbits.LATB11 == 1)
        {
            return (bpm - 10);
        }
        //return (bpm-10);
        //if neither were pressed
        else {return (bpm);}
    }  


    bool Time_TwoFour(){
        //if the two four button was pressed
        //  PIN 24
        //return 1;
        if(LATBbits.LATB13 == 1)
        {
            return 1;
        }
        //else
        //return 0;
        else {return 0;}
    } 
    
    
    bool Time_ThreeFour(){
        //if the three four button was pressed
        //  PIN 25
        //return 1;
        if(LATBbits.LATB14 == 1)
        {
            return 1;
        }
        //else
        //return 0;
        else {return 0;}
    } 
    
    
    bool Time_FourFour(){
        //if the four four button was pressed
        //  PIN 26
        if(LATBbits.LATB15 == 1)
        {
            return 1;
        }
        //return 1;
        //else
        //return 0;
        else {return 0;}
    } 

    
    bool StartStop(){
        //if the start stop button was pressed
        //  PIN 26
        if(LATBbits.LATB10 == 1)
        {
            return 1;
        }
        //return 1;
        //else
        //return 0;
        else {return 0;}
    }