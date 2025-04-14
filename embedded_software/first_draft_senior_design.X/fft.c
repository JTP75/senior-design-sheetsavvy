//#include "fft.h"
//#include "dsp.h"
////#include "libdsp-elf.a"
///*
// fractcomplex* TwidFactorInit (int log2N, fractcomplex* twidFactors, int conjFlag);
// * 
// fractcomplex* FFTComplexIP(int log2N, fractcomplex* srcCV, fractcomplex* twidFactors, int factPage);
// * 
// fractcomplex* BitReverseComplex (int log2N, fractcomplex* srcCV);
// * 
// fractional* SquareMagnitudeCplx (int numelems, fractcomplex* srcV,  fractional* dstV);
// * 
// */
//
//void FFT()
//{
//    int factPage;
//    int numelems;
//
//    int twiddles[8];             //array where the twiddle factors will be stored
//    int inputdata[20];
//
//
//    fractcomplex* srvCV;        //struct of 2 ints
//    fractcomplex* twidFactors;  //struct of two ints
//
//    fractional* dstV;
//    
//    
////    const fractcomplex twiddleFactors[FFT_SIZE/2]
////    __attribute__((space(auto_psv)))=
////    {
////     //.. enter twiddle factor values
////    here
////    };
//    
//    
//    //first we need to call this init function to generate the twid factors
//    twidFactors = TwidFactorInit(8, &twiddles[0], 0);
//    
//    //then it does the fft on the input data
//    srvCV = FFTComplexIP(8, &inputdata[0], &twiddles[0], COEFFS_IN_DATA);
//    
//    srvCV =  BitReverseComplex (8, &inputdata[0]);
//    
////    dstV =  SquareMagnitudeCplx (int numelems, &inputdata[0],  fractional* dstV);
//    
//    
////    // variable definitions
////    fractional squaredMagnitude[FFT_SIZE];
////    fractional fftMaxValue;
////    int16_t fftMaxValueBin;
////    uint16_t peakFrequencyHz;
////    // find the max value in the magnitude vector and /
////    // which bin it is in
////    fftMaxValue = VectorMax(FFT_SIZE/2,
////    (fractional*)&squaredMagnitude[0],
////    (int16_t*)&fftMaxValueBin);
////    // Compute the frequency (in Hz) of the largest //
////    // spectral component
////    peakFrequencyHz = fftMaxValueBin *
////    (SAMPLING_FREQUENCY_HZ / FFT_SIZE);
//    
//}
//
//
//
//
