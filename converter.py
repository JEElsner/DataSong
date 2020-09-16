import numpy as np

# === Configuration Options === #


# scale = ['C', 'CS', 'D', 'DS', 'E', 'F', 'FS', 'G', 'GS', 'A', 'AS', 'B'] # Chromatic
# scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B'] # Major
scale = ['BF', 'DF', 'EF', 'E', 'F', 'AF', 'B']  # Pentatonic

octave_min = 3  # The lowest octave played
octave_range = 4  # The total range of octaves to select notes
a4_freq = 440  # The frequency of A4 in Hertz


# === Notes === #

# Map Spelled notes to their value in scientific pitch notation
# F suffix indicates flat
# S suffix indicates sharp
# More on scientific pitch notation, and a table of values:
# https://en.wikipedia.org/wiki/Scientific_pitch_notation#Table_of_note_frequencies
note_names = {'C': 0, 'CS': 1, 'DF': 1, 'D': 2, 'DS': 3, 'EF': 3, 'E': 4,
              'F': 5, 'FS': 6, 'GF': 6, 'G': 7, 'GS': 8, 'AF': 8, 'A': 9,
              'AS': 10, 'BF': 10, 'B': 11}


# Print current configuration when the module is loaded
print('Using Scale: {0}'.format(scale))
print('Over {0} octaves'.format(octave_range))
print('Beginning with octave: {0}'.format(octave_min))


def midi(note_name, octave=4):
    '''
    Converts a spelled note name or list of spelled note names to their
    scientific pitch notation value.

    This function essentially converts between note names and numerical values
    in this table:
    https://en.wikipedia.org/wiki/Scientific_pitch_notation#Table_of_note_frequencies

    Arguments:

        note_name   The spelled name of the note, such as C, BF, or FS. See the
            note_names variable for all possible examples. The note_name can be
            suffixed by a number indicating the octave at which it is played.
            This number will override the octave keyword argument.

        octave      Keyword argument indicating the octave of the note. The
            default value is 4. This argument is ignored if an octave is
            suffixed to the note_name

    Note: This function can be used as a NumPy Universal function. This likely
    has little efficiency advantage, but is offered for convenience.
    '''

    # Function that actually does the parsing of the note_name string
    # Used differently whether this function is called with one note_name or as
    #   a universal function
    def parse(note, octave=octave):
        # Check if each character is a letter
        for i in range(len(note), 0, -1):
            if i == 0:
                raise ValueError

            # Check if the left side of the string to the current index is a
            # letter. If it is, use it for the note name
            if note[:i].isalpha():
                letter = note[:i].upper()
                try:
                    # Try to use the rest of the string as the octave number
                    octave = int(note[i:])
                except ValueError:
                    pass
                break

        # Use a formula to convert the spelled note and octave into scientific
        # pitch notation
        # Looks up the numerical value in the note_names dictionary
        return 12 * (octave+1) + note_names[letter]

    # Code to make this function a unviersal function
    if isinstance(note_name, list) or isinstance(note_name, np.ndarray):
        # In the case that a list or NumPy ndarray was passed
        # Iterate through the array and return the numerical value of each note
        note_name = np.array(note_name)
        return np.fromiter(
            (parse(note, octave=o)  # Operation done on each iteration
             for note, o in zip(note_name,  # What we're iterating through
                                np.resize(octave, note_name.shape))),
            int)
    else:
        # In the case of a single value
        # Just parse the note
        return parse(note_name)


# Perform the Scientific Pitch Notation conversion on the range of notes to be
# used when processing data into notes
midi_notes = np.array([
    midi(scale, octave=o)
    for o in np.arange(octave_range) + octave_min]
).flatten()


def frequency(note):
    '''
    Convert a numerical note value in scientific pitch notation or a list or
    NumPy ndarray of these into their associated frequencies
    '''
    if isinstance(note, str):
        note = midi(note)

    # Formula to convert MIDI numerical note values to frequency
    # Information and Formula on Wikipedia:
    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    return np.power(2, (note-69)/12) * a4_freq


def to_notes(data):
    '''
    Process data into notes in scientific pitch notation as specified by
    configuration values in the module.

    Returns:    A Numpy ndarray of numerical notes that correlates to the data
    '''

    # Make the data set on the range of >=0 with the minimum value being 0
    data -= min(data)

    # Scale the data into discrete increments between 0 and len(possible_notes)
    data = np.floor(data / np.ceil(max(data)) *
                    (len(midi_notes) - 1)).astype(int)

    # Calculate the midi note values for the data set, so that the minimum is
    # the lowest note, the maximum is the highest note, and the rest are evenly
    # distributed throughout the scale
    return np.fromiter((midi_notes[i] for i in data), int)
