from copy import deepcopy
from xml.etree.ElementTree import Element, SubElement, ElementTree, indent

from src.framework.app_constants import DEFAULT_MEASURE_WIDTH, DEFAULT_STAFF_DISTANCE, DEFAULT_MEASURE_NUMBERING, \
    DEFAULT_DIVISIONS, DEFAULT_STAFF_COUNT
from src.framework.measure import Measure
from src.framework.score import Score
from src.framework.sheet_music_generator import SheetMusicGenerator
from src.framework.sheet_music_generator_exception import SheetMusicGeneratorException

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

_sixteenth_rest_map = {
    1: ("sixteenth",0),
    2: ("eighth",0),
    4: ("quarter",0),
    8: ("half",0),
    16: ("whole",0),
}


def find_consecutive_beam_notes(measure: Measure) -> list:
    beam_indices = []
    start, count = -1, 0
    div_counter = 0
    for i,note in enumerate(measure.notes):
        div_counter += note.duration
        if note.note_type=="eighth" or note.note_type=="sixteenth":
            if start==-1: start = i
            count += 1
            if div_counter>measure.duration//2:
                div_counter = 0
                if count>1: beam_indices.append((start,i-1))
                start, count = i, 0
        else:
            if count>1: beam_indices.append((start,i-1))
            start, count = -1, 0
    if count>1: beam_indices.append((start,len(measure.notes)-1))
    return beam_indices

