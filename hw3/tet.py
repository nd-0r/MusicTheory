# tet.py : Twelve-tone Equal Temperment (TET) 
# See tet.html for module documentation.

import math

_letters = {'A':9, 'B':11, 'C':0, 'D':2, 'E':4, 'F':5, 'G':7}
_accidentals = {'bb':-2, 'ff':-2, 'b':-1, 'f':-1, '':0, '#':1, 's':1, '##':2, 'ss':2}
_template = ('C','','D','','E','F','','G','', 'A','','B')
_default = ('C','C#','D','Eb','E','F','F#','G','Ab', 'A','Bb','B')

# GOOD
def hertz_to_midi(hertz):
    if not isinstance(hertz, float) or (hertz < 0):
        raise ValueError(f'You must provide a frequency as a positive float')
    out = math.floor(69 + math.log2(hertz / 440.0) * 12)
    if not (0 <= out < 128):
        raise ValueError(f'{out} is not a valid midi key number')
    return out

# GOOD
def midi_to_hertz(midi):
    if type(midi) is not int or not (0 <= midi < 128):
        raise ValueError(f'{midi} is not a valid midi key number')
    return 440 * 2 ** ((midi-69)/12)

# GOOD
def midi_to_pc(midi):
    if type(midi) is not int or not (0 <= midi < 128):
        raise ValueError(f'You must provide a midi key number as an integer')
    return midi % 12

# refactor
def pitch_to_midi(pitch):
    letter = ''
    octave = 0
    accidental = ''
    offset = 0
    try:
        letter = pitch[0:1]
        if (pitch[-2:] == '00'):
            octave = -1
            if (len(pitch) > 3):
                accidental = pitch[1:-2]
        else:
            octave = int(pitch[-1])
            if (len(pitch) > 2):
                accidental = pitch[1:-1]
        if(letter not in {'A', 'B', 'C', 'D', 'E', 'F', 'G'}):
            raise ValueError(f'{pitch} is not a valid pitch')
        if (octave < -1 or octave > 12):
            raise ValueError(f'{octave} is not a valid octave')
        if accidental not in dict.keys(_accidentals):
            raise ValueError(f'{accidental} is not a valid accidental')
        offset = _accidentals[accidental]
        # for accidental in dict.keys(_accidentals):
        #     if (str(accidental) in pitch and (str.count(pitch, accidental) == 1)):
        #         offset = _accidentals[accidental]
        #         break
    except Exception:
            raise ValueError(f'{pitch} is not a valid pitch')
    midi_key = ((12 * (octave + 1)) + int(_letters[letter]) + offset)
    if not (0 <= midi_key < 128):
        raise ValueError(f'{pitch} does not correspond to a valid midi key {midi_key}')
    if (__name__ == '__main__'):
        print("letter: " + letter)
        print("offset: " + str(offset))
        print("octave: " + str(octave))
    return midi_key

# refactor
def midi_to_pitch(midi, accidental=None):

    if (not isinstance(midi, int)):
        raise ValueError(f'Please provide midi key as an integer')
    if (accidental != None and not isinstance(accidental, str)):
        raise ValueError(f'Please provide accidental as a string')

    if (midi > 127 or midi < 0):
        raise ValueError(f'{midi} is not a valid midi key number')
    elif (accidental not in {"bb", "ff", "b", "f", "#", "s", "##", "ss"} and accidental != None):
        raise ValueError(f'{accidental} is not a valid accidental')

    octave = (midi // 12) - 1
    pc = midi_to_pc(midi)
    if __name__ == '__main__':
        print(pc)

    if ( (pc in {1, 4, 6, 8, 11} and (accidental in {"bb", "ff"})) or (pc in {0, 3, 5, 8, 10} and (accidental in {"##", "ss"})) or (pc in {0, 2, 5, 7, 9} and (accidental in {"b", "f"})) or (pc in {2, 4, 7, 9, 11} and (accidental in {"#", "s"})) ):
        raise ValueError(f'Cannot express pitch class {pc} with the accidental {accidental}')

    if (accidental == None):
        return _default[pc] + str(octave)
    
    offset = _accidentals[accidental]
    letter = _template[((pc - offset) + 12) % 12]
    octave += (pc - offset) // 12

    return  letter + accidental + str(octave)


def hertz_to_pitch(hertz):
    if not isinstance(hertz, float) or (hertz < 20 or hertz > 20000):
        raise ValueError(f'Please provide the frequency as a float between 20 and 20,000 hertz')
    midi = hertz_to_midi(hertz)
    assert(isinstance(midi, int))
    return midi_to_pitch(midi)


def pitch_to_hertz(pitch):
    if not isinstance(pitch, str):
        raise ValueError(f'please provide the pitch as a string')
    midi = pitch_to_midi(pitch)
    assert(isinstance(midi, int))
    return midi_to_hertz(midi)


if __name__ == '__main__':
    print("Testing...")

    # print("pitch_to_midi:")
    # print(pitch_to_midi("A4"), end="\n\n")

    # print("hertz_to_pitch:")
    # count = 1
    # for i in range(100, 10000, 10 * 2**count):
    #     print(hertz_to_pitch(float(i)))
    #     count += 1

    # for i in range(60, 72):
    #     print(midi_to_pitch(i))

    print("Done!")
