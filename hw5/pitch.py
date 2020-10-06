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
PitchBase = None


class Pitch (PitchBase):


    # Create the pnum class here, see documentation in pitch.html
    pnums = None
 

    def __new__(cls, arg=None):
        pass


    @classmethod
    def _string_to_pitch(cls, arg):
        pass


    @classmethod
    def _values_to_pitch(cls, let, acc, ova):
        pass


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

