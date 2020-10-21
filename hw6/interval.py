###############################################################################

from pitch import Pitch
import random

class Interval:

    # span 0-7, qual 0-12, xoct 0-10, sign -1 or 1
    _quals = ('ddddd', 'ooooo', 'dddd', 'oooo', 'ddd', 'ooo', 'dd', 'oo', 'd', 'o', 'm', 'm', 'P', 
    'P', 'M', 'M', 'a', '+', 'aa', '++', 'aaa', '+++', 'aaaa', '++++', 'aaaaa', '+++++')
    # 2d dictionary for semitones that I look up given a span and a quality levelss
    _UNISON, _SECOND, _THIRD, _FOURTH, _FIFTH, _SIXTH, _SEVENTH = 0, 2, 4, 5, 7, 9, 11
    _safe_quals_dict = {e:(i // 2) for i,e in enumerate(_quals)}
    _semitones = (_UNISON, _SECOND, _THIRD, _FOURTH, _FIFTH, _SIXTH, _SEVENTH)
    
    def __init__(self, arg, other=None):
        if (isinstance(arg, str)):
            self._init_from_string(arg)
            return
        elif (isinstance(arg, list) and all(isinstance(e, int) for e in arg) and len(arg) == 4):
            self._init_from_list(arg[0], arg[1], arg[2], arg[3])
            return
        elif (isinstance(arg, Pitch) and isinstance(other, Pitch)):
            self._init_from_pitches(arg, other)
            return
        raise TypeError(f'Invalid input: {arg} of type: {type(arg)}')

    
    def _init_from_list(self, span, qual, xoct, sign):
        if ((0 <= span <= 7) and (0 <= qual <= 12) and (0 <= xoct <= 10) and (sign == 1 or sign == -1)):
            self.span = span
            self.qual = qual
            self.xoct = xoct
            self.sign = sign
        else:
            raise ValueError(f'Values out of range for Interval.  span: {span} qual: {qual} xoct: {xoct} sign: {sign}')
        return self

    
    def _init_from_string(self, name):
        if not isinstance(name, str):
            raise TypeError(f'Cannot convert {type(name)} {name} to Interval')
        try:
            end = None
            n = -1
            while (n >= -len(name) and name[n].isnumeric()):
                end = name[n:]
                n -= 1
            if (end == None):
                raise ValueError(f'No span provided in {name}')
            to_span = int(end)
            to_qual = name[:name.index(end)]
            
            print("to_span: ", to_span)
            print("to_qual: ", to_qual)

            if ((to_span % 7 - 1) in range(8) and name[0] == '-' and to_qual[1:] in self._safe_quals_dict):
                self._init_from_list(to_span % 7 - 1, self._safe_quals_dict[to_qual[1:]], max(to_span // 9 - 1, 0), -1)
            elif ((to_span % 7 - 1) in range(8) and to_qual in self._safe_quals_dict):
                self._init_from_list(to_span % 7 - 1, self._safe_quals_dict[to_qual], max(to_span // 9 - 1, 0), 1)
            else:
                raise ValueError(f'Invalid interval name {name}')
        except Exception:
            raise ValueError(f'Invalid interval name {name}')

    
    def _init_from_pitches(self, pitch1, pitch2):
        pass
    

    def __str__(self):
        return f'<Interval: {self.string()} {self.to_list()} {hex(id(self))}>'


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
        if (self.sign == -1):
            return '-' + self._quals[self.qual * 2] + str(self.span + 1)
        else:
            return self._quals[self.qual * 2] + str(self.span + 1)


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
        return [self.span, self.qual, self.xoct, self.sign]


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
        base = self._semitones[self.span]
        if (base in {_UNISON, _FOURTH, _FIFTH} and (self.qual in range(0, 5))): # if dim
            return base + (self.qual - 5) + (12 * xoct)
        elif (base in {_UNISON, _FOURTH, _FIFTH} and self.qual in range(8, 13)): # if aug
            return base + (self.qual - 7) + (12 * xoct)
        elif (base in {_SECOND, _THIRD, _SIXTH, _SEVENTH} and (self.qual in range(0, 5))): # if dim
            return base + (self.qual)
        elif (base in {_SECOND, _THIRD, _SIXTH, _SEVENTH} and (self.qual in range(8, 13))): # if aug

        elif (base in {_SECOND, _THIRD, _SIXTH, _SEVENTH} and (self.qual in range(5, 8))): # if min/maj/p

        else:
            return base


    
    def add(self, other):
        # figure out what the diatonic span would be, and then look at the semitonal content
        pass

    
    def transpose(self, p):
        pass


def test():
    # Add your testing code here!
    print(Interval([7, 1, 0, 1]))
    print(Interval([random.randint(0, 7), random.randint(0, 12), random.randint(0, 10), random.randint(-1, 1)]))


if __name__ == '__main__':
    test()