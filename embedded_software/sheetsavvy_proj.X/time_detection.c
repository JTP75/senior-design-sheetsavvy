#include "time_detection.h"

bool current_note = false;
uint64_t maintain_counter = 0;
float max_rms = 0.0f;
float maintained_freq = 0.0f;
    
void detect_timings(uint64_t sample_num, float peak_freq, float rms, time_t * onset, time_t * release) {
    
    *onset = 0;
    *release = 0;
    
    // peak should be lowpassed before this call perhaps
    
    // check:
    // 1. peak freq spectrum size (handle this somewhere else maybe. still need to call reset_detect_timings() if called elsewhere)
    // 2. freq tolerance band
    // 3. relative rms
    // 4. absolute rms
    
    if (current_note && rms > max_rms) {
        max_rms = rms;
    }
    
    if (peak_freq > 60.0
            && rms > max_rms/10 
            && rms > RMS_THRESHOLD
            && abs(peak_freq-maintained_freq) < get_tolerance_at(maintained_freq)) {
        maintain_counter += 128;
    } else {
        if (current_note) {
            time(release);
        }
        current_note = false;
        maintain_counter = 0;
        max_rms = 0;
        maintained_freq = peak_freq;
    }
    
    if (maintain_counter >= MIN_DURATION_SMPL && !current_note) {
        time(onset);
        *onset -= FCY / 25;
        current_note = true;
    }
}

float get_tolerance_at(float frequency) {
    // 0.057762265 / 2
    // 0.0288811325
    // 2888 / 100000
    return frequency * 0.028881;
}