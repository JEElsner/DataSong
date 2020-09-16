import unittest

import numpy as np

import converter


class TestMidiConverter(unittest.TestCase):
    def test_one_long_letter(self):
        self.assertEqual(converter.midi('c4'), 60)
        self.assertEqual(converter.midi('A4'), 69)

    def test_flats_and_sharps(self):
        self.assertEqual(converter.midi('BF0'), 22)
        self.assertEqual(converter.midi('CS4'), 61)

    def test_no_octave(self):
        self.assertEqual(converter.midi('C'), 60)
        self.assertEqual(converter.midi('BF'), 70)

    def test_specified_octave(self):
        self.assertEqual(converter.midi('C', octave=8), 108)
        self.assertEqual(converter.midi('BF', octave=5), 82)
        self.assertEqual(converter.midi('C4', octave=7), 60)

    def test_two_digit_octave(self):
        self.assertEqual(converter.midi('C-1'), 0)
        self.assertEqual(converter.midi('BF-1'), 10)
        self.assertEqual(converter.midi('A10'), 141)
        self.assertEqual(converter.midi('FS10'), 138)

    def test_vfunc_list(self):
        notes = ['A4', 'BF3', 'C', 'FS']
        midi = [69, 58, 60, 66]

        out = converter.midi(notes)
        for o, m in zip(out, midi):
            self.assertEqual(o, m)

    def test_vfunc_ndarray(self):
        notes = np.array(['A4', 'BF3', 'C', 'FS'])
        midi = [69, 58, 60, 66]

        out = converter.midi(notes)
        for o, m in zip(out, midi):
            self.assertEqual(o, m)

    def test_vfunc_octave(self):
        notes = np.array(['A4', 'BF3', 'C', 'FS'])
        midi = [69, 58, 108, 114]

        out = converter.midi(notes, octave=8)
        for o, m in zip(out, midi):
            self.assertEqual(o, m)

    def test_vfunc_octave_arr(self):
        notes = np.array(['A4', 'BF3', 'C', 'FS'])
        octs = np.array([1, 2, 3, 5])
        midi = [69, 58, 48, 78]

        out = converter.midi(notes, octave=octs)
        for o, m in zip(out, midi):
            self.assertEqual(o, m)


if __name__ == '__main__':
    unittest.main()
