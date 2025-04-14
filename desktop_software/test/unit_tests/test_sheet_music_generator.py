import unittest
from xml.etree.ElementTree import ElementTree, indent

from src.sheet_music_generator.sheet_music_generator_impl import SheetMusicGeneratorImpl


BASE_SCORE_PATH = "../../src/archive/base_score.xml"
OUTPUT_PATH = "../test_outputs/"

WRITE_FILES = True

class ScoreBaseTestCase(unittest.TestCase):

    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)

    def tearDown(self):
        del self.fixture

    def test_fixture_exists(self):
        self.assertIsNotNone(self.fixture)

    def test_base_should_have_no_title(self):
        self.assertIsNotNone(self.fixture.score.find("work/work-title"))
        self.assertEqual("This Song Has No Title",self.fixture.score.find("work/work-title").text)

    def test_base_should_have_no_creator(self):
        self.assertIsNotNone(self.fixture.score.find("identification/creator"))
        self.assertEqual("Elton John",self.fixture.score.find("identification/creator").text)

    def test_base_should_have_no_measures(self):
        self.assertIsNone(self.fixture.score.find("part/measure"))

class AttributesTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    def test_attr_data_exists(self):
        self.assertIsNotNone(self.fixture.attr_data)

    def test_staff_layout_info(self):
        self.assertIsNotNone(self.fixture.score.find("part/measure/print/staff-layout"))
        self.assertEqual("70", self.fixture.score.find("part/measure/print/staff-layout/staff-distance").text)
        self.assertEqual("none",self.fixture.score.find("part/measure/print/staff-layout/measure-numbering").text)

    def test_base_divisions(self):
        self.assertIsNotNone(self.fixture.score.find("part/measure/attributes/divisions"))
        self.assertEqual("96",self.fixture.score.find("part/measure/attributes/divisions").text)

    def test_key_signature(self):
        self.assertIsNotNone(self.fixture.score.find("part/measure/attributes/key"))
        self.assertEqual("0",self.fixture.score.find("part/measure/attributes/key/fifths").text)
        self.assertEqual("major",self.fixture.score.find("part/measure/attributes/key/mode").text)

    def test_time_signature(self):
        self.assertIsNotNone(self.fixture.score.find("part/measure/attributes/time"))
        self.assertEqual("4",self.fixture.score.find("part/measure/attributes/time/beats").text)
        self.assertEqual("4",self.fixture.score.find("part/measure/attributes/time/beat-type").text)

    def test_base_staves(self):
        self.assertIsNotNone(self.fixture.score.find("part/measure/attributes/staves"))
        self.assertEqual("1",self.fixture.score.find("part/measure/attributes/staves").text)

    def test_clef(self):
        self.assertIsNotNone(self.fixture.score.find("part/measure/attributes/clef"))
        self.assertEqual("G",self.fixture.score.find("part/measure/attributes/clef/sign").text)
        self.assertEqual("2",self.fixture.score.find("part/measure/attributes/clef/line").text)

    def test_tempo(self):
        self.assertIsNotNone(self.fixture.score.find("part/measure/direction/direction-type/metronome/per-minute"))
        self.assertEqual("100",self.fixture.score.find("part/measure/direction/direction-type/metronome/per-minute").text)

# one measure cases #

class ElementaryOneMeasureTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 96,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {
                    "step": "D",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 96,
                "release": 192,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {
                    "step": "E",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 192,
                "release": 288,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 288,
                "release": 384,
                "type": "quarter",
                "duration": 96,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.set_note_data(self.note_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    def test_should_have_1_measure(self):
        self.assertEqual(1,len(self.fixture.score.findall("part/measure")))

    def test_should_have_4_notes(self):
        self.assertEqual(4,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/elementary.xml")

    def test_note_1_pitch(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("C",note.find("pitch/step").text)
        self.assertEqual("0",note.find("pitch/alter").text)
        self.assertEqual("4",note.find("pitch/octave").text)

    def test_note_1_type(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("quarter",note.find("type").text)

    def test_note_1_duration(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("96",note.find("duration").text)

    def test_note_2_pitch(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("D",note.find("pitch/step").text)
        self.assertEqual("0",note.find("pitch/alter").text)
        self.assertEqual("4",note.find("pitch/octave").text)

    def test_note_3_pitch(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        self.assertEqual("E",note.find("pitch/step").text)
        self.assertEqual("0",note.find("pitch/alter").text)
        self.assertEqual("4",note.find("pitch/octave").text)

    def test_note_4_pitch(self):
        note = self.fixture.score.findall("part/measure/note")[3]
        self.assertEqual("C",note.find("pitch/step").text)
        self.assertEqual("0",note.find("pitch/alter").text)
        self.assertEqual("4",note.find("pitch/octave").text)

class OneMeasureWithRestsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 96,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {},
                "onset": 96,
                "release": 192,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 3,
                },
                "onset": 192,
                "release": 288,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {},
                "onset": 288,
                "release": 384,
                "type": "quarter",
                "duration": 96,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.set_note_data(self.note_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    def test_should_have_1_measure(self):
        self.assertEqual(1,len(self.fixture.score.findall("part/measure")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/rests.xml")

    def test_should_have_4_notes(self):
        self.assertEqual(4,len(self.fixture.score.findall("part/measure/note")))

    def test_note_1_pitch(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertIsNotNone(note.find("pitch"))
        self.assertIsNone(note.find("rest"))

    def test_note_2_rest(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertIsNone(note.find("pitch"))
        self.assertIsNotNone(note.find("rest"))

    def test_note_3_pitch(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        self.assertIsNotNone(note.find("pitch"))
        self.assertIsNone(note.find("rest"))

    def test_note_4_rest(self):
        note = self.fixture.score.findall("part/measure/note")[3]
        self.assertIsNone(note.find("pitch"))
        self.assertIsNotNone(note.find("rest"))

class DottedHalfNoteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 288,
                "type": "half",
                "duration": 288,
                "dot": True,
            },
            {
                "pitch": {},
                "onset": 288,
                "release": 384,
                "type": "quarter",
                "duration": 96,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.set_note_data(self.note_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    def test_should_have_2_notes(self):
        self.assertEqual(2,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/dotted_half.xml")

    def test_should_be_dotted_note(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertIsNotNone(note.find("dot"))

class CompoundNoteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 240,
                "type": "compound",
                "duration": 240,
            },
            {
                "pitch": {},
                "onset": 240,
                "release": 384,
                "type": "quarter",
                "duration": 144,
                "dot": True,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.set_note_data(self.note_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    def test_should_have_3_notes(self):
        self.assertEqual(3,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/compound_note.xml")

    def test_should_be_half_note(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("half",note.find("type").text)

    def test_should_be_eighth_note(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("eighth",note.find("type").text)

    def test_should_be_tie_start(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("start",note.find("tie").attrib["type"])
        self.assertEqual("start",note.find("notations/tied").attrib["type"])

    def test_should_be_tie_stop(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("stop",note.find("tie").attrib["type"])
        self.assertEqual("stop",note.find("notations/tied").attrib["type"])

class CompoundRestTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {},
                "onset": 0,
                "release": 240,
                "type": "compound",
                "duration": 240,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 240,
                "release": 384,
                "type": "quarter",
                "duration": 144,
                "dot": True,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.set_note_data(self.note_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    def test_should_have_3_notes(self):
        self.assertEqual(3,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/compound_rest.xml")

    def test_should_be_half_rest(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("half",note.find("type").text)

    def test_should_be_eighth_rest(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("eighth",note.find("type").text)

class DoubleCompoundNoteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {},
                "onset": 0,
                "release": 72,
                "type": "compound",
                "duration": 72,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 72,
                "release": 384,
                "type": "compound",
                "duration": 312,
                "dot": True,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.set_note_data(self.note_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    # should be: 1/8 rest -> 1/16 rest -> 1/16 note -> 1/4 note -> 1/2 note

    def test_should_have_5_notes(self):
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/double_compound.xml")
        self.assertEqual(5,len(self.fixture.score.findall("part/measure/note")))

    def test_should_be_eighth_rest(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("eighth",note.find("type").text)
        self.assertIsNotNone(note.find("rest"))

    def test_should_be_sixteenth_rest(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("sixteenth",note.find("type").text)
        self.assertIsNotNone(note.find("rest"))

    def test_should_be_sixteenth_note(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        self.assertEqual("sixteenth",note.find("type").text)
        self.assertIsNone(note.find("rest"))

    def test_should_be_quarter_note(self):
        note = self.fixture.score.findall("part/measure/note")[3]
        self.assertEqual("quarter",note.find("type").text)
        self.assertIsNone(note.find("rest"))

    def test_should_be_half_note(self):
        note = self.fixture.score.findall("part/measure/note")[4]
        self.assertEqual("half",note.find("type").text)
        self.assertIsNone(note.find("rest"))

    def test_should_be_tied_1(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        self.assertEqual("start",note.find("notations/tied").attrib["type"])

    def test_should_be_double_tied_2(self):
        note = self.fixture.score.findall("part/measure/note")[3]
        ties = note.findall("notations/tied")
        self.assertEqual("start",ties[0].attrib["type"])
        self.assertEqual("stop",ties[1].attrib["type"])

    def test_should_be_tied_3(self):
        note = self.fixture.score.findall("part/measure/note")[4]
        self.assertEqual("stop",note.find("notations/tied").attrib["type"])

class OneQuarterNoteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 96,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {},
                "onset": 96,
                "release": 384,
                "type": "compound",
                "duration": 288,
                "dot": False,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture.set_attr_data(self.attr_data)
        self.fixture.set_note_data(self.note_data)
        self.fixture.add_first_measure()
    def tearDown(self):
        del self.fixture

    def test_should_have_3_notes(self):
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/quarter_note.xml")
        self.assertEqual(3,len(self.fixture.score.findall("part/measure/note")))

    def test_should_be_quarter_note(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("quarter",note.find("type").text)

    def test_should_be_quarter_rest(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("quarter",note.find("type").text)

    def test_should_be_half_rest(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        self.assertEqual("half",note.find("type").text)

# multiple measure cases #

class SplitWholeRest11TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 192,
                "type": "half",
                "duration": 192,
            },
            {
                "pitch": {},
                "onset": 192,
                "release": 576,
                "type": "whole",
                "duration": 384,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 576,
                "release": 768,
                "type": "half",
                "duration": 192,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_4_notes(self):
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/whole_rest_split_11.xml")
        self.assertEqual(4,len(self.fixture.score.findall("part/measure/note")))

    def test_should_be_first_half_rest(self):
        note = self.fixture.score.findall("part/measure/note")
        self.assertEqual("half",note[1].find("type").text)
        self.assertIsNone(note[1].find("tie"))

    def test_should_be_second_half_rest(self):
        note = self.fixture.score.findall("part/measure/note")
        self.assertEqual("half",note[2].find("type").text)
        self.assertIsNone(note[1].find("tie"))

class SplitWholeNote11TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 192,
                "type": "half",
                "duration": 192,
            },
            {
                "pitch": {
                    "step": "B",
                    "alter": 0,
                    "octave": 3,
                },
                "onset": 192,
                "release": 576,
                "type": "whole",
                "duration": 384,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 576,
                "release": 768,
                "type": "half",
                "duration": 192,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_4_notes(self):
        self.assertEqual(4,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/whole_note_split_11.xml")

    def test_should_be_first_half_note(self):
        note = self.fixture.score.findall("part/measure/note")
        self.assertEqual("half",note[1].find("type").text)
        self.assertEqual("start",note[1].find("tie").attrib["type"])

    def test_should_be_second_half_note(self):
        note = self.fixture.score.findall("part/measure/note")
        self.assertEqual("half",note[2].find("type").text)
        self.assertEqual("stop",note[2].find("tie").attrib["type"])

class SplitWholeNote31TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 96,
                "type": "quarter",
                "duration": 96,
            },
            {
                "pitch": {
                    "step": "B",
                    "alter": 0,
                    "octave": 3,
                },
                "onset": 96,
                "release": 480,
                "type": "whole",
                "duration": 384,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 480,
                "release": 768,
                "type": "half",
                "duration": 288,
                "dot": True,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_4_notes(self):
        self.assertEqual(4,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/whole_note_split_31.xml")

    def test_should_be_first_dotted_half_note(self):
        note = self.fixture.score.findall("part/measure/note")
        self.assertEqual("half",note[1].find("type").text)
        self.assertIsNotNone(note[1].find("dot"))
        self.assertEqual("start",note[1].find("tie").attrib["type"])

    def test_should_be_second_quarter_note(self):
        note = self.fixture.score.findall("part/measure/note")
        self.assertEqual("quarter",note[2].find("type").text)
        self.assertIsNone(note[2].find("dot"))
        self.assertEqual("stop",note[2].find("tie").attrib["type"])

class SplitWholeNote53TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 144,
                "type": "quarter",
                "duration": 144,
                "dot": True,
            },
            {
                "pitch": {
                    "step": "B",
                    "alter": 0,
                    "octave": 3,
                },
                "onset": 144,
                "release": 528,
                "type": "whole",
                "duration": 384,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 528,
                "release": 768,
                "type": "compound",
                "duration": 240,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_6_notes(self):
        self.assertEqual(6,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/whole_note_split_53.xml")

    def test_should_have_double_tie(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        tied = note.findall("notations/tied")
        self.assertEqual("start",tied[0].attrib["type"])
        self.assertEqual("stop",tied[1].attrib["type"])

    def test_should_be_first_eighth_note(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("eighth",note.find("type").text)
        self.assertEqual("start",note.find("notations/tied").attrib["type"])

    def test_should_be_second_half_note(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        self.assertEqual("half",note.find("type").text)

    def test_should_be_third_dotted_quarter_note(self):
        note = self.fixture.score.findall("part/measure/note")[3]
        self.assertEqual("quarter",note.find("type").text)
        self.assertIsNotNone(note.find("dot"))
        self.assertEqual("stop",note.find("tie").attrib["type"])

class SplitWholeNote97TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            "key": {
                "fifths": 0,
                "mode": "major",
            },
            "time": {
                "beats": 4,
                "beat-type": 4,
            },
            "clef": {
                "sign": "G",
                "line": 2,
            },
            "tempo": 100,
        }
        cls.note_data = [
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 0,
                "release": 168,
                "type": "compound",
                "duration": 168,
            },
            {
                "pitch": {
                    "step": "B",
                    "alter": 0,
                    "octave": 3,
                },
                "onset": 168,
                "release": 552,
                "type": "whole",
                "duration": 384,
            },
            {
                "pitch": {
                    "step": "C",
                    "alter": 0,
                    "octave": 4,
                },
                "onset": 552,
                "release": 768,
                "type": "compound",
                "duration": 216,
            },
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_8_notes(self):
        self.assertEqual(8,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/whole_note_split_97.xml")

    def test_should_have_double_tie_3(self):
        note = self.fixture.score.findall("part/measure/note")[3]
        tied = note.findall("notations/tied")
        self.assertEqual("start",tied[0].attrib["type"])
        self.assertEqual("stop",tied[1].attrib["type"])

    def test_should_have_double_tie_4(self):
        # FIXME this test fails, but the sheet music output is still correct
        note = self.fixture.score.findall("part/measure/note")[4]
        tied = note.findall("notations/tied")
        self.assertEqual("start",tied[0].attrib["type"])
        self.assertEqual("stop",tied[1].attrib["type"])

    def test_should_be_quarter_0(self):
        note = self.fixture.score.findall("part/measure/note")[0]
        self.assertEqual("quarter",note.find("type").text)

    def test_should_be_dotted_eighth_1(self):
        note = self.fixture.score.findall("part/measure/note")[1]
        self.assertEqual("eighth",note.find("type").text)
        self.assertIsNotNone(note.find("dot"))

    def test_should_be_sixteenth_2(self):
        note = self.fixture.score.findall("part/measure/note")[2]
        self.assertEqual("sixteenth",note.find("type").text)

    def test_should_be_half_3(self):
        note = self.fixture.score.findall("part/measure/note")[3]
        self.assertEqual("half",note.find("type").text)

    def test_should_be_quarter_4(self):
        note = self.fixture.score.findall("part/measure/note")[4]
        self.assertEqual("quarter",note.find("type").text)

    def test_should_be_dotted_eighth_5(self):
        note = self.fixture.score.findall("part/measure/note")[5]
        self.assertEqual("eighth",note.find("type").text)
        self.assertIsNotNone(note.find("dot"))

    def test_should_be_sixteenth_6(self):
        note = self.fixture.score.findall("part/measure/note")[6]
        self.assertEqual("sixteenth",note.find("type").text)

    def test_should_be_half_7(self):
        note = self.fixture.score.findall("part/measure/note")[7]
        self.assertEqual("half",note.find("type").text)

class CMajorScaleTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            'key': {
                'fifths': 0,
                'mode': 'major'
            },
            'time': {
                'beats': 4,
                'beat-type': 4
            },
            'clef': {
                'sign': 'G',
                'line': 2
            },
            'tempo': 120,
        }
        cls.note_data = [
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 0, 'release': 48, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'D', 'alter': 0, 'octave': 4}, 'onset': 48, 'release': 96, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'E', 'alter': 0, 'octave': 4}, 'onset': 96, 'release': 144, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'F', 'alter': 0, 'octave': 4}, 'onset': 144, 'release': 192, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'G', 'alter': 0, 'octave': 4}, 'onset': 192, 'release': 240, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'F', 'alter': 0, 'octave': 4}, 'onset': 240, 'release': 288, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'E', 'alter': 0, 'octave': 4}, 'onset': 288, 'release': 336, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'D', 'alter': 0, 'octave': 4}, 'onset': 336, 'release': 384, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 384, 'release': 480, 'type': 'quarter',
             'duration': 96, 'dot': False},
            {'pitch': {}, 'onset': 480, 'release': 768, 'type': 'compound',
             'duration': 288, 'dot': False},
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_2_measures(self):
        self.assertEqual(2,len(self.fixture.score.findall("part/measure")))

    def test_should_have_11_notes(self):
        self.assertEqual(11,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/cmajor.xml")

    def test_should_have_beam_first_4(self):
        notes = self.fixture.score.findall("part/measure/note")[:4]
        self.assertIsNotNone(notes[0].find("beam"))
        self.assertEqual("begin", notes[0].find("beam").text)
        self.assertEqual("continue", notes[1].find("beam").text)
        self.assertEqual("continue", notes[2].find("beam").text)
        self.assertEqual("end", notes[3].find("beam").text)

    def test_should_have_beam_second_4(self):
        notes = self.fixture.score.findall("part/measure/note")[4:8]
        self.assertIsNotNone(notes[0].find("beam"))
        self.assertEqual("begin", notes[0].find("beam").text)
        self.assertEqual("continue", notes[1].find("beam").text)
        self.assertEqual("continue", notes[2].find("beam").text)
        self.assertEqual("end", notes[3].find("beam").text)

class CMajorScaleWithRestsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            'key': {
                'fifths': 0,
                'mode': 'major'
            },
            'time': {
                'beats': 4,
                'beat-type': 4
            },
            'clef': {
                'sign': 'G',
                'line': 2
            },
            'tempo': 120,
        }
        cls.note_data = [
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 0, 'release': 48, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'D', 'alter': 0, 'octave': 4}, 'onset': 48, 'release': 96, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {}, 'onset': 96, 'release': 144, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'F', 'alter': 0, 'octave': 4}, 'onset': 144, 'release': 192, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {}, 'onset': 192, 'release': 240, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'F', 'alter': 0, 'octave': 4}, 'onset': 240, 'release': 288, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'E', 'alter': 0, 'octave': 4}, 'onset': 288, 'release': 336, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {}, 'onset': 336, 'release': 384, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 384, 'release': 480, 'type': 'quarter',
             'duration': 96, 'dot': False},
            {'pitch': {}, 'onset': 480, 'release': 768, 'type': 'compound',
             'duration': 288, 'dot': False},
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_2_measures(self):
        self.assertEqual(2,len(self.fixture.score.findall("part/measure")))

    def test_should_have_11_notes(self):
        self.assertEqual(11,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/cmajor_rest.xml")

    def test_should_have_beam_first_4(self):
        notes = self.fixture.score.findall("part/measure/note")[:4]
        self.assertIsNotNone(notes[0].find("beam"))
        self.assertEqual("begin", notes[0].find("beam").text)
        self.assertEqual("continue", notes[1].find("beam").text)
        self.assertEqual("continue", notes[2].find("beam").text)
        self.assertEqual("end", notes[3].find("beam").text)

    def test_should_have_beam_second_4(self):
        notes = self.fixture.score.findall("part/measure/note")[4:8]
        self.assertIsNotNone(notes[0].find("beam"))
        self.assertEqual("begin", notes[0].find("beam").text)
        self.assertEqual("continue", notes[1].find("beam").text)
        self.assertEqual("continue", notes[2].find("beam").text)
        self.assertEqual("end", notes[3].find("beam").text)

class RhythmTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            'key': {
                'fifths': 0,
                'mode': 'major'
            },
            'time': {
                'beats': 4,
                'beat-type': 4
            },
            'clef': {
                'sign': 'G',
                'line': 2
            },
            'tempo': 120,
        }
        cls.note_data = [
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 0, 'release': 48, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {}, 'onset': 48, 'release': 72, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'D', 'alter': 0, 'octave': 4}, 'onset': 72, 'release': 96, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'E', 'alter': 0, 'octave': 4}, 'onset': 96, 'release': 144, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'F', 'alter': 0, 'octave': 4}, 'onset': 144, 'release': 192, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'G', 'alter': 0, 'octave': 4}, 'onset': 192, 'release': 240, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'F', 'alter': 0, 'octave': 4}, 'onset': 240, 'release': 264, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'G', 'alter': 0, 'octave': 4}, 'onset': 264, 'release': 288, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'E', 'alter': 0, 'octave': 4}, 'onset': 288, 'release': 312, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'G', 'alter': 0, 'octave': 4}, 'onset': 312, 'release': 336, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'D', 'alter': 0, 'octave': 4}, 'onset': 336, 'release': 360, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'B', 'alter': 0, 'octave': 3}, 'onset': 360, 'release': 384, 'type': 'sixteenth',
             'duration': 24, 'dot': False},
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 384, 'release': 480, 'type': 'quarter',
             'duration': 96, 'dot': False},
            {'pitch': {}, 'onset': 480, 'release': 768, 'type': 'compound',
             'duration': 288, 'dot': False},
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_2_measures(self):
        self.assertEqual(2,len(self.fixture.score.findall("part/measure")))

    def test_should_have_15_notes(self):
        self.assertEqual(15,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/rhythms.xml")

    def test_should_have_beam_first_5(self):
        notes = self.fixture.score.findall("part/measure/note")[:5]
        self.assertIsNotNone(notes[0].find("beam"))
        self.assertEqual("begin", notes[0].find("beam").text)
        self.assertEqual("continue", notes[1].find("beam").text)
        self.assertEqual("continue", notes[2].find("beam").text)
        self.assertEqual("continue", notes[3].find("beam").text)
        self.assertEqual("end", notes[4].find("beam").text)

    def test_should_have_beam_second_7(self):
        notes = self.fixture.score.findall("part/measure/note")[5:12]
        self.assertIsNotNone(notes[0].find("beam"))
        self.assertEqual("begin", notes[0].find("beam").text)
        self.assertEqual("continue", notes[1].find("beam").text)
        self.assertEqual("continue", notes[2].find("beam").text)
        self.assertEqual("continue", notes[3].find("beam").text)
        self.assertEqual("continue", notes[4].find("beam").text)
        self.assertEqual("continue", notes[5].find("beam").text)
        self.assertEqual("end", notes[6].find("beam").text)

class SplitEighthsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {
            'key': {
                'fifths': 0,
                'mode': 'major'
            },
            'time': {
                'beats': 4,
                'beat-type': 4
            },
            'clef': {
                'sign': 'G',
                'line': 2
            },
            'tempo': 120,
        }
        cls.note_data = [
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 0, 'release': 48, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {}, 'onset': 48, 'release': 144, 'type': 'quarter',
             'duration': 96, 'dot': False},
            {'pitch': {'step': 'G', 'alter': 0, 'octave': 4}, 'onset': 144, 'release': 192, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'F', 'alter': 0, 'octave': 4}, 'onset': 192, 'release': 240, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {}, 'onset': 240, 'release': 336, 'type': 'quarter',
             'duration': 96, 'dot': False},
            {'pitch': {'step': 'E', 'alter': 0, 'octave': 4}, 'onset': 336, 'release': 384, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {'step': 'C', 'alter': 0, 'octave': 4}, 'onset': 384, 'release': 432, 'type': 'eighth',
             'duration': 48, 'dot': False},
            {'pitch': {}, 'onset': 432, 'release': 768, 'type': 'compound',
             'duration': 336, 'dot': False},
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_2_measures(self):
        self.assertEqual(2,len(self.fixture.score.findall("part/measure")))

    def test_should_have_10_notes(self):
        self.assertEqual(10,len(self.fixture.score.findall("part/measure/note")))
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/split_eighths.xml")

    def test_should_have_no_beams(self):
        beams = self.fixture.score.findall("part/measure/note/beam")
        self.assertEqual(0, len(beams))

# real data cases #

class AllOfMeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.attr_data = {'clef': {'line': 2, 'sign': 'G'},
                         'key': {'fifths': -1, 'mode': 'major'},
                         'tempo': 106.5,
                         'time': {'beat-type': 4, 'beats': 4}}
        cls.note_data = [
            {'dot': False, 'duration': 336, 'onset': 0, 'pitch': {}, 'release': 336, 'type': 'compound'},
            {'dot': False, 'duration': 48, 'onset': 336, 'pitch': {'alter': 0, 'octave': 4, 'step': 'A'}, 'release': 384, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 384, 'pitch': {'alter': 0, 'octave': 5, 'step': 'C'}, 'release': 432, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 432, 'pitch': {}, 'release': 480, 'type': 'eighth'},
            {'dot': False, 'duration': 24, 'onset': 480, 'pitch': {'alter': 0, 'octave': 4, 'step': 'A'}, 'release': 504, 'type': 'sixteenth'},
            {'dot': False, 'duration': 24, 'onset': 504, 'pitch': {}, 'release': 528, 'type': 'sixteenth'},
            {'dot': False, 'duration': 48, 'onset': 528, 'pitch': {'alter': 0, 'octave': 4, 'step': 'F'}, 'release': 576, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 576, 'pitch': {'alter': 0, 'octave': 4, 'step': 'D'}, 'release': 624, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 624, 'pitch': {'alter': 0, 'octave': 4, 'step': 'F'}, 'release': 672, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 672, 'pitch': {'alter': 0, 'octave': 4, 'step': 'A'}, 'release': 720, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 720, 'pitch': {}, 'release': 768, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 768, 'pitch': {'alter': 0, 'octave': 5, 'step': 'D'}, 'release': 816, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 816, 'pitch': {'alter': 0, 'octave': 5, 'step': 'C'}, 'release': 864, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 864, 'pitch': {}, 'release': 912, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 912, 'pitch': {'alter': 0, 'octave': 5, 'step': 'F'}, 'release': 960, 'type': 'eighth'},
            {'dot': False, 'duration': 96, 'onset': 960, 'pitch': {}, 'release': 1056, 'type': 'quarter'},
            {'dot': False, 'duration': 48, 'onset': 1056, 'pitch': {'alter': -1, 'octave': 5, 'step': 'E'}, 'release': 1104, 'type': 'eighth'},
            {'dot': False, 'duration': 24, 'onset': 1104, 'pitch': {}, 'release': 1128, 'type': 'sixteenth'},
            {'dot': False, 'duration': 24, 'onset': 1128, 'pitch': {'alter': 0, 'octave': 5, 'step': 'E'}, 'release': 1152, 'type': 'sixteenth'},
            {'dot': False, 'duration': 144, 'onset': 1152, 'pitch': {}, 'release': 1296, 'type': 'compound'},
            {'dot': False, 'duration': 48, 'onset': 1296, 'pitch': {'alter': 0, 'octave': 5, 'step': 'C'}, 'release': 1344, 'type': 'eighth'},
            {'dot': True, 'duration': 72, 'onset': 1344, 'pitch': {'alter': 0, 'octave': 4, 'step': 'G'}, 'release': 1416, 'type': 'eighth'},
            {'dot': False, 'duration': 24, 'onset': 1416, 'pitch': {}, 'release': 1440, 'type': 'sixteenth'},
            {'dot': False, 'duration': 48, 'onset': 1440, 'pitch': {'alter': 0, 'octave': 4, 'step': 'A'}, 'release': 1488, 'type': 'eighth'},
            {'dot': False, 'duration': 24, 'onset': 1488, 'pitch': {}, 'release': 1512, 'type': 'sixteenth'},
            {'dot': False, 'duration': 48, 'onset': 1512, 'pitch': {'alter': -1, 'octave': 4, 'step': 'B'}, 'release': 1560, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 1560, 'pitch': {}, 'release': 1608, 'type': 'eighth'},
            {'dot': False, 'duration': 24, 'onset': 1608, 'pitch': {'alter': 0, 'octave': 4, 'step': 'A'}, 'release': 1632, 'type': 'sixteenth'},
            {'dot': False, 'duration': 48, 'onset': 1632, 'pitch': {'alter': -1, 'octave': 4, 'step': 'A'}, 'release': 1680, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 1680, 'pitch': {'alter': 0, 'octave': 4, 'step': 'A'}, 'release': 1728, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 1728, 'pitch': {'alter': 0, 'octave': 5, 'step': 'C'}, 'release': 1776, 'type': 'eighth'},
            {'dot': False, 'duration': 24, 'onset': 1776, 'pitch': {}, 'release': 1800, 'type': 'sixteenth'},
            {'dot': False, 'duration': 48, 'onset': 1800, 'pitch': {'alter': 0, 'octave': 4, 'step': 'A'}, 'release': 1848, 'type': 'eighth'},
            {'dot': True, 'duration': 72, 'onset': 1848, 'pitch': {'alter': 0, 'octave': 4, 'step': 'F'}, 'release': 1920, 'type': 'eighth'},
            {'dot': False, 'duration': 120, 'onset': 1920, 'pitch': {'alter': 0, 'octave': 4, 'step': 'E'}, 'release': 2040, 'type': 'compound'},
            {'dot': False, 'duration': 48, 'onset': 2040, 'pitch': {}, 'release': 2088, 'type': 'eighth'},
            {'dot': False, 'duration': 24, 'onset': 2088, 'pitch': {'alter': 0, 'octave': 3, 'step': 'A'}, 'release': 2112, 'type': 'sixteenth'},
            {'dot': True, 'duration': 72, 'onset': 2112, 'pitch': {'alter': -1, 'octave': 3, 'step': 'A'}, 'release': 2184, 'type': 'eighth'},
            {'dot': True, 'duration': 72, 'onset': 2184, 'pitch': {'alter': 0, 'octave': 3, 'step': 'A'}, 'release': 2256, 'type': 'eighth'},
            {'dot': False, 'duration': 120, 'onset': 2256, 'pitch': {'alter': 0, 'octave': 4, 'step': 'E'}, 'release': 2376, 'type': 'compound'},
            {'dot': False, 'duration': 72, 'onset': 2376, 'pitch': {}, 'release': 2448, 'type': 'compound'},
            {'dot': False, 'duration': 48, 'onset': 2448, 'pitch': {'alter': 0, 'octave': 4, 'step': 'G'}, 'release': 2496, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 2496, 'pitch': {'alter': 0, 'octave': 4, 'step': 'E'}, 'release': 2544, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 2544, 'pitch': {'alter': 0, 'octave': 3, 'step': 'G'}, 'release': 2592, 'type': 'eighth'},
            {'dot': False, 'duration': 48, 'onset': 2592, 'pitch': {'alter': 0, 'octave': 3, 'step': 'A'}, 'release': 2640, 'type': 'eighth'},
            {'dot': False, 'duration': 168, 'onset': 2640, 'pitch': {'alter': 0, 'octave': 4, 'step': 'C'}, 'release': 2808, 'type': 'compound'},
            {'dot': False, 'duration': 264, 'onset': 2808, 'pitch': {}, 'release': 3072, 'type': 'compound'}
        ]
    @classmethod
    def tearDownClass(cls):
        del cls.attr_data
        del cls.note_data
    def setUp(self):
        self.fixture = SheetMusicGeneratorImpl(BASE_SCORE_PATH)
        self.fixture(self.attr_data,self.note_data)
    def tearDown(self):
        del self.fixture

    def test_should_have_save(self):
        if WRITE_FILES: self.fixture.save_as(f"{OUTPUT_PATH}/allofme.xml")
        self.assertEqual(1,1)

# unittest main #

if __name__ == '__main__':
    unittest.main()
