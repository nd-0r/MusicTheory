###############################################################################
"""
A class that implements musical pitches.

The Pitch class represent equal tempered pitches and returns information
in hertz, keynum, pitch class, Pnum  and pitch name formats.  Pitches
can be compared using standard math relations and maintain proper spelling
when complemented or transposed by an Interval.
"""

from enum import IntEnum
from math import pow
from collections import namedtuple

# Create the namedtuple super class for Pitch with three attributes:
# letter, accidental, and octave.  See your ratio.py file for an example.
PitchBase = namedtuple('PitchBase', ['let', 'acc', 'oct'])

_letters = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
_octaves = ('00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
_accidentals = ('ff', 'bb', 'f', 'b', 'n', '', 's', '#', 'ss', '##')
_template = ('C','','D','','E','F','','G','', 'A','','B')
_default = ('C','C#','D','Eb','E','F','F#','G','Ab', 'A','Bb','B')

class Pitch (PitchBase):

    # Create the pnum class here, see documentation in pitch.html
    # toPnums = []
    # for i,l in enumerate(_letters):
    #     print('1', str(i))
    #     for j,a in enumerate(_accidentals[::2]):
    #         print('2', str(j))
    #         toPnums.append((str(l) + str(a), (i<<4) + j))
    pnums = IntEnum('Pnum', [(str(l) + str(a), (i<<4) + j) for j,a in enumerate(_accidentals[::2]) for i,l in enumerate(_letters)])
 

    def __new__(cls, arg=None):
        if isinstance(arg, list) and (len(arg) == 3) and all(isinstance(e, int) for e in arg):
            try:
                return super(Pitch, cls).__new__(cls, _letters[arg[0]], _accidentals[arg[1] * 2], _octaves[arg[2]])
            except IndexError:
                raise ValueError(f'input list out of range')
        elif isinstance(arg, str):
            return cls._string_to_pitch(arg)
        elif arg == None:
            return super(Pitch, cls).__new__(cls, None, None, None)
        else:
            raise TypeError(f'Cannot make new pitch from type: {type(arg)}')


    @classmethod
    def _string_to_pitch(cls, arg):
        try:
            letter = arg[0:1].upper()
            if (arg[-2:] == '00'):
                octave = '00'
                if len(arg) > 4:
                    raise ValueError(f'{arg} is not a valid pitch')
                accidental = arg[1:-2]
            else:
                octave = arg[-1]
                if len(arg) > 4:
                    raise ValueError(f'{arg} is not a valid pitch')
                accidental = arg[1:-1]
        except Exception:
            raise ValueError(f'{arg} is not a valid pitch')
        
        return cls._values_to_pitch(letter, accidental, octave)


    @classmethod
    def _values_to_pitch(cls, let, acc, ova): 
        if (let not in _letters):
            raise ValueError(f'{let} is not a valid pitch')
        if (ova not in _octaves):
            raise ValueError(f'{ova} is not a valid octave')
        if acc not in _accidentals:
            raise ValueError(f'{acc} is not a valid accidental')
        if (__name__ == '__main__'):
            print(let)
            print(acc)
            print(ova, end='\n\n')
        lnum = _letters.index(str(let))
        anum = _accidentals.index(str(acc))
        onum = _octaves.index(str(ova))
        if (__name__ == '__main__'):
            print(lnum)
            print(anum)
            print(onum)
        if (onum == 0 and (anum // 2 < 2 and lnum == 0)) or (onum == 10 and ((anum // 2 > 2 and lnum == 4) or (anum // 2 > 0 and lnum == 5) or lnum == 6)):
            raise ValueError(f'Pitch is out of midi range')

        return super(Pitch, cls).__new__(cls, let, acc, ova)



    def __str__(self):
        # It is important that you implement the __str__ method precisely.
        # In particular, for __str__ you want to see '<', '>', '0x' in 
        # your output string.  The format of your output strings from your
        # version of this function must look EXACTLY the same as in the two
        # examples below.
        # 
        #     >>> str(Pitch("C#6"))
        #     '<Pitch: C#6 0x7fdb17e2e950>'
        #     >>> str(Pitch())
        #     '<Pitch: empty 0x7fdb1898fa70>'

        # if self.is_empty():
        #     return str(f'<Pitch: empty {hex(id(self))}>')
        # return str(f'<Pitch: {self.string()} {hex(id(self))}>')
        # To accomodate the autograder:
        if self.is_empty():
            return str(f'<Pitch: empty>')
        return str(f'<Pitch: {self.string()}>')


    def __repr__(self):
        # Note: It is the __repr__ (not the __str__) function that the autograder
        # uses to compare results. So it is very important that you implement this
        # method precisely. In particular, for __repr__ you want to see double
        # quotes inside single quotes and NOT the other way around. The format of
        # your output strings from your version of this function must look 
        # EXACTLY the same as in the two examples below.
        #
        #     >>> str(Pitch("C#6"))
        #     '<Pitch: C#6 0x7fdb17e2e950>'
        #     >>> repr(Pitch("Bbb3"))
        #     'Pitch("Bbb3")'
        return str(f'Pitch("{self.string()}")')


    def __lt__(self, other):
        if (not isinstance(other, Pitch)):
            raise TypeError(f'Cannot compare Pitch with {type(other)}')
        # return self.pnum() < other.pnum()
        return self.pos() < other.pos()

    def __le__(self, other):
        if (not isinstance(other, Pitch)):
            raise TypeError(f'Cannot compare Pitch with {type(other)}')
        # return self.pnum() <= other.pnum()
        return self.pos() <= other.pos()


    def __eq__(self, other):
        if (not isinstance(other, Pitch)):
            raise TypeError(f'Cannot compare Pitch with {type(other)}')
        # return self.pnum() == other.pnum()
        return self.pos() == other.pos()


    def __ne__(self, other):
        if (not isinstance(other, Pitch)):
            raise TypeError(f'Cannot compare Pitch with {type(other)}')
        # return self.pnum() != other.pnum()
        return self.pos() != other.pos()


    def __ge__(self, other):
        if (not isinstance(other, Pitch)):
            raise TypeError(f'Cannot compare Pitch with {type(other)}')
        # return self.pnum() >= other.pnum()
        return self.pos() >= other.pos()


    def __gt__(self, other):
        if (not isinstance(other, Pitch)):
            raise TypeError(f'Cannot compare Pitch with {type(other)}')
        # return self.pnum() > other.pnum()
        return self.pos() > other.pos()


    def pos(self):
        return (_octaves.index(self.oct)<<8) + (_letters.index(self.let)<<4) + _accidentals.index(self.acc)


    def is_empty(self):
        if self.let == None or self.acc == None or self.oct == None:
            return True
        return False


    def string(self):
        if (_accidentals.index(self.acc) % 2 == 1):
            return f'{self.let}{self.acc}{self.oct}'
        else:
            return f'{self.let}{_accidentals[_accidentals.index(self.acc) + 1]}{self.oct}'


    def keynum(self):
        midi_key = ((12 * _octaves.index(self.oct)) + _template.index(self.let) + ((_accidentals.index(self.acc) // 2) - 2))
        if not (0 <= midi_key < 128):
            raise ValueError(f'{self.string()} does not correspond to a valid midi key {midi_key}')
        return midi_key


    def pnum(self):
        return Pitch.pnums[self.let + _accidentals[_accidentals.index(self.acc) - (_accidentals.index(self.acc) % 2)]]

    
    def pc(self):
        return self.keynum() % 12

    
    def hertz(self):
        return float(440 * 2 ** ((self.keynum() - 69) / 12))


    @classmethod
    def from_keynum(cls, midi, accidental=None):
        if (not isinstance(midi, int)):
            raise ValueError(f'Please provide midi key as an integer')
        if (accidental != None and not isinstance(accidental, str)):
            raise ValueError(f'Please provide accidental as a string')

        if (midi > 127 or midi < 0):
            raise ValueError(f'{midi} is not a valid midi key number')
        elif (accidental not in _accidentals and accidental != None):
            raise ValueError(f'{accidental} is not a valid accidental')

        octave = (midi // 12) - 1
        if (octave < 0):
            octave = '00'
        pc = midi % 12
        if __name__ == '__main__':
            print(pc)

        if ( (pc in {1, 4, 6, 8, 11} and (accidental in {"bb", "ff"})) or (pc in {0, 3, 5, 8, 10} and (accidental in {"##", "ss"})) or (pc in {0, 2, 5, 7, 9} and (accidental in {"b", "f"})) or (pc in {2, 4, 7, 9, 11} and (accidental in {"#", "s"})) ):
            raise ValueError(f'Cannot express pitch class {pc} with the accidental {accidental}')

        if (accidental == None):
            return Pitch(_default[pc] + str(octave))
        
        offset = ((_accidentals.index(accidental) // 2) - 2)
        letter = _template[((pc - offset) + 12) % 12]
        octave += (pc - offset) // 12

        return  Pitch(letter + accidental + str(octave))

def test():
    # Add your testing code here!
    # for p in ['F##2', 'Gs8', 'Bb3', 'Df00', 'fff4', 'bbb0', 'cn00', 'Abb9', [0,3,6], [1,2,3], [5,4,3]]:
    #     print(Pitch(p), end='\n\n\n')
    # print(Pitch('C4') < Pitch('A4'))
    # print(Pitch('C4') <= Pitch('A4'))
    # print(Pitch('C4') > Pitch('A4'))
    # print(Pitch('C4') >= Pitch('A4'))
    # print(Pitch('C4') == Pitch('A4'))
    # print(Pitch('C4') != Pitch('A4'))
    # print(Pitch('C4') < Pitch('A3'))
    # print(Pitch('C4') <= Pitch('A3'))
    # print(Pitch('C4') > Pitch('A3'))
    # print(Pitch('C4') >= Pitch('A3'))
    # print(Pitch('C4') == Pitch('A3'))
    # print(Pitch('C4') != Pitch('A3'))
    # print(Pitch('E##3') < Pitch('Fbb3'))
    # print(Pitch('E##3') <= Pitch('Fbb3'))
    # print(Pitch('E##3') > Pitch('Fbb3'))
    # print(Pitch('E##3') >= Pitch('Fbb3'))
    # print(Pitch('E##3') == Pitch('Fbb3'))
    # print(Pitch('E##3') != Pitch('Fbb3'))
    # print(Pitch('B#5') < Pitch('C6'))
    # print(Pitch('B#5') <= Pitch('C6'))
    # print(Pitch('B#5') > Pitch('C6'))
    # print(Pitch('B#5') >= Pitch('C6'))
    # print(Pitch('B#5') == Pitch('C6'))
    # print(Pitch('B#5') != Pitch('C6'))
    # print(Pitch('B#5') < Pitch('C5'))
    # print(Pitch('B#5') <= Pitch('C5'))
    # print(Pitch('B#5') > Pitch('C5'))
    # print(Pitch('B#5') >= Pitch('C5'))
    # print(Pitch('B#5') == Pitch('C5'))
    # print(Pitch('B#5') != Pitch('C5'))
    # print(Pitch('B#5') < Pitch('B#5'))
    # print(Pitch('B#5') <= Pitch('B#5'))
    # print(Pitch('B#5') > Pitch('B#5'))
    # print(Pitch('B#5') >= Pitch('B#5'))
    # print(Pitch('B#5') == Pitch('B#5'))
    # print(Pitch('B#5') != Pitch('B#5'))
    # print(Pitch('Fss4') == Pitch([3,4,5]))

    # These are all off by 13?
    print(Pitch('A4').keynum() )
    print(Pitch('A#4').keynum() )
    print(Pitch('A##4').keynum() )
    print(Pitch('Ab4').keynum() )
    print(Pitch('Abb4').keynum() )

    # These are all off by 11?
    print(Pitch('B7').pc() )
    print(Pitch('B#7').pc())
    print(Pitch('B##7').pc())
    print(Pitch('Bb7').pc() )
    print(Pitch('Bbb7').pc())

    # These are also off...
    print(Pitch('E6').hertz() )
    print(Pitch('E#6').hertz())
    print(Pitch('E##6').hertz())
    print(Pitch('Eb6').hertz())
    print(Pitch('Ebb6').hertz() )
    
    # print(Pitch.from_keynum(66))
    # print(Pitch.from_keynum(72) )
    # print(Pitch.from_keynum(60,'#')  )
    # print(Pitch.from_keynum(96,'bb'))
    # print(Pitch.from_keynum(80))
    # print(Pitch.from_keynum(80,'b')  )
    # print(Pitch.from_keynum(80,'#'))
    # print(Pitch.from_keynum(70)  )
    # print(Pitch.from_keynum(70,'b')  )
    # print(Pitch.from_keynum(70,'bb'))


if __name__ == '__main__':
    test()