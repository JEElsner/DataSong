import numpy as np

# scale = ['C', 'CS', 'D', 'DS', 'E', 'F', 'FS', 'G', 'GS', 'A', 'AS', 'B'] # Chromatic
# scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B'] # Major
scale = ['BF', 'DF', 'EF', 'E', 'F', 'AF', 'B']  # Pentatonic
octave_min = 3
octave_range = 4
bpm = 120
a4_freq = 440

note_names = {'C': 0, 'CS': 1, 'DF': 1, 'D': 2, 'DS': 3, 'EF': 3, 'E': 4, 'F': 5,
              'FS': 6, 'GF': 6, 'G': 7, 'GS': 8, 'AF': 8, 'A': 9, 'AS': 10, 'BF': 10, 'B': 11}

print('Using Scale: {0}'.format(scale))
print('Over {0} octaves'.format(octave_range))
print('Beginning with octave: {0}'.format(octave_min))


def midi(note_name, octave=4):

    def parse(note, octave=octave):
        for i in range(len(note), 0, -1):
            if i == 0:
                raise ValueError

            if note[:i].isalpha():
                letter = note[:i].upper()
                try:
                    octave = int(note[i:])
                except ValueError:
                    pass
                break

        return 12 * (octave+1) + note_names[letter]

    if isinstance(note_name, list) or isinstance(note_name, np.ndarray):
        note_name = np.array(note_name)
        return np.fromiter((parse(note, octave=o) for note, o in zip(note_name, np.resize(octave, note_name.shape))), int)
    else:
        return parse(note_name)


midi_notes = np.array([midi(scale, octave=o)
                       for o in np.arange(octave_range) + octave_min]).flatten()


def frequency(note):
    if isinstance(note, str):
        note = midi(note)

    return np.power(2, (note-69)/12) * a4_freq


def to_notes(data):
    # Create the scale specified on the octave range specified
    # possible_notes = [midi(l, octave=o) for l in scale for o in range(
    #     octave_min, octave_min + octave_range + 1)]

    # Make the data set on the range of >=0 with the minimum value being 0
    data -= min(data)

    # Scale the data into discreet increments between 0 and len(possible_notes)
    data = np.floor(data / np.ceil(max(data)) *
                    (len(midi_notes) - 1)).astype(int)

    # Calculate the midi note values for the data set, so that the minimum is the lowest note, the maximum is the highest note, and the rest are evenly distributed throughout the scale
    return np.fromiter((midi_notes[i] for i in data), int)
