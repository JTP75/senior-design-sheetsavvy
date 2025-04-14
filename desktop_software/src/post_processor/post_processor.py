import copy
from copy import deepcopy

from src.framework.app_constants import DEFAULT_DIVISIONS


_sample_raw_data = {
    "notes": [
        {
            "pitch": 48,
            "onset": 0.0,
            "release": 0.5,
        },
    ],
    "attributes": {
        "time": {
            "beats": 4,
            "beat_type": 4,
        },
        "tempo": 120,
    }
}

_sharp_step_alter_map = {
    0: ("C",0),
    1: ("C",1),
    2: ("D",0),
    3: ("D",1),
    4: ("E",0),
    5: ("F",0),
    6: ("F",1),
    7: ("G",0),
    8: ("G",1),
    9: ("A",0),
    10: ("A",1),
    11: ("B",0),
}
"""For sharp key signatures"""

_flat_step_alter_map = {
    0: ("C",0),
    1: ("D",-1),
    2: ("D",0),
    3: ("E",-1),
    4: ("E",0),
    5: ("F",0),
    6: ("G",-1),
    7: ("G",0),
    8: ("A",-1),
    9: ("A",0),
    10: ("B",-1),
    11: ("B",0),
}
"""For flat key signatures"""

_sixteenth_note_map = {
    1: ("sixteenth",0),
    2: ("eighth",0),
    3: ("eighth",1),
    4: ("quarter",0),
    6: ("quarter",1),
    8: ("half",0),
    12: ("half",1),
    16: ("whole",0),
}
"""Does not include ties. integer in tuple is whether the note is dotted (1.5x duration)"""

_sixteenth_rest_map = {
    1: ("sixteenth",0),
    2: ("eighth",0),
    4: ("quarter",0),
    8: ("half",0),
    16: ("whole",0),
}

scales = [
    [0,1,3,5,6,8,10],   # Db (-5)
    [0,1,3,5,7,8,10],   # Ab (-4)
    [0,2,3,5,7,8,10],   # Eb (-3)
    [0,2,3,5,7,9,10],   # Bb (-2)
    [0,2,4,5,7,9,10],   # F  (-1)
    [0,2,4,5,7,9,11],   # C  (0)
    [0,2,4,6,7,9,11],   # G  (1)
    [1,2,4,6,7,9,11],   # D  (2)
    [1,2,4,6,8,9,11],   # A  (3)
    [1,3,4,6,8,9,11],   # E  (4)
    [1,3,4,6,8,10,11],  # B  (5)
    [1,3,5,6,8,10,11],  # F# (6)
]

root_to_fifths = {
    0: 0,
    1: -5,
    2: 2,
    3: -3,
    4: 4,
    5: -1,
    6: 6,
    7: 1,
    8: -4,
    9: 3,
    10: -2,
    11: 5,
}

treble_clef_center = 71
bass_clef_center = 49

def convert_float_to_div(tempo: int, time: float) -> int:
    return round(time*tempo/60*DEFAULT_DIVISIONS)

def round_to(div,n):
    return int(n*round(div/n))

def convert_pitch(num_pitch: int, use_flat=False) -> dict:
    """note: C_-1 is defined as note zero, meaning number 36 should go to C2"""
    step,alter = _flat_step_alter_map[num_pitch%12] if (
        use_flat) else _sharp_step_alter_map[num_pitch%12]
    octave = num_pitch//12 - 1
    return {"step": step,
            "alter": alter,
            "octave": octave}

def convert_note_timing(onset: int, release: int) -> tuple:
    d = (release-onset)*4/DEFAULT_DIVISIONS
    num_sixteenth_notes = round((release-onset)*4/DEFAULT_DIVISIONS)
    if num_sixteenth_notes not in _sixteenth_note_map.keys():
        return "compound",0
    return _sixteenth_note_map[num_sixteenth_notes]

def convert_rest_timing(onset: int, release: int) -> tuple:
    d = (release-onset)*4/DEFAULT_DIVISIONS
    num_sixteenth_rests = round((release-onset)*4/DEFAULT_DIVISIONS)
    if num_sixteenth_rests not in _sixteenth_rest_map.keys():
        return "compound",0
    return _sixteenth_rest_map[num_sixteenth_rests]

