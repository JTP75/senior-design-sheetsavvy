#define FCY 8000000UL

#include <libpic30.h>

#include "user.h"
#include <p33EV256GM002.h>
#include <xc.h>

void INIT(void) {
    //literally never delete the following 3 lines
    _ROSEL = 0x01;  //oscillator clock is used as reference (16MHz))
    INIT_PPS();     //have to do this for UART
    INIT_UART();    //never change this please god
    
    INIT_ADC_V2();
}

void INIT_OSC()
{
    OSCCONbits.NOSC = 0x00;
    OSCCONbits.CLKLOCK = 0x01;
    OSCCONbits.IOLOCK = 0x00;
    CLKDIVbits.DOZE = 0x00;
    CLKDIVbits.PLLPOST = 0b11;      //8
    CLKDIVbits.PLLPRE = 0b00110;    //6 + 1 = 7
}

void INIT_ADC_V2() {
    
    // Initialize all registers to 0
    AD1CON1 =   0x0000;
    AD1CON2 =   0x0000;
    AD1CON3 =   0x0000;
    AD1CON4 =   0x0000;
    AD1CHS123 = 0x0000;
    AD1CHS0 =   0x0000;
    AD1CSSH =   0x0000;
    AD1CSSL =   0x0000;
    ANSELA =    0x0000;
    
    // ADC 1 Control Register 1
    AD1CON1bits.ADON =          0b1;        //bit15
    AD1CON1bits.ADSIDL =        0b0;        //bit13
    AD1CON1bits.ADDMABM =       0b1;        //bit12
    AD1CON1bits.AD12B =         0b1;        //bit10
    AD1CON1bits.FORM =          0b11;       //bit9-8 //0->uint, 1->int, 2->ufract, 3->fract
    AD1CON1bits.SSRC =          0b111;      //bit7-5
    AD1CON1bits.SSRCG =         0b0;        //bit4
    AD1CON1bits.SIMSAM =        0b0;        //bit3
    AD1CON1bits.ASAM =          0b0;        //bit2
    AD1CON1bits.SAMP =          0b0;        //bit1
    AD1CON1bits.DONE =          0b0;        //bit0
    
    // ADC 1 Control Register 2
    AD1CON2bits.VCFG =          0b000;      //bit15-13
    AD1CON2bits.CSCNA =         0b0;        //bit10
    AD1CON2bits.CHPS =          0b00;       //bit9-8
    // AD1CON2bits.BUFS read only           //bit7
    AD1CON2bits.SMPI =          0b01111;    //bit6-2
    AD1CON2bits.BUFM =          0b0;        //bit1
    AD1CON2bits.ALTS =          0b0;        //bit0
    
    //SETS SAMPLING FREQ
    // ADC 1 Control Register 3
    AD1CON3bits.ADRC =          0b0;        //bit15
    AD1CON3bits.SAMC =          0b00001;    //bit12-8  (sample for 2* 8MHz before converting)
    // for samc:
    //      adds N * T_AD to sampling time
    
    AD1CON3bits.ADCS =          63;  //0b00111111; //bit7-0
    // for adcs: 
    //      (ADCS<7:0> + 1) / 8 = T_AD (in us)
    
    // ADC 1 Control Register 4
    AD1CON4bits.ADDMAEN =       0b1;        //bit8
    AD1CON4bits.DMABL =         0b101;      //bit2-0
    
    // ADC 1 Input Channel 1,2,3 Select Register
    AD1CHS123bits.CH123NB =     0b00;       //bit10-9
    AD1CHS123bits.CH123SB0 =    0b0;        //bit8
    AD1CHS123bits.CH123NA =     0b00;       //bit2-1
    AD1CHS123bits.CH123SA0 =    0b0;        //bit0
    
    // ADC 1 Input Channel 0 Select Register
    AD1CHS0bits.CH0NB =         0b0;        //bit15
    AD1CHS0bits.CH0SB =         0b000000;   //bit13-8
    AD1CHS0bits.CH0NA =         0b0;        //bit7
    AD1CHS0bits.CH0SA =         0b000000;   //bit5-0
    
    // ADC 1 Input Scan Select High Register
    AD1CSSH =                   0x0000;     //bit15-0
    
    // ADC 1 Input Scan Select Low Register
    AD1CSSL =                   0x0000;     //bit15-0
    
    // Analog/Digital Pin Selection Register
    ANSELAbits.ANSA0 =          0b1;        //bit0
    
    
    __delay_us(20);

}

void IO_LED()
{
    TRISBbits.TRISB6 = 0x00;
    
//    CNPUBbits.CNPUB6 = 0x01;
    LATBbits.LATB6 = 0x01;
    PORTBbits.RB6 = 0x01;
    __delay_ms(100);
    LATBbits.LATB6 = 0x00;
    PORTBbits.RB6 = 0x00;
    __delay_ms(100);
    
}

