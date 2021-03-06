###############################################################################

from .pitch import Pitch
import random

# !!! fix f to b sharp case
# !!! fix midi oob error for pitch to interval
# !!! fix descending case for transpose/pitch_to_interval

class Interval:

    @staticmethod
    def dict_slice(d, start, end):
        return dict((k, d[k]) for i,k in enumerate(d.keys()) if (i in range(start, end))) 

    # span 0-7, qual 0-12, xoct 0-10, sign -1 or 1
    _quals = ('ddddd', 'ooooo', 'dddd', 'oooo', 'ddd', 'ooo', 'dd', 'oo', 'd', 'o', 'm', 'm', 'p', 
    'P', 'M', 'M', 'a', '+', 'aa', '++', 'aaa', '+++', 'aaaa', '++++', 'aaaaa', '+++++')
    # format is {qual_index<0-12> : qual}
    _safe_quals_dict = {e:(i // 2) for i,e in enumerate(_quals)}
    # index vars for readability
    _UNISON, _SECOND, _THIRD, _FOURTH, _FIFTH, _SIXTH, _SEVENTH, _OCTAVE = 0, 1, 2, 3, 4, 5, 6, 7
    # format is {qual_index : offset}
    _perfect_intervals_dict = {0: -5, 1: -4, 2: -3, 3: -2, 4: -1, 6: 0, 8: 1, 9: 2, 10: 3, 11: 4, 12: 5}
    # All imperfect intervals default to major
    # format is {qual_index : offset} removed 6:0.  Let's see if it blows up...
    _imperfect_intervals_dict = {0: -6, 1: -5, 2: -4, 3: -3, 4: -2, 5: -1, 7: 0, 8: 1, 9: 2, 10: 3, 11: 4, 12: 5}
    # format is {span_index : default_span}
    _default_spans = {i:s for i,s in enumerate([0,2,4,5,7,9,11,12])}
    # format is {span_index : {qual_index : offset}}
    _semitones = {_UNISON:_perfect_intervals_dict, _SECOND:_imperfect_intervals_dict, 
    _THIRD:_imperfect_intervals_dict, _FOURTH:_perfect_intervals_dict, 
    _FIFTH:_perfect_intervals_dict, _SIXTH:_imperfect_intervals_dict, 
    _SEVENTH:_imperfect_intervals_dict, _OCTAVE:_perfect_intervals_dict}
    # format is {span_index : span_name}
    _span_names = {i:n for i,n in enumerate(['unison', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'octave'])}
    # format is {qual_index : qual_name}
    _qual_names = {i:n for i,n in enumerate(['quintuply-diminished', 'quadruply-diminished', 'triply-diminished', 'doubly-diminished', 
    'diminished', 'minor', 'perfect', 'major', 'augmented', 'doubly-augmented', 'triply-augmented', 'quadruply-augmented', 
    'quintuply-augmented'])}
    # reverse _qual_names for iq method
    _qual_names_reversed = dict(reversed(pair) for pair in _qual_names.items())
    # format is {midi_span<0-12> : interval}
    _diatonic_intervals = {i:interval for i,interval in enumerate(['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'a4', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8'])}
    # Two-way dictionaries for mapping the indices of qualities (0-12) 
    # to a sliding scale for imperfect and perfect intervals to allow 
    # intuitive stretching and shrinking of intervals.
    # Standard takes an interval quality index and maps it to a sliding
    # scale standard for imperfect/perfect intervals. Reverse does the 
    # opposite
    _qual_scale_devil = {q:i for i,q in enumerate([0,1,2,3,4,8,9,10,11,12])}
    _qual_scale_devil_reverse = dict(reversed(pair) for pair in _qual_scale_devil.items())
    _qual_scale_imperfect = {q:i for i,q in enumerate([0,1,2,3,4,5,7,8,9,10,11,12])}
    _qual_scale_imperfect_reverse = dict(reversed(pair) for pair in _qual_scale_imperfect.items())
    _qual_scale_perfect = {q:i for i,q in enumerate([0,1,2,3,4,6,8,9,10,11,12])}
    _qual_scale_perfect_reverse = dict(reversed(pair) for pair in _qual_scale_perfect.items())

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
        # checks if it is a valid combo of span and qual
        if (span == 0 and xoct > 0):
            span += 7
            xoct -= 1
        elif (span > 7):
            span %= 7
            xoct += (span // 7)
        try:
            # special dicts for unison, second, and third b/c they can't have certain qualities
            print(f'init from list span: {span}')
            print(f'init from list qual: {qual}')
            if (xoct == 0):
                _temp = dict(self._semitones)
                _temp[self._UNISON] = self.dict_slice(self._perfect_intervals_dict, 5, 11)
                _temp[self._SECOND] = self.dict_slice(self._imperfect_intervals_dict, 4, 12)
                _temp[self._THIRD] = self.dict_slice(self._imperfect_intervals_dict, 2, 12)
                _temp[self._FOURTH] = self.dict_slice(self._perfect_intervals_dict, 1, 11)
                _temp[self._FIFTH] = self.dict_slice(self._perfect_intervals_dict, 0, 10)
                _temp[span][qual]
            else:
                self._semitones[span][qual]
        except KeyError:
            raise ValueError(f'Values out of range for Interval.  span: {span} qual: {qual} xoct: {xoct} sign: {sign}')
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
            # find longest number at end of string
            while (n >= -len(name) and name[n].isnumeric()):
                end = name[n:]
                n -= 1
            if (end == None):
                raise ValueError(f'No span provided in {name}')
            to_span = int(end)
            # if compound
            if (to_span > 8):
                to_xoct = (to_span - 1) // 8
                to_span = ((to_span - 1) % 7 + 7) % 7
            else:
                to_span -= 1
                to_xoct = 0
            to_qual = name[:name.index(end)]
            if (to_qual not in ('m', 'M') and to_qual[1:] not in ('m', 'M')):
                to_qual = str.lower(to_qual)
            
            print("to_span: ", to_span)
            print("to_qual: ", to_qual)
            print("to_xoct: ", to_xoct)

            if (to_span in range(8) and name[0] == '-' and to_qual[1:] in self._quals):
                self._init_from_list(to_span, self._safe_quals_dict[to_qual[1:]], to_xoct, -1)
            elif (to_span in range(8) and to_qual in self._quals):
                self._init_from_list(to_span, self._safe_quals_dict[to_qual], to_xoct, 1)
            else:
                raise ValueError(f'Invalid interval name {name}')
        except Exception:
            raise ValueError(f'Invalid interval name {name}')

    
    def _init_from_pitches(self, pitch1, pitch2):
        # gets the pitch class of the not without accidentals
        # fix for midi out of range errors!
        try:
            pitch1_base_keynum = Pitch([pitch1.letter, 2, pitch1.octave]).keynum()
        except ValueError:
            if (pitch1.letter == 5 and pitch1.octave == 10 and pitch1.accidental < 2):
                pitch1_base_keynum = 127 - (pitch1.accidental - 2)
            elif (pitch1.letter == 0 and pitch1.octave == 0 and pitch1.accidental >= 2):
                pitch1_base_keynum = 0 + (pitch1.accidental - 2)
            else:
                raise ValueError(f'invalid pitches')
        try:
            pitch2_base_keynum = Pitch([pitch2.letter, 2, pitch2.octave]).keynum()
        except ValueError:
            if (pitch2.letter == 5 and pitch2.octave == 10 and pitch2.accidental < 2):
                pitch2_base_keynum = 127 - (pitch2.accidental - 2)
            elif (pitch2.letter == 0 and pitch2.octave == 0 and pitch2.accidental >= 2):
                pitch2_base_keynum = 0 + (pitch2.accidental - 2)
            else:
                raise ValueError(f'invalid pitches')
        # print("p1 pc: " + str(pitch1_base_keynum))
        # print("p2 pc: " + str(pitch2_base_keynum))
        # checks if the pitches crossy crossy
        if (pitch2_base_keynum > pitch1_base_keynum and pitch1.keynum() > pitch2.keynum() 
            or pitch2_base_keynum < pitch1_base_keynum and pitch1.keynum() < pitch2.keynum()):
                raise ValueError(f'Cannnot make an interval from pitches that crossy crossy')
        # substracts those pitch classes to get a basic interval to build off
        if (abs(pitch2_base_keynum - pitch1_base_keynum) == 12):
            keynum_span = (pitch2_base_keynum - pitch1_base_keynum)
        else:
            keynum_span = (pitch2_base_keynum - pitch1_base_keynum) % 12
        print("pc span: " + str(keynum_span))
        # if (pitch2.keynum() - pitch1.keynum() < 0):
        #     base_interval = Interval("-" + self._diatonic_intervals[12 - abs(keynum_span)])
        # 1) accomodates the unison case
        # 4) accomodates the octave case
        # 3) accomodates the devil (and others) case
        # 2) accomodates the converse of the devil case
        # 5) sets base interval to the default span
        if (pitch2.keynum() - pitch1.keynum() < 0 and pitch2_base_keynum - pitch1_base_keynum == 0):
            base_interval = Interval("-" + self._diatonic_intervals[0])
            print("in 1")
        elif (pitch2.keynum() - pitch1.keynum() < 0 and pitch1.letter < pitch2.letter):
            base_interval = Interval("-" + self._diatonic_intervals[abs(keynum_span)]).complemented()
            print("in 2")
        elif (pitch2.keynum() - pitch1.keynum() < 0):
            base_interval = Interval("-" + self._diatonic_intervals[12 - abs(keynum_span)])
            print("in 3")
        # elif (pitch2.keynum() - pitch1.keynum() > 0 and pitch1.letter > pitch2.letter):
        #     base_interval = Interval(self._diatonic_intervals[abs(keynum_span)]).complemented()
        #     print("in 4")
        else:
            base_interval = Interval(self._diatonic_intervals[abs(keynum_span)])
            print("in 5")
        print("base interval: " + str(base_interval.string())) 
        # offset from the diatonic intervals given by the pitches' accidentals
        if (pitch2.keynum() - pitch1.keynum() < 0):
            qual_offset = -((pitch2.accidental - 2) - (pitch1.accidental - 2))
        else:
            qual_offset = (pitch2.accidental - 2) - (pitch1.accidental - 2)
        print("qual offset: " + str(qual_offset))
        if ((pitch1.letter == 3 and pitch2.letter == 6) or(pitch1.letter == 6 and pitch2.letter == 3)):
            qual = self._qual_scale_perfect_reverse[self._qual_scale_perfect[base_interval.qual] + qual_offset]
        elif (base_interval.is_perfect()):
            qual = self._qual_scale_perfect_reverse[self._qual_scale_perfect[base_interval.qual] + qual_offset]
        else:
            qual = self._qual_scale_imperfect_reverse[self._qual_scale_imperfect[base_interval.qual] + qual_offset]
        # handles the octave special case for extra octaves (the crossover)
        if (base_interval.span == 7 and abs(pitch2_base_keynum - pitch1_base_keynum) // 12 == 1):
            self._init_from_list(base_interval.span, qual, max((abs(pitch2_base_keynum - pitch1_base_keynum) // 12) - 1, 0), base_interval.sign)
        else:
            self._init_from_list(base_interval.span, qual, max((abs(pitch2_base_keynum - pitch1_base_keynum) // 12), 0), base_interval.sign)
        

    def __str__(self):
        return f'<Interval: {self.string()} {self.to_list()} {hex(id(self))}>'


    def __repr__(self):
        return f'Interval("{self.string()}")'


    def __lt__(self, other):
        if (not isinstance(other, Interval)):
            raise TypeError(f'{type(other)} is not an Interval')
        if (self.pos() < other.pos()):
            return True
        return False


    def __le__(self, other):
        if (not isinstance(other, Interval)):
            raise TypeError(f'{type(other)} is not an Interval')
        if (self.pos() <= other.pos()):
            return True
        return False


    def __eq__(self, other):
        if (not isinstance(other, Interval)):
            raise TypeError(f'{type(other)} is not an Interval')
        if (self.pos() == other.pos()):
            return True
        return False


    def __ne__(self, other):
        if (not isinstance(other, Interval)):
            raise TypeError(f'{type(other)} is not an Interval')
        if (self.pos() != other.pos()):
            return True
        return False


    def __ge__(self, other):
        if (not isinstance(other, Interval)):
            raise TypeError(f'{type(other)} is not an Interval')
        if (self.pos() >= other.pos()):
            return True
        return False


    def __gt__(self, other):
        if (not isinstance(other, Interval)):
            raise TypeError(f'{type(other)} is not an Interval')
        if (self.pos() > other.pos()):
            return True
        return False

  
    def pos(self):
        return (((self.span + (self.xoct * 7)) + 1) << 8) + self.qual


    def string(self):
        if (self.sign == -1):
            return '-' + self._quals[self.qual * 2 + 1] + str(self.span + (7 * self.xoct) + 1)
        else:
            return self._quals[self.qual * 2 + 1] + str(self.span + (7 * self.xoct) + 1)


    def full_name(self, *, sign=True):
        if (sign == True and self.sign == -1):
            return "descending " + self.quality_name() + " " + self.span_name()
        return self.quality_name() + " " + self.span_name()


    def span_name(self):
        return self._span_names[self.span]

    def quality_name(self):
        return self._qual_names[self.qual]


    def matches(self, other):
        if (self.span == other.span and self.qual == other.qual and self.sign == other.sign):
            return True
        return False


    def lines_and_spaces(self):
        return self.span + 1


    def _to_iq(self, name):
        return self._qual_names_reversed[str(name).lower]


    def to_list(self):
        return [self.span, self.qual, self.xoct, self.sign]

    def is_interval(self, span, qual=None):
        if (qual is not None and qual not in ('M','m')):
            qual = str.lower(qual)
        try:
            if (self.span == span and (qual==None or self.qual == (self._quals.index(qual) // 2))):
                return True
        except ValueError:
            raise ValueError(f'invalid quality: {qual}')
        return False

    def is_unison(self, qual=None):
        return self.is_interval(0, qual)


    def is_second(self, qual=None):
        return self.is_interval(1, qual)
    
    def is_third(self, qual=None):
        return self.is_interval(2, qual)


    def is_fourth(self, qual=None):
        return self.is_interval(3, qual)


    def is_fifth(self, qual=None):
        return self.is_interval(4, qual)


    def is_sixth(self, qual=None):
        return self.is_interval(5, qual)


    def is_seventh(self, qual=None):
        return self.is_interval(6, qual)

    
    def is_octave(self, qual=None):
        return self.is_interval(7, qual)


    def is_diminished(self):
        if (self.qual in [i for i in range(0, 5)]):
            return 5 - self.qual
        return False


    def is_minor(self):
        if (self.qual == 5):
            return True
        return False

    
    def is_perfect(self):
        if (self.qual == 6):
            return True
        return False

    
    def is_major(self):
        if (self.qual == 7):
            return True
        return False

    
    def is_augmented(self):
        if (self.qual in [i for i in range(8, 13)]):
            return self.qual - 7
        return False

    
    def is_perfect_type(self):
        if (self.span in (0, 3, 4, 7)):
            return True
        return False

    
    def is_imperfect_type(self):
        return not self.is_perfect()

        
    def is_simple(self):
        if (self.xoct == 0):
            return True
        return False

        
    def is_compound(self):
        return not self.is_simple()

    
    def is_ascending(self):
        return not self.is_descending()

    
    def is_descending(self):
        if (self.sign == -1):
            return True
        return False

    
    def is_consonant(self):
        return not self.is_dissonant()

                   
    def is_dissonant(self):
        if (self.semitones() in (6,1,11,2,10)):
            return True
        return False


    def complemented(self):
        return Interval([(7 - self.span + (7 * self.xoct)), 12 - self.qual, self.xoct, self.sign])

    
    def semitones(self):
        return self._default_spans[self.span] + self._semitones[self.span][self.qual] + (12 * self.xoct)


    def add(self, other):
        if (self.is_descending() or other.is_descending()):
            raise NotImplementedError('adding descending intervals not implemented')
        if (not(isinstance(other, Interval))):
            raise TypeError(f'cannot add a {type(other)} to an interval')
        to_span = self.span + other.span
        target = self.semitones() + other.semitones()
        to_qual = ((self.qual - 6) + (other.qual - 6)) + 6
        to_xoct = self.xoct + other.xoct
        assert (to_qual >= 0)
        print(f'add to_span: {to_span}')
        print(f'add to_qual: {to_qual}')
        print(f'add to_xoct: {to_xoct}')
        out = Interval([to_span, to_qual, to_xoct, 1])
        # fine tune the quality
        if (out.semitones() < target):
            to_qual += target - out.semitones()
        out = Interval([to_span, to_qual, to_xoct, 1])
        assert (out.semitones() == target)
        return out

    def transpose(self, p):
        if (isinstance(p, Pitch.pnums)):
            if (self.is_descending()):
                interval_to_use = self.complemented()
                interval_to_use.sign = 1
                print(interval_to_use)
            else:
                interval_to_use = self
            print(f'Interval to use: {interval_to_use}')
            print(f'Pitch to use: {Pitch(p.name + "4")}')
            return interval_to_use.transpose(Pitch(p.name + '4')).pnum()
        elif (isinstance(p, str)):
            pass
        elif (isinstance(p, Pitch)):
            if (self.is_descending()):
                interval_to_use = self.complemented()
                interval_to_use.sign = 1
                octave_offset = 1
                print(interval_to_use)
            else:
                interval_to_use = self
                octave_offset = 0
            new_letter = p.letter + interval_to_use.span
            print(f'keynum: {p.keynum()}')
            target = p.keynum() + interval_to_use.semitones()
            # accomodates special cases going to/from letters surrounding half steps
            if (new_letter % 7 in (0, 3) and self.is_ascending() and self.is_imperfect_type()):
                target += 1
                print("in 1")
            elif (new_letter % 7 in (6, 2) and self.is_descending() and self.is_imperfect_type()):
                target -= 1
                print("in 2")
            elif (p.letter % 7 == 6 and self.is_ascending() and not (self.is_fourth())):
                target += 1
                print("in 3")
            elif (p.letter % 7 == 3 and self.is_ascending() and self.is_fourth()):
                target -= 1
                print("in 4")
            elif (p.letter % 7 == 3 and self.is_descending() and self.is_perfect_type()):
                target -= 1
                print("in 5")
            elif (p.letter % 7 == 6 and self.is_descending) and (self.is_imperfect_type()):
                target += 1
                print("in 6")
            print(f'target: {target}')
            current = (p.keynum() - (p.accidental - 2)) + self._default_spans[interval_to_use.span]
            print(f'current: {current}')
            accidental = 2 + (target - current)
            print(f'accidental: {accidental}')
            if (accidental < 0 and new_letter in (0, 1, 3, 4, 5)):
                raise ValueError(f'Invalid transposition - 1')
            elif (accidental < 0):
                raise ValueError(f'Invalid transposition - 2')
            elif (accidental > 4 and new_letter in (1, 2, 4, 5, 6)):
                raise ValueError(f'Invalid transposition - 3')
            elif (accidental > 4):
                raise ValueError(f'Invalid transposition - 4')
            assert (accidental >= 0 and accidental < 5)
            xoct = (new_letter) // 7
            print(new_letter)
            return Pitch([(new_letter) % 7, accidental, p.octave + xoct - octave_offset])
        else:
            raise TypeError(f'invalid input {p} with type {type(p)}')



def test():
    # Add your testing code here!
    to_test = Pitch('C##5')
    # for interval in ['-P1', '-m2', '-M2', '-m3', '-M3', '-P4', '-d5', '-P5', '-m6', '-M6', '-m7', '-M7', '-P8']:
        #print(Interval(interval).transpose(to_test))
    
    # print(Interval('+1').is_unison('A'))
    # print(Interval('+1').is_unison('+'))
    # print(Interval('+1').is_unison('o'))
    # print(Interval('+2').is_second('A'))
    # print(Interval('+2').is_second('+'))
    # print(Interval('+2').is_second('m') )
    # print(Interval('+3').is_third('A'))
    # print(Interval('+3').is_third('+'))
    # print(Interval('+3').is_third('++') )
    # print(Interval('+4').is_fourth('A'))
    # print(Interval('+4').is_fourth('+'))
    # print(Interval('+4').is_fourth('oo') )
    # print(Interval('+5').is_fifth('A'))
    # print(Interval('+5').is_fifth('+'))
    # print(Interval('+5').is_fifth('oo') )
    # print(Interval('M6').is_sixth('M'))
    # print(Interval('+6').is_sixth('+'))
    # print(Interval('+6').is_sixth('oo') )
    # print(Interval('m7').is_seventh('m'))
    # print(Interval('+7').is_seventh('+'))
    # print(Interval('+7').is_seventh('oo') )
    # print(Interval('+++14').is_seventh())
    # print(Interval('+8').is_octave('A'))
    # print(Interval('+8').is_octave('+'))
    # print(Interval('+8').is_octave('P') )
    # print(Interval('-m14').is_major() )
    # print(Interval('-m14').is_minor())
    # print(Interval('m9').is_compound())
    # print(Interval('o9').is_compound())
    # print(Interval('oo9').is_compound())
    # print(Interval('ooo9').is_compound())
    # print(Interval('oooo9').is_compound())
    # print(Interval('-m3').is_ascending())
    # print(Interval('-+3').is_descending())
    # print(Interval('+++++4').is_consonant())
    # print(Interval('ooooo5').is_consonant())
    # print(Interval('oo3').is_consonant())
    # print(Interval('+6').is_consonant())
    # print(Interval('+++++4').is_dissonant())
    # print(Interval('ooooo5').is_dissonant())
    # print(Interval('oo3').is_dissonant())
    # print(Interval('+6').is_dissonant())

    # print(Interval('o3').semitones())
    # print(Interval('oo3').semitones())
    # print(Interval('ooo3').semitones())
    # print(Interval('o2').semitones())
    # print(Interval('oooo9').semitones() )
    # print(Interval('ooo9').semitones()  )
    # print(Interval('oo9').semitones() )
    # print(Interval('o9').semitones() )
    # print(Interval('m9').semitones() )
    # print(Interval('M9').semitones() )
    # print(Interval('+9').semitones() )
    # print(Interval('++9').semitones() )
    # print(Interval('+++9').semitones() )
    # print(Interval('++++9').semitones() )

    # print(Interval('P5').full_name()  )
    # print(Interval('++15').full_name()  )
    # print(Interval('P5').span_name()  )
    # print(Interval('++15').span_name()  )
    # print(Interval('P5').quality_name())
    # print(Interval('++15').quality_name())
    # print(Interval('P5').lines_and_spaces())

    # print(Interval([0, 6, 1, 1]).to_list())
    # print(Interval([0, 6, 2, 1]).to_list())

    # print(Interval('P5').is_fifth()  )
    # print(Interval('P5').is_perfect()  )
    # print(Interval('P5').is_imperfect_type()  )
    # print(Interval('AAAA5').is_augmented())
    # print(Interval('P5').is_diminished()  )
    # print(Interval('AAAA5').is_diminished()  )
    # print(Interval('P5').is_augmented()  )
    # print(Interval('P5').is_major()  )
    # print(Interval('P5').is_consonant())
    # print(Interval('P5').is_dissonant() )

    # print(Interval('P1').complemented())
    # print(Interval('+1').complemented())
    # print(Interval('+7').complemented())
    # print(Interval('m2').complemented())
    # print(Interval('m9').complemented() )
    # print(Interval('P8').complemented())
    # print(Interval('++6').complemented()  )
    # print(Interval('o8').complemented())
    # print(Interval('oo8').complemented()  )
    # print(Interval('++15').complemented()  )
    # print(Interval('M3').complemented()  )
    # print(Interval('m73').complemented() )
    # print(Interval('m66').complemented() )
    # print(Interval('++3').complemented()  )
    # print(Interval('oo3').complemented()  )
    # print(Interval('P5').complemented()  )
    # print(Interval('-P5').complemented()  )
    # print(Interval('-M3').complemented()  )
    # print(Interval('-oo5').complemented()   )
    # print(Interval('-ooo5').complemented())
    # print(Interval('-oooo5').complemented()  )
    # print(Interval('-ooooo5').complemented()   )
    # print(Interval('ooooo12').complemented()  )
    # print(Interval('-+++++18').complemented())

    print(Interval(Pitch('D##4'), Pitch('Ebb3')))
    print(Interval(Pitch('E9'), Pitch('C00')))
    print(Interval(Pitch('C##4'), Pitch('Cbb4')))
    print(Interval(Pitch('Bbb4'), Pitch('F##4')))
    print(Interval(Pitch('B##4'), Pitch('Fbb4')))
    print(Interval(Pitch('Cs4'), Pitch('B3')))
    print(Interval(Pitch('E4'), Pitch('D4')))
    print(Interval(Pitch('E4'), Pitch('D#4')))
    print(Interval(Pitch('Cs4'), Pitch('B3')))
    print(Interval(Pitch('Cs4'), Pitch('B2')))
    print(Interval(Pitch('Bb5'), Pitch('Cs4')))
    print(Interval(Pitch('B3'), Pitch('Bb3'))  )
    print(Interval(Pitch('Eb4'), Pitch('D#4')))
    print(Interval(Pitch('B3'), Pitch('Bb3'))  )
    print(Interval(Pitch('Eb4'), Pitch('D#4')))
    print(Interval(Pitch('C#5'), Pitch('C4')))
    print(Interval(Pitch('C##5'), Pitch('C4'))   )
    print(Interval(Pitch('C##5'), Pitch('Cb4'))   )
    print(Interval(Pitch('C##5'), Pitch('Cbb4'))  )
    print(Interval(Pitch('C##5'), Pitch('Cbb3'))  )
    print(Interval(Pitch('F4'), Pitch('B4'))  )
    print(Interval(Pitch('F4'), Pitch('B#4')) )
    print(Interval(Pitch('F4'), Pitch('B##4'))  )
    print(Interval(Pitch('Fb4'), Pitch('B##4'))  )
    print(Interval(Pitch('Fbb4'), Pitch('B##4')) )
    print(Interval(Pitch('B#4'), Pitch('Fbb4'))  )
    print(Interval(Pitch('B4'), Pitch('F5'))  )
    print(Interval(Pitch('B4'), Pitch('Fbb5')) )
    print(Interval(Pitch('B#4'), Pitch('Fbb5'))    )
    print(Interval(Pitch('B##4'), Pitch('Fbb5'))  )
    print(Interval(Pitch('Fbb5'), Pitch('B##4'))  )
    print(Interval(Pitch('C00'), Pitch('Abb9'))  )



if __name__ == '__main__':
    test()