def insert_rests(notes: list, end_of_final_measure: int):
    curr_onset,prev_release = 0,0
    i = 0
    while i<len(notes):
        curr_onset = notes[i]["onset"]
        sixteenth_rests = round((curr_onset - prev_release)/DEFAULT_DIVISIONS*4)
        if sixteenth_rests!=0:
            # i.e. if delta is more than half the duration of a sixteenth note
            rest_type,dots = convert_rest_timing(prev_release, curr_onset)
            notes.insert(i,{
                "pitch": {},
                "onset": prev_release,
                "release": curr_onset,
                "type": rest_type,
                "duration": curr_onset-prev_release,
                "dot": dots>0,
            })
            i+=1
        prev_release = notes[i]["release"]
        i+=1
    sixteenth_rests = round((end_of_final_measure - prev_release)/DEFAULT_DIVISIONS*4)
    if sixteenth_rests != 0:
        # i.e. if delta is more than half the duration of a sixteenth note
        rest_type,dots = convert_rest_timing(prev_release, end_of_final_measure)
        notes.append({
            "pitch": {},
            "onset": prev_release,
            "release": end_of_final_measure,
            "type": rest_type,
            "duration": end_of_final_measure - prev_release,
            "dot": dots>0,
        })

def create_note_data(data: dict, use_flats: bool = False) -> list:
    notes = []
    for note in data["notes"]:
        note_type,dots = convert_note_timing(
            note["onset"],
            note["release"]
        )
        pitch_dict = convert_pitch(
            note["pitch"],
            use_flats,
        )
        notes.append({
            "pitch": pitch_dict,
            "onset": note["onset"],
            "release": note["release"],
            "type": note_type,
            "duration": note["release"]-note["onset"],
            "dot": dots>0,
        })
    end_of_final_measure = 0
    if notes:
        while notes[-1]["release"] > end_of_final_measure:
            end_of_final_measure += DEFAULT_DIVISIONS*data["attributes"]["time"]["beats"]
    else:
        end_of_final_measure = DEFAULT_DIVISIONS*data["attributes"]["time"]["beats"]
    insert_rests(notes,end_of_final_measure)
    return notes

def get_clef(data: dict) -> dict:
    avg_pitch = sum([note["pitch"] for note in data["notes"]]) / len(data["notes"]) if data["notes"] else 70
    if abs(bass_clef_center-avg_pitch) < abs(treble_clef_center-avg_pitch):
        return {"sign": "F", "line": 4}
    else:
        return {"sign": "G", "line": 2}

def get_accidental_count(data: dict, fifths: int) -> int:
    index = fifths + 5
    scale = scales[index]
    count = sum([0 if note["pitch"]%12 in scale else 1 for note in data["notes"]])
    return count

def get_fifths(data: dict) -> int:
    if len(data["notes"]) < 3 or len(set([note["pitch"] for note in data["notes"]])) < 3:
        return 0

    accidental_count_list = [(get_accidental_count(data,fifths),fifths) for fifths in range(-5,6+1)]
    accidental_count_list.sort(key=lambda tup: (tup[0],abs(tup[1])))

    min_acc_count_list = []
    for acc_count,fifths in accidental_count_list:
        if acc_count != accidental_count_list[0][0]: break
        min_acc_count_list.append(fifths)

    if len(min_acc_count_list) == 1:
        return min_acc_count_list[0]

    # keeping this just in case #
    # pitch_occurrences = {}
    # for note in data["notes"]:
    #     step = note["pitch"]%12
    #     if step not in pitch_occurrences.keys():
    #         pitch_occurrences[step] = 0
    #     pitch_occurrences[step] += 1

    last_note_fifths = root_to_fifths[data["notes"][-1]["pitch"]%12]
    if last_note_fifths in min_acc_count_list:
        return last_note_fifths

    return min_acc_count_list[0]

def get_key(data: dict) -> dict:
    return {"fifths": get_fifths(data), "mode": "major"}

def process_data(data: dict) -> tuple:

    data = copy.deepcopy(data)
    for note in data["notes"]:
        note["onset"] = round_to(convert_float_to_div(data["attributes"]["tempo"],note["onset"]/1000),DEFAULT_DIVISIONS/4)
        note["release"] = round_to(convert_float_to_div(data["attributes"]["tempo"],note["release"]/1000),DEFAULT_DIVISIONS/4)

    clef = get_clef(data)
    key = get_key(data)

    use_flats = key["fifths"]<0
    note_data = create_note_data(data, use_flats)

    attr_data = {
        "key": key,
        "time": data["attributes"]["time"],
        "clef": clef,
        "tempo": data["attributes"]["tempo"],
    }

    return note_data,attr_data