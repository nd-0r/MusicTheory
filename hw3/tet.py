# tet.py : Twelve-tone Equal Temperment (TET) 
# See tet.html for module documentation.

import math

_letters = {'A':9, 'B':11, 'C':0, 'D':2, 'E':4, 'F':5, 'G':7}
_accidentals = {'bb':-2, 'ff':-2, 'b':-1, 'f':-1, '#':1, 's':1, '##':2, 'ss':2}
_template = ('C','','D','','E','F','','G','', 'A','','B')
_default = ('C','C#','D','Eb','E','F','F#','G','Ab', 'A','Bb','B')

# test this:
def hertz_to_midi(hertz):
    if type(hertz) is not float or (hertz < 0):
        raise ValueError(f'You must provide a frequency as a positive float')
    return math.floor(69 + math.log2(hertz / 440.0) * 12)


def midi_to_hertz(midi):
    if type(midi) is not int:
        raise ValueError(f'You must provide a midi key number as an integer')
    return 440 * 2 ** ((midi-69)/12)


def midi_to_pc(midi):
    if type(midi) is not int:
        raise ValueError(f'You must provide a midi key number as an integer')
    return midi % 12

# test this:
def pitch_to_midi(pitch):
    try:
        letter = pitch[0:1]
        accidental = pitch[1:-1]
        octave = 0
        if (pitch[-1] == '00'):
            octave = -1
        else:
            octave = int(pitch[-1])
        if(letter not in {'A', 'B', 'C', 'D', 'E', 'F', 'G'} or (accidental not in _accidentals) or (octave != '00' or int(octave) < 0 or int(octave) > 12)):
            raise ValueError(f'{pitch} is not a valid pitch')
    except (Exception):
        raise ValueError(f'Please enter a valid pitch')

    return ((12 * octave) + int(_letters[letter]) + int(_accidentals[accidental]))

# test this:
def midi_to_pitch(midi, accidental=None):

    if (midi > 127 or midi < 0):
        raise ValueError(f'{midi} is not a valid midi key number')
    elif (accidental not in {"bb", "ff", "b", "f", "#", "s", "##", "ss"} and accidental != None):
        raise ValueError(f'{accidental} is not a valid accidental')

    octave = midi // 12
    pc = midi_to_pc(midi)

    if ((pc == (1, 6, 8) and (accidental == "bb" or accidental == "ff")) or (pc == (0, 3, 5, 8, 10) and (accidental == "##" or accidental == "ss"))):
        raise ValueError(f'Cannot apply express pitch class {pc} with the accidental {accidental}')
    if (accidental == None):
        return _default[pc] + str(octave)
    
    offset = _accidentals[accidental]
    letter = _template[((pc - offset) + 12) % 12]
    octave += (pc - offset) // 12

    return  letter + accidental + str(octave)


def hertz_to_pitch(hertz):
    midi = hertz_to_midi(hertz)
    return midi_to_pitch(midi)


def pitch_to_hertz(pitch):
    midi = pitch_to_midi(pitch)
    assert(isinstance(midi, float))
    return midi_to_hertz(midi)


if __name__ == '__main__':
    print("Testing...")
    
    for i in range(60, 72):
        print(midi_to_pitch(i))

    print("Done!")
