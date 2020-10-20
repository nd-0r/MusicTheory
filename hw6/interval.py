###############################################################################

from .pitch import Pitch
import random

class Interval:

    # span 0-7, qual 0-12, xoct 0-10, sign -1 or 1

    def __init__(self, arg, other=None):
        if (isinstance(arg, str)):
            self._init_from_string(arg)
        elif (isinstance(arg, list) and all((isinstance(e, int) for e in arg)) and len(arg) == 4):
            self._init_from_list(arg[0], arg[1], arg[2], arg[3])
        elif (isinstance(arg, Pitch) and isinstance(other, Pitch)):
            self._init_from_pitches(arg, other)
        raise TypeError("Invalid input")

    
    def _init_from_list(self, span, qual, xoct, sign):
        if ((0 <= span <= 7) and (0 <= qual <= 12) and (0 <= xoct <= 10) and (sign == 1 or sign == -1)):
            self.span = span
            self.qual = qual
            self.xoct = xoct
            self.sign = sign
        else:
            raise ValueError(f'Values out of range for Interval.  span: {span} qual: {qual} xoct: {xoct} sign: {sign}')

    
    def _init_from_string(self, name):
        pass

    
    def _init_from_pitches(self, pitch1, pitch2):
        pass
    

    def __str__(self):
        return f'<Interval: {self.string()} {hex(id(self))}>'


    def __repr__(self):
        return f'Interval("{self.string()}")'


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


    def string(self):
        return ''


    def full_name(self, *, sign=True):
        pass


    def span_name(self):
        pass

    def quality_name(self):
        pass


    def matches(self, other):
        pass


    def lines_and_spaces(self):
        pass


    def _to_iq(self, name):
        pass


    def to_list(self):
        pass


    def is_unison(self, qual=None):
        pass


    def is_second(self, qual=None):
        pass
    
    def is_third(self, qual=None):
        pass


    def is_fourth(self, qual=None):
        pass


    def is_fifth(self, qual=None):
        pass


    def is_sixth(self, qual=None):
        pass


    def is_seventh(self, qual=None):
        pass

    
    def is_octave(self, qual=None):
        pass


    def is_diminished(self):
        pass
    

    def is_minor(self):
        pass

    
    def is_perfect(self):
        pass

    
    def is_major(self):
        pass

    
    def is_augmented(self):
        pass

    
    def is_perfect_type(self):
        pass

    
    def is_imperfect_type(self):
        pass

        
    def is_simple(self):
        pass

        
    def is_compound(self):
        pass

    
    def is_ascending(self):
        pass

    
    def is_descending(self):
        pass

    
    def is_consonant(self):
        pass

                   
    def is_dissonant(self):
        pass

    
    def complemented(self):
        pass

    
    def semitones(self):
        pass

    
    def add(self, other):
        pass

    
    def transpose(self, p):
        pass


def test():
    # Add your testing code here!
    print(Interval([7, 1, 0, 1]))
    print(Interval([random.randint(0, 7), random.randint(0, 12), random.randint(0, 10), random.randint(-1, 1)]))


if __name__ == '__main__':
    test()