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


class Pitch (PitchBase):

    _letters = ('C', 'D', 'E', 'F', 'G', 'A', 'B')
    _octaves = ('00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
    _accidentals = ('bb', 'ff', 'b', 'f', '', 'n', '#', 's', '##', 'ss')


    # Create the pnum class here, see documentation in pitch.html
    pnums = IntEnum('Pnum', [('Cff', )])
 

    def __new__(cls, arg=None):
        if isinstance(arg, list) and (len(arg) == 3) and all(type(e, int) for e in arg):
            cls._values_to_pitch(arg[1], arg[2], arg[3])
        elif isinstance(arg, str):
            cls._string_to_pitch(arg)


    @classmethod
    def _string_to_pitch(cls, arg):
        try:
            letter = arg[0:1]
            if (arg[-2:] == '00'):
                octave = '00'
                if len(arg) > 4:
                    raise ValueError(f'{arg} is not a valid pitch')
                accidental = arg[1:-2]
            else:
                octave = arg[-1]
                if len(arg) > 3:
                    raise ValueError(f'{arg} is not a valid pitch')
                accidental = arg[1:-1]
        except Exception:
            raise ValueError(f'{arg} is not a valid pitch')
        
        return cls._values_to_pitch(letter, accidental, octave)


    @classmethod
    def _values_to_pitch(cls, let, acc, ova): 
        if (let not in cls._letters):
            raise ValueError(f'{let} is not a valid pitch')
        if (ova not in cls._octaves):
            raise ValueError(f'{ova} is not a valid octave')
        if acc not in cls._accidentals:
            raise ValueError(f'{acc} is not a valid accidental')
        lnum = cls._letters.index(let)
        anum = cls._letters.index(acc)
        onum = cls._letters.index(ova)
        if (onum == 0 and (anum // 2 < 2 and lnum == 0)) or (onum == 9 and (anum // 2 > 2 and lnum == 4) or (anum // 2 > 0 and lnum == 5) or lnum == 6):
            raise ValueError(f'Pitch is out of midi range')

        super(Pitch, cls).__new__(cls, let, acc, ova)



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
        return ''


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
        return ''


    def __lt__(self, other):
        pass


    def __le__(self, other):
        pass


    def __eq__(self, other):
        pass


    def __ne__(self, other):
        pass


    def __ge__(self, other):
        pass


    def __gt__(self, other):
        pass


    def pos(self):
        pass


    def is_empty(self):
        pass


    def string(self):
        pass


    def keynum(self):
        pass


    def pnum(self):
        pass

    
    def pc(self):
        pass

    
    def hertz(self):
        pass


    @classmethod
    def from_keynum(cls, keynum, acci=None):
        pass



if __name__ == '__main__':
    # Add your testing code here!
    pass

