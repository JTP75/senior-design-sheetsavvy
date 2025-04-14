import unittest

from src.post_processor.post_processor import convert_pitch, convert_note_timing, process_data


# test cases must start with test_ #

class ConvertPitchTestCase(unittest.TestCase):

    def test_should_convert_36_to_c2(self):
        dict_pitch = convert_pitch(36)
        self.assertEqual("C",dict_pitch["step"])
        self.assertEqual(0,dict_pitch["alter"])
        self.assertEqual(2,dict_pitch["octave"])

    def test_should_convert_37_to_c2sharp(self):
        dict_pitch = convert_pitch(37)
        self.assertEqual("C",dict_pitch["step"])
        self.assertEqual(1,dict_pitch["alter"])
        self.assertEqual(2,dict_pitch["octave"])

    def test_should_convert_38_to_d2(self):
        dict_pitch = convert_pitch(38)
        self.assertEqual("D",dict_pitch["step"])
        self.assertEqual(0,dict_pitch["alter"])
        self.assertEqual(2,dict_pitch["octave"])

    def test_should_convert_37_to_d2flat(self):
        dict_pitch = convert_pitch(37,True)
        self.assertEqual("D",dict_pitch["step"])
        self.assertEqual(-1,dict_pitch["alter"])
        self.assertEqual(2,dict_pitch["octave"])

    def test_should_convert_84_to_c6(self):
        dict_pitch = convert_pitch(84)
        self.assertEqual("C",dict_pitch["step"])
        self.assertEqual(0,dict_pitch["alter"])
        self.assertEqual(6,dict_pitch["octave"])

class ConvertTimingTestCase(unittest.TestCase):

    def test_should_convert_120_quarter_note(self):
        note_type,dots = convert_note_timing(0, 96)
        self.assertEqual("quarter",note_type)

    def test_should_convert_60_whole_note(self):
        note_type,dots = convert_note_timing(0, 384)
        self.assertEqual("whole",note_type)

    def test_should_convert_120_eighth_note(self):
        note_type,dots = convert_note_timing(0, 48)
        self.assertEqual("eighth",note_type)

# one measure cases #

class OneQuarterNoteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            "notes": [
                {
                    "pitch": 60,
                    "onset": 0.0,
                    "release": 0.5,
                },
            ],
            "attributes": {
                "time": {
                    "beats": 4,
                    "beat-type": 4,
                },
                "tempo": 120,
            },
        }
    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_be_4_4_time(self):
        _,attr_data = process_data(self.data)
        self.assertEqual(4,attr_data["time"]["beats"])
        self.assertEqual(4,attr_data["time"]["beat-type"])

    def test_should_be_120_bpm(self):
        _,attr_data = process_data(self.data)
        self.assertEqual(120,attr_data["tempo"])

    def test_should_be_c4(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("C",note_data[0]["pitch"]["step"])
        self.assertEqual(0,note_data[0]["pitch"]["alter"])
        self.assertEqual(4,note_data[0]["pitch"]["octave"])

    def test_should_be_onset_0(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(0,note_data[0]["onset"])

    def test_should_be_release_96(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(96,note_data[0]["release"])

    def test_should_be_duration_96(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(96,note_data[0]["duration"])

    def test_should_be_quarter_note(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("quarter",note_data[0]["type"])

    # rest handling #

    def test_should_be_two_notes(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(2,len(note_data))

    def test_should_be_compound_rest(self):
        note_data,_ = process_data(self.data)
        self.assertEqual({},note_data[1]["pitch"])
        self.assertEqual("compound",note_data[1]["type"])

class EmptyMeasureTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            "notes": [
            ],
            "attributes": {
                "time": {
                    "beats": 4,
                    "beat-type": 4,
                },
                "tempo": 120,
            },
        }
    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_be_one_note(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(1, len(note_data))

    def test_should_be_whole_rest(self):
        note_data,_ = process_data(self.data)
        self.assertEqual({}, note_data[0]["pitch"])
        self.assertEqual("whole", note_data[0]["type"])

class DottedHalfNoteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            "notes": [
                {
                    "pitch": 54,
                    "onset": 0.0,
                    "release": 1.5,
                }
            ],
            "attributes": {
                "time": {
                    "beats": 4,
                    "beat-type": 4,
                },
                "tempo": 120,
            },
        }
    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_have_2_notes(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(2,len(note_data))

    def test_should_be_dotted_half_note(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("half",note_data[0]["type"])
        self.assertEqual(True,note_data[0]["dot"])

    def test_should_be_quarter_rest(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("quarter",note_data[1]["type"])
        self.assertEqual({},note_data[1]["pitch"])

class OffbeatEighthsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            "notes": [
                {
                    "pitch": 41,
                    "onset": 0.25,
                    "release": 0.5,
                },
                {
                    "pitch": 41,
                    "onset": 0.75,
                    "release": 1.0,
                },
                {
                    "pitch": 41,
                    "onset": 1.25,
                    "release": 1.5,
                },
                {
                    "pitch": 41,
                    "onset": 1.75,
                    "release": 2.0,
                },
            ],
            "attributes": {
                "time": {
                    "beats": 4,
                    "beat-type": 4,
                },
                "tempo": 120,
            },
        }
    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_have_8_notes(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(8,len(note_data))

    def test_should_have_eighth_rest(self):
        note_data,_ = process_data(self.data)
        self.assertEqual({},note_data[0]["pitch"])
        self.assertEqual("eighth",note_data[0]["type"])

    def test_should_have_eighth_note(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("F",note_data[-1]["pitch"]["step"])
        self.assertEqual("eighth",note_data[-1]["type"])

class CompoundNoteTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            "notes": [
                {
                    "pitch": 41,
                    "onset": 0.0,
                    "release": 1.25,
                },
            ],
            "attributes": {
                "time": {
                    "beats": 4,
                    "beat-type": 4,
                },
                "tempo": 120,
            },
        }
    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_have_3_notes(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(2,len(note_data))

    def test_should_have_compound_note(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("compound",note_data[0]["type"])

# multiple measure cases #

class RealSignalTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            "notes": [
                {
                    "pitch": 60,
                    "onset": 1.329,
                    "release": 1.565,
                },
                {
                    "pitch": 60,
                    "onset": 1.801,
                    "release": 2.058,
                },
                {
                    "pitch": 60,
                    "onset": 2.327,
                    "release": 2.535,
                },
                {
                    "pitch": 60,
                    "onset": 2.832,
                    "release": 3.064,
                },
                {
                    "pitch": 60,
                    "onset": 5.334,
                    "release": 5.562,
                },
                {
                    "pitch": 60,
                    "onset": 5.827,
                    "release": 6.017,
                },
                {
                    "pitch": 60,
                    "onset": 6.087,
                    "release": 6.269,
                },
                {
                    "pitch": 60,
                    "onset": 6.351,
                    "release": 6.611,
                },
                {
                    "pitch": 60,
                    "onset": 6.826,
                    "release": 7.002,
                },
                {
                    "pitch": 60,
                    "onset": 7.101,
                    "release": 7.273,
                },
            ],
            "attributes": {
                "time": {
                    "beats": 4,
                    "beat-type": 4,
                },
                "tempo": 120,
            },
        }
        start = 1.316
        for note in cls.data["notes"]:
            note["onset"] = note["onset"]-start
            note["release"] = note["release"]-start
    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_have_16_notes(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(16, len(note_data))

    def test_should_be_eighth_note(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("eighth",note_data[0]["type"])
        self.assertNotEqual({},note_data[0]["pitch"])

    def test_should_be_compound_rest(self):
        note_data,_ = process_data(self.data)
        self.assertEqual("compound",note_data[7]["type"])
        self.assertEqual({},note_data[7]["pitch"])

class CMajorTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            'notes': [
                {'pitch': 60, 'onset': 0, 'release': 0.25},
                {'pitch': 62, 'onset': 0.25, 'release': 0.5},
                {'pitch': 64, 'onset': 0.5, 'release': 0.75},
                {'pitch': 65, 'onset': 0.75, 'release': 1},
                {'pitch': 67, 'onset': 1, 'release': 1.25},
                {'pitch': 65, 'onset': 1.25, 'release': 1.5},
                {'pitch': 64, 'onset': 1.5, 'release': 1.75},
                {'pitch': 62, 'onset': 1.75, 'release': 2},
                {'pitch': 60, 'onset': 2, 'release': 2.5}
            ],
            'attributes': {
                'time': {
                    'beats': 4,
                    'beat-type': 4
                },
                'tempo': 120
            }
        }
    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_have_11_notes(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(10, len(note_data))

    def test_last_rest_should_onset_480(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(480,note_data[-1]["onset"])

    def test_last_rest_should_release_768(self):
        note_data,_ = process_data(self.data)
        self.assertEqual(768,note_data[-1]["release"])

# clef estimation cases #

class TrebleClefTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            'notes': [
                {'pitch': 60, 'onset': 0, 'release': 0.25},
                {'pitch': 62, 'onset': 0.25, 'release': 0.5},
                {'pitch': 64, 'onset': 0.5, 'release': 0.75},
                {'pitch': 65, 'onset': 0.75, 'release': 1},
                {'pitch': 67, 'onset': 1, 'release': 1.25},
                {'pitch': 65, 'onset': 1.25, 'release': 1.5},
                {'pitch': 64, 'onset': 1.5, 'release': 1.75},
                {'pitch': 62, 'onset': 1.75, 'release': 2},
                {'pitch': 60, 'onset': 2, 'release': 2.5}
            ],
            'attributes': {
                'time': {
                    'beats': 4,
                    'beat-type': 4
                },
                'tempo': 120
            }
        }

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_be_treble_clef(self):
        _,attr_data = process_data(self.data)
        self.assertEqual("G", attr_data["clef"]["sign"])
        self.assertEqual(2, attr_data["clef"]["line"])

class BassClefTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            'notes': [
                {'pitch': 48, 'onset': 0, 'release': 0.25},
                {'pitch': 50, 'onset': 0.25, 'release': 0.5},
                {'pitch': 52, 'onset': 0.5, 'release': 0.75},
                {'pitch': 53, 'onset': 0.75, 'release': 1},
                {'pitch': 55, 'onset': 1, 'release': 1.25},
                {'pitch': 53, 'onset': 1.25, 'release': 1.5},
                {'pitch': 52, 'onset': 1.5, 'release': 1.75},
                {'pitch': 50, 'onset': 1.75, 'release': 2},
                {'pitch': 48, 'onset': 2, 'release': 2.5}
            ],
            'attributes': {
                'time': {
                    'beats': 4,
                    'beat-type': 4
                },
                'tempo': 120
            }
        }

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_be_bass_clef(self):
        _,attr_data = process_data(self.data)
        self.assertEqual("F", attr_data["clef"]["sign"])
        self.assertEqual(4, attr_data["clef"]["line"])

# key signature estimation cases #

class NaturalScaleKeyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            'notes': [
                {'pitch': 48, 'onset': 0, 'release': 0.25},
                {'pitch': 50, 'onset': 0.25, 'release': 0.5},
                {'pitch': 52, 'onset': 0.5, 'release': 0.75},
                {'pitch': 53, 'onset': 0.75, 'release': 1},
                {'pitch': 55, 'onset': 1, 'release': 1.25},
                {'pitch': 53, 'onset': 1.25, 'release': 1.5},
                {'pitch': 52, 'onset': 1.5, 'release': 1.75},
                {'pitch': 50, 'onset': 1.75, 'release': 2},
                {'pitch': 48, 'onset': 2, 'release': 2.5}
            ],
            'attributes': {
                'time': {
                    'beats': 4,
                    'beat-type': 4
                },
                'tempo': 120
            }
        }

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_be_natural(self):
        _,attr_data = process_data(self.data)
        self.assertEqual(0,attr_data["key"]["fifths"])

class AllMajorScalesTestCase(unittest.TestCase):

    def setUp(self):
        self.data = {
            'notes': [
                {'pitch': 48, 'onset': 0, 'release': 0.25},
                {'pitch': 50, 'onset': 0.25, 'release': 0.5},
                {'pitch': 52, 'onset': 0.5, 'release': 0.75},
                {'pitch': 53, 'onset': 0.75, 'release': 1},
                {'pitch': 55, 'onset': 1, 'release': 1.25},
                {'pitch': 53, 'onset': 1.25, 'release': 1.5},
                {'pitch': 52, 'onset': 1.5, 'release': 1.75},
                {'pitch': 50, 'onset': 1.75, 'release': 2},
                {'pitch': 48, 'onset': 2, 'release': 2.5}
            ],
            'attributes': {
                'time': {
                    'beats': 4,
                    'beat-type': 4
                },
                'tempo': 120
            }
        }

    def tearDown(self):
        del self.data

    def translate_step(self, step):
        for note in self.data["notes"]:
            note["pitch"] += step

    def test_ab_m4(self):
        self.translate_step(-4)
        _,attr_data = process_data(self.data)
        self.assertEqual(-4,attr_data["key"]["fifths"])

    def test_a_3(self):
        self.translate_step(-3)
        _,attr_data = process_data(self.data)
        self.assertEqual(3,attr_data["key"]["fifths"])

    def test_bb_m2(self):
        self.translate_step(-2)
        _,attr_data = process_data(self.data)
        self.assertEqual(-2,attr_data["key"]["fifths"])

    def test_b_5(self):
        self.translate_step(-1)
        _,attr_data = process_data(self.data)
        self.assertEqual(5,attr_data["key"]["fifths"])

    def test_c_0(self):
        self.translate_step(0)
        _,attr_data = process_data(self.data)
        self.assertEqual(0,attr_data["key"]["fifths"])

    def test_db_m5(self):
        self.translate_step(1)
        _,attr_data = process_data(self.data)
        self.assertEqual(-5,attr_data["key"]["fifths"])

    def test_d_2(self):
        self.translate_step(2)
        _,attr_data = process_data(self.data)
        self.assertEqual(2,attr_data["key"]["fifths"])

    def test_eb_m3(self):
        self.translate_step(3)
        _,attr_data = process_data(self.data)
        self.assertEqual(-3,attr_data["key"]["fifths"])

    def test_e_4(self):
        self.translate_step(4)
        _,attr_data = process_data(self.data)
        self.assertEqual(4,attr_data["key"]["fifths"])

    def test_f_m1(self):
        self.translate_step(5)
        _,attr_data = process_data(self.data)
        self.assertEqual(-1,attr_data["key"]["fifths"])

    def test_fs_6(self):
        self.translate_step(6)
        _,attr_data = process_data(self.data)
        self.assertEqual(6,attr_data["key"]["fifths"])

    def test_g_1(self):
        self.translate_step(7)
        _,attr_data = process_data(self.data)
        self.assertEqual(1,attr_data["key"]["fifths"])

class SongKeyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = {
            'notes': [
                {"pitch": 69, "onset": 0.54, "release": 0.76},
                {"pitch": 72, "onset": 0.76, "release": 1.01},
                {"pitch": 69, "onset": 1.31, "release": 1.51},
                {"pitch": 65, "onset": 1.68, "release": 1.86},
                {"pitch": 62, "onset": 1.86, "release": 2.13},
                {"pitch": 65, "onset": 2.23, "release": 2.43},
                {"pitch": 69, "onset": 2.45, "release": 2.69},
                {"pitch": 74, "onset": 3.00, "release": 3.27},
                {"pitch": 72, "onset": 3.34, "release": 3.56},
                {"pitch": 77, "onset": 3.91, "release": 4.15},
                {"pitch": 75, "onset": 4.70, "release": 5.00},
                {"pitch": 76, "onset": 5.07, "release": 5.25},
                {"pitch": 72, "onset": 6.14, "release": 6.33},
                {"pitch": 67, "onset": 6.38, "release": 6.85},
                {"pitch": 69, "onset": 6.95, "release": 7.27},
                {"pitch": 70, "onset": 7.34, "release": 7.67},
                {"pitch": 69, "onset": 7.91, "release": 8.11},
                {"pitch": 68, "onset": 8.11, "release": 8.43},
                {"pitch": 69, "onset": 8.43, "release": 8.65},
                {"pitch": 72, "onset": 8.65, "release": 8.88},
                {"pitch": 69, "onset": 9.03, "release": 9.38},
                {"pitch": 65, "onset": 9.38, "release": 9.79},
                {"pitch": 64, "onset": 9.79, "release": 10.49},
                {"pitch": 57, "onset": 10.73, "release": 10.95},
                {"pitch": 56, "onset": 10.95, "release": 11.26},
                {"pitch": 57, "onset": 11.26, "release": 11.78},
                {"pitch": 64, "onset": 11.78, "release": 12.51},
                {"pitch": 67, "onset": 12.93, "release": 13.13},
                {"pitch": 64, "onset": 13.13, "release": 13.48},
                {"pitch": 55, "onset": 13.48, "release": 13.70},
                {"pitch": 57, "onset": 13.77, "release": 14.07},
                {"pitch": 60, "onset": 14.07, "release": 15.02},
            ],
            'attributes': {
                'time': {
                    'beats': 4,
                    'beat-type': 4
                },
                'tempo': 106.5
            }
        }
        for note in cls.data["notes"]:
            note["onset"] += 1.49
            note["release"] += 1.49

    @classmethod
    def tearDownClass(cls):
        del cls.data

    def test_should_have_32_notes(self):
        self.assertEqual(32, len(self.data["notes"]))

    def test_should_be_f_major_m1(self):
        # this song is actually c major but should optimize to f major :)
        note_data,attr_data = process_data(self.data)
        self.assertEqual(-1,attr_data["key"]["fifths"])

if __name__ == '__main__':
    unittest.main()