class SheetMusicGeneratorImpl(SheetMusicGenerator):

    base_score_path: str
    score: Score
    note_data: list
    attr_data: dict

    def __init__(self, base_score_path: str):
        self.base_score_path = base_score_path
        self.score = Score(self.base_score_path)
        self.note_data = []
        self.attr_data = {}

    def __call__(self, attr_data: dict=None, note_data: list=None):
        if attr_data: self.set_attr_data(attr_data)
        if note_data: self.set_note_data(note_data)
        measure_duration = DEFAULT_DIVISIONS * self.attr_data["time"]["beats"]
        self.add_first_measure()
        for begin in range(measure_duration, self.note_data[-1]["release"], measure_duration):
            self.add_measure(begin,begin+measure_duration)

    def reset(self):
        self.score = Score(self.base_score_path)
        self.note_data = []
        self.attr_data = {}

    def save_as(self, location: str):
        try:
            indent(self.score)
            self.score.write(location)
        except IOError as err:
            print(f"[WARNING] save_as() failed to save to {location}")
        except Exception as err:
            raise err

    def add_first_measure(self):

        t_print = Element("print")
        t_layout = SubElement(t_print, "staff-layout")
        t_distance = SubElement(t_layout, "staff-distance")
        t_distance.text = str(DEFAULT_STAFF_DISTANCE)
        t_numbering = SubElement(t_layout, "measure-numbering")
        t_numbering.text = DEFAULT_MEASURE_NUMBERING

        t_attributes = Element("attributes")
        t_divisions = SubElement(t_attributes, "divisions")
        t_divisions.text = str(DEFAULT_DIVISIONS)
        t_key = SubElement(t_attributes, "key")
        t_fifths = SubElement(t_key, "fifths")
        t_fifths.text = str(self.attr_data["key"]["fifths"])
        t_mode = SubElement(t_key, "mode")
        t_mode.text = str(self.attr_data["key"]["mode"])
        t_time = SubElement(t_attributes, "time")
        t_beats = SubElement(t_time, "beats")
        t_beats.text = str(self.attr_data["time"]["beats"])
        t_beat_type = SubElement(t_time, "beat-type")
        t_beat_type.text = str(self.attr_data["time"]["beat-type"])
        t_staves = SubElement(t_attributes, "staves")
        t_staves.text = str(DEFAULT_STAFF_COUNT)
        t_clef = SubElement(t_attributes, "clef")
        t_sign = SubElement(t_clef, "sign")
        t_sign.text = str(self.attr_data["clef"]["sign"])
        t_line = SubElement(t_clef, "line")
        t_line.text = str(self.attr_data["clef"]["line"])

        t_direction = Element("direction", {"placement": "above"})
        t_direction_type = SubElement(t_direction,"direction-type")
        t_metronome = SubElement(t_direction_type, "metronome", {
            "default-y": "20",
            "font-family":
            "EngraverTextT",
            "font-size": "12",
            "halign": "left",
            "relative-x": "-32"
        })
        t_beat_unit = SubElement(t_metronome,"beat-unit")
        t_beat_unit.text = "quarter"
        t_per_minute = SubElement(t_metronome,"per-minute")
        t_per_minute.text = str(self.attr_data["tempo"])

        self.add_measure(0,self.attr_data["time"]["beats"]*DEFAULT_DIVISIONS)

        self.score.measures[0].insert(0, t_direction)
        self.score.measures[0].insert(0, t_attributes)
        self.score.measures[0].insert(0, t_print)

    def add_measure(self, begin: int, end: int):
        # FIXME add measure numbering
        # FIXME add default-x values
        measure = Measure(self.score, 1, DEFAULT_MEASURE_WIDTH, begin, end)
        for i,note in enumerate(self.note_data):
            if begin <= note["onset"] < end:
                if note["release"] > end:
                    self.split_note_at(i,end)
                if note["type"]=="compound":
                    self.handle_compound_note_at(i, begin)
                measure.add_note(50,self.note_data[i])
        for start,stop in find_consecutive_beam_notes(measure):
            measure.add_beam(start,stop)
        self.score.append_measure(measure)

    def handle_compound_note_at(self, index: int, begin: int):
        note = self.note_data[index]
        div = DEFAULT_DIVISIONS//4
        while note["onset"]+div*2 < note["release"]: div *= 2
        self.split_note_at(index,note["onset"]+div)
        if note["onset"]%note["duration"]>0:
            self.swap_notes(index,index+1)
            if self.note_data[index]["type"]=="compound":
                self.handle_compound_note_at(index, begin)

    def swap_notes(self, i1: int, i2: int):
        t1 = self.note_data[i1]["tie"] if "tie" in self.note_data[i1].keys() else None
        a1 = self.note_data[i1]["onset"]
        t2 = self.note_data[i2]["tie"] if "tie" in self.note_data[i2].keys() else None
        r2 = self.note_data[i2]["release"]
        self.note_data[i1],self.note_data[i2] = self.note_data[i2],self.note_data[i1]
        if t1: self.note_data[i1]["tie"] = t1
        self.note_data[i1]["onset"] = a1
        self.note_data[i1]["release"] = a1 + self.note_data[i1]["duration"]
        if t2: self.note_data[i2]["tie"] = t2
        self.note_data[i2]["onset"] = r2 - self.note_data[i2]["duration"]
        self.note_data[i2]["release"] = r2

    def split_note_at(self, index: int, div: int):

        note = self.note_data[index]
        if not note["onset"] < div < note["release"]:
            raise SheetMusicGeneratorException(f"Invalid split point ({div}) for note between {note['onset']} and {note['release']}")

        s1 = (div - note["onset"]) // (DEFAULT_DIVISIONS//4)
        s2 = (note["release"] - div) // (DEFAULT_DIVISIONS//4)

        if note["pitch"]:

            t1, d1 = _sixteenth_note_map[s1] if s1 in _sixteenth_note_map.keys() else ("compound",0)
            t2, d2 = _sixteenth_note_map[s2] if s2 in _sixteenth_note_map.keys() else ("compound",0)
            r2 = 0 + note["release"]
            tie_start = "tie" in note.keys() and note["tie"]=="start"
            note["release"] = div
            note["type"] = t1
            note["duration"] = div - note["onset"]
            note["dot"] = bool(d1)
            note["tie"] = "start"
            self.note_data.insert(index + 1, {
                "pitch": note["pitch"],
                "onset": div,
                "release": r2,
                "type": t2,
                "duration": r2 - div,
                "dot": bool(d2),
                "tie": "continue" if tie_start else "stop",
            })

        else:

            t1, _ = _sixteenth_rest_map[s1] if s1 in _sixteenth_rest_map.keys() else ("compound",0)
            t2, _ = _sixteenth_rest_map[s2] if s2 in _sixteenth_rest_map.keys() else ("compound",0)
            r2 = 0 + note["release"]
            note["release"] = div
            note["type"] = t1
            note["duration"] = div - note["onset"]
            self.note_data.insert(index + 1, {
                "pitch": note["pitch"],
                "onset": div,
                "release": r2,
                "type": t2,
                "duration": r2 - div,
            })

    def set_note_data(self, data: list):
        self.note_data = deepcopy(data)

    def set_attr_data(self, data: dict):
        self.attr_data = deepcopy(data)