void INIT_UART(void)
{
    U1MODEbits.UARTEN = 0x00;
    U1MODEbits.USIDL = 0x00;
    U1MODEbits.IREN = 0x00;
    U1MODEbits.UEN = 0x00;
    U1MODEbits.WAKE = 0x00;
    U1MODEbits.LPBACK = 0x00;
    U1MODEbits.ABAUD = 0x00;
    U1MODEbits.URXINV = 0x00;   //idle state polarity is 1 (high)
    U1MODEbits.BRGH = 0x00;     //16x baud clock, standard mode
    U1MODEbits.PDSEL = 0x00;    //8-bit data, no parity
    U1MODEbits.STSEL = 0x00;    //one stop bit
    U1STAbits.URXISEL = 0x00;  
            
    TRISBbits.TRISB6 = 0x00;
    TRISBbits.TRISB6 = 0x00;
    
    U1BRG = 51;               //set the baud rate
}

void UART_SEND_ARRAY(char talky[], int size) {
    U1MODEbits.UARTEN = 0x01;   //enable uart again
    U1STAbits.UTXEN = 0x01;     //enable transmitting
    
    for (int i=0; i<size; i++) {
        U1TXREG = talky[i];         //set the data we wanna send
        while(!U1STAbits.TRMT){};   //wait for the flag to say its been done
    }
    
    U1MODEbits.UARTEN = 0x00;   //disable uart again
    U1STAbits.UTXEN = 0x00;     //disable transmitting
}

void UART_SEND_CHAR(uint8_t data)
{
    U1MODEbits.UARTEN = 0x01;   //enable uart again
    U1STAbits.UTXEN = 0x01;     //enable transmitting
    
    U1TXREG = 0x0000;
    U1TXREG = data;            //set the data we wanna send
    while(!U1STAbits.TRMT){};          //wait for the flag to say its been done
    
    _UTXEN = 0;
    
    U1MODEbits.UARTEN = 0x00;   //disable uart again
    U1STAbits.UTXEN = 0x00;     //disable transmitting
}

void INIT_PPS()
{
    //unlock pps registers (might be necessary, might not)
    __builtin_write_OSCCONL(OSCCON & ~(1<<6)); 
    
    //setting pin 9 to be used for UART RX
//    RPINR18bits.U1RXR = 0b0010010;
    
    //seting pin 11 to be used for UART TX
    RPOR1bits.RP36R = 0b000001;
    
    //lock pps registers again (might be necessary, might not)
    __builtin_write_OSCCONL(OSCCON | (1<<6));
    
}

void INIT_PWM()
{
    TRISBbits.TRISB14 = 0x00;
    PORTBbits.RB14 = 0x00;
    
    IOCON1  = 0xCC00;  //independent mode
    PWMCON1  = 0x0204; 
    FCLCON1  = 0x0003;
    PTCON2 = 0x0000;    //1:1 prescaler
    _SSRCG = 0x01;
    _SSRC = 0x00;
    
    PTPER = 100;
    PHASE1 = 1000;   //page 72 pwm)
    PDC1 = 5;     //DUTY CYCLE = (page 74 pwm)
    DTR1 = 50;       //dead time
    ALTDTR1 = 50;    //dead time value
    TRGCON1bits.TRGDIV = 0x00;
    TRGCON1bits.TRGSTRT = 0x00;
    TRIG1 = 0;
    
    FCLCON1 = 0;
    FCLCON1bits.FLTMOD = 3;
    
    PTCONbits.PTEN = 0x01;
}

void INIT_I2C()
{
    //fill this in later
    I2C1CON1bits.I2CEN = 0x00; //disable it to start
    I2C1CON1bits.I2CSIDL = 0x00; //continues in idle mode
    I2C1CON1bits.A10M = 0x00; //address is 7 bits long
    I2C1CON1bits.DISSLW = 0x01; //slew rate control disabled
    I2C1CON1bits.SMEN = 0x00;
    I2C1CON1bits.STREN = 0x00;
    I2C1CON1bits.ACKDT = 0x01; //NACK is sent after a receive
    I2C1CON1bits.ACKEN = 0x01;
    I2C1CON1bits.RCEN = 0x00; //receive sequence not in progress
    I2C1CON1bits.PEN = 0x00; //stop condition is idle
    I2C1CON1bits.RSEN = 0x00; //restart condition is idle
    I2C1CON1bits.SEN = 0x00; //start condition is idle
    
    I2C1CON2bits.SDAHT = 0x01; //minimum 300 ns after scl falling edge
    
    I2C1CON1bits.I2CEN = 0x01; //enable I2C operation
}

void I2C_send(uint8_t msg)
{
    I2C1CON1bits.I2CEN = 0x01; //enable I2C operation
    
    I2C1CON1bits.SEN = 0x01; //start condition is set
    
    //LOAD I2C1TRN with the data byte to transmit
    I2C1TRN = msg;
    
    //ACKSTAT is cleared when the msg is acknowledged
    while(_ACKSTAT){};
    
    //wait for the MI2C1IF
    while(_MI2C1IF){};
    
    I2C1CON1bits.PEN = 0x01; //stop condition is set
    
}