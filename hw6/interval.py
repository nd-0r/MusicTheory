###############################################################################

from .pitch import Pitch

class Interval:

    def __init__(self, arg, other=None):
        pass

    
    def _init_from_list(self, span, qual, xoct, sign):
        pass

    
    def _init_from_string(self, name):
        pass

    
    def _init_from_pitches(self, pitch1, pitch2):
        pass
    

    def __str__(self):
        return ''


    def __repr__(self):
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


    def string(self):
        pass


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


if __name__ == '__main__':
    # Add your testing code here!
    pass

