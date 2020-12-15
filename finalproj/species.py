###############################################################################

# autograding:
# autograder starts saturday or sunday
# autograder will run for a few days
# autograder will run for earlier projects

# You can import from score, theory, and any python system modules you want.
# if it's not a whole note, it's wrong
# only one rest allowed, and it must be in the first position
# raised leading tone and raised 6th has to be at the end in minor

from .score import Note, Pitch, Rest, Interval, Ratio, Key, Mode, import_score
from .theory import Analysis, Rule, timepoints, Transition
from copy import copy
from math import inf

# Settings for a species 1 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a species 1 score. See also: SpeciesAnalysis.
s1_settings = {
    # section 1: melodic tests
    # Maximum number of melodic unisons allowed.
    'MAX_UNI': 1,
    # Maximum number of melodic 4ths allowed.
    'MAX_4TH': 2,
    # Maximum number of melodic 5ths allowed.
    'MAX_5TH': 1,
    # Maximum number of melodic 6ths allowed.
    'MAX_6TH': 0,
    # Maximum number of melodic 7ths allowed.
    'MAX_7TH': 0,
    # Maximum number of melodic 8vas allowed.
    'MAX_8VA': 0,
    # Maximum number of leaps larger than a 3rd.
    'MAX_LRG': 2,
    # Maximum number of consecutive melodic intervals
    # moving in same direction.
    'MAX_SAMEDIR': 3,

    # section 2: harmonic tests
    # Maximum number of parallel consecutive harmonic 3rds/6ths.
    'MAX_PARALLEL': 3,

    # section 3: leap tests
    # Maximum number of consecutive leaps of any type.
    'MAX_CONSEC_LEAP': 2,
    # Smallest leap demanding recovery step in opposite direction.
    'STEP_THRESHOLD': 5,

    # section 4: pitch checks
    # List of allowed starting scale degrees of a CP that is above the CF.
    'START_ABOVE': [1, 5],
    # List of allowed starting scale degrees of a CP that is below the CF.
    'START_BELOW': [1],
    # List of allowed melodic cadence patterns for the CP.
    'CADENCE_PATTERNS': [[2, 1], [7, 1]]
}

# Settings for species 2 analysis. Pass this to SpeciesAnalysis() if you
# are analyzing a second species score. See also: SpeciesAnalysis.
s2_settings = copy(s1_settings)
s2_settings['START_ABOVE'] = [1, 3, 5]
s2_settings['MAX_4TH'] = inf  # no limit on melodic fourths
s2_settings['MAX_5TH'] = inf  # no limit on melodic fifths
s2_settings['MAX_UNI'] = 0    # no melodic unisons allowed

# A list of all the possible result strings your analysis can generate.
# The {} marker in each string will always receive the 1-based integer index
# of the left-side time point that contains the offending issue. For example,
# if the first timepoint (e.g. self.timepoints[0]) contained an illegal
# starting pitch the message would be: 'At 1: forbidden starting pitch'
# Note: the variable result_strings does not need to be used by your code,
# it simply contains the list of all the result strings ;)
result_strings = [
    # VERTICAL RESULTS
    'At #{0}: consecutive unisons',             # DONE
    'At #{0}: consecutive fifths',              # DONE
    'At #{0}: consecutive octaves',             # DONE
    'At #{0}: direct unisons',                  # DONE
    'At #{0}: direct fifths',                   # DONE
    'At #{0}: direct octaves',                  # DONE
    'At #{0}: consecutive unisons in cantus firmus notes',  # if species 2
    'At #{0}: consecutive fifths in cantus firmus notes',   # if species 2
    'At #{0}: consecutive octaves in cantus firmus notes',  # if species 2
    'At #{0}: voice overlap',                   # DONE
    'At #{0}: voice crossing',                  # DONE
    'At #{0}: forbidden weak beat dissonance',   # if species 2 vertical dissonance
    'At #{0}: forbidden strong beat dissonance',  # DONE vertical dissonance
    'At #{0}: too many consecutive parallel intervals',  # DONE parallel vert ints

    # MELODIC RESULTS
    'At #{0}: forbidden starting pitch',        # DONE
    'At #{0}: forbidden rest',                  # DONE
    'At #{0}: forbidden duration',              # DONE
    'At #{0}: missing melodic cadence',         # DONE
    'At #{0}: forbidden non-diatonic pitch',    # DONE
    'At #{0}: dissonant melodic interval',      # DONE
    'At #{0}: too many melodic unisons',         # DONE 'MAX_UNI' setting
    'At #{0}: too many leaps of a fourth',       # DONE 'MAX_4TH' setting
    'At #{0}: too many leaps of a fifth',        # DONE 'MAX_5TH' setting
    'At #{0}: too many leaps of a sixth',        # DONE 'MAX_6TH' setting
    'At #{0}: too many leaps of a seventh',      # DONE 'MAX_7TH' setting
    'At #{0}: too many leaps of an octave',      # DONE 'MAX_8VA' setting
    'At #{0}: too many large leaps',             # DONE 'MAX_LRG' setting
    'At #{0}: too many consecutive leaps',        # DONE 'MAX_CONSEC_LEAP' setting
    'At #{0}: too many consecutive intervals in same direction', # DONE
    'At #{0}: missing reverse by step recovery',  # DONE 'STEP_THRESHOLD' setting
    'At #{0}: forbidden compound melodic interval', # TODO
    ]


# My own stupid implementation of the Transition class
class MyTransition(Transition):

    def __init__(self, from_tp, to_tp):
        self.from_tp = from_tp
        self.to_tp = to_tp


# Rules
MELODY_ERROR = "Voice is not a melody!"


class MelodicNoteChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "Check the notes of the melody \
            for compliance with father Laitz's unbreakable and \
                indisputable laws of the construction of objectively \
                    perfect music")
        self.pitches = []
        self.indices = []
        for tp in self.analysis.tps:
            current_tp = tp.nmap[self.analysis.cp_voice]
            self.pitches.append(current_tp.pitch)
            self.indices.append(tp.index + 1)

    def apply(self):
        tests = {
            14: self.check_start_pitch(s1_settings),
            15: self.check_rests(),
            16: self.check_durations(),
            17: self.check_mel_cadence(s1_settings),
            18: self.check_diatonic()
        }
        if not tests[14]:
            self.analysis.results.append(result_strings[14].format('1'))
        for key in list(tests.keys())[1:]:
            if tests[key] != []:
                for note in tests[key]:
                    self.analysis.results.append(result_strings[key].format(note))

    def check_start_pitch(self, sets):
        if self.analysis.cp_voice == 'P1.1':
            pits = [self.analysis.key.scale()[i - 1] for i in sets['START_ABOVE']]
        else:
            pits = [self.analysis.key.scale()[i - 1] for i in sets['START_BELOW']]
        if self.pitches[0].pnum() in pits:
            return True
        return False

    def check_rests(self):
        out = []
        for timepoint in self.analysis.tps:
            current_tp = timepoint.nmap[self.analysis.cp_voice]
            if isinstance(current_tp, Rest):
                out.append(timepoint.index + 1)
        return out

    def check_durations(self):
        out = []
        for timepoint in self.analysis.tps:
            current_tp = timepoint.nmap[self.analysis.cp_voice]
            if current_tp.dur != Ratio('1/1'):
                out.append(timepoint.index + 1)
        return out

    def check_mel_cadence(self, sets):
        out = []
        final_int = Interval(self.pitches[-2], self.pitches[-1])
        if self.analysis.key.mode == Mode.MINOR:
            nat_minor = self.analysis.key.scale()
            mel_minor = nat_minor[:-2]
            for p in nat_minor[-2:]:
                let = p.value >> 4
                acc = p.value - (let << 4)
                to_append = Pitch([let, acc + 1, 4])
                mel_minor.append(to_append.pnum())
            try:
                if final_int.is_ascending():
                    cadence = [mel_minor.index(p.pnum()) + 1 for p in self.pitches[-2:]]
                else:
                    cadence = [nat_minor.index(p.pnum()) + 1 for p in self.pitches[-2:]]
            except ValueError:
                out.append(self.indices[-2] + 1)
        else:
            scale = self.analysis.key.scale()
            try:
                cadence = [scale.index(p.pnum()) + 1 for p in self.pitches[-2:]]
                print(cadence)
            except ValueError:
                out.append(self.indices[-2] + 1)
                return out
            if not (cadence in sets['CADENCE_PATTERNS'] and self.check_diatonic() == []):
                out.append(self.indices[-2] + 1)
        return out

    def check_diatonic(self):
        out = []
        if self.analysis.key.mode == Mode.MINOR:
            nat_minor = self.analysis.key.scale()
            mel_minor = nat_minor[:-2]
            for p in nat_minor[-2:]:
                let = p.value >> 4
                acc = p.value - (let << 4)
                to_append = Pitch([let, acc + 1, 4])
                mel_minor.append(to_append.pnum())
            for i, p in enumerate(self.pitches[:-2]):
                if (p.pnum() not in nat_minor):
                    out.append(self.indices[i] + 1)
            for i, p in enumerate(self.pitches[-2:]):
                if (p.pnum() not in mel_minor):
                    out.append(self.indices[i] + 1)
            # for num, tran in enumerate(self.analysis.trns):
            #     from_note = tran.from_tp.nmap[self.analysis.cp_voice].pitch
            #     to_note = tran.to_tp.nmap[self.analysis.cp_voice].pitch
            #     # print(from_note.pnum(), ' ', from_note.pnum() in nat_minor, ' ', from_note.pnum() in mel_minor)
            #     if ((Interval(from_note, to_note).is_ascending()
            #          and (from_note.pnum() not in mel_minor)
            #          and (not Interval(from_note, to_note).is_unison()))
            #             or (Interval(from_note, to_note).is_descending()
            #                 and (from_note.pnum() not in nat_minor))):
            #         out.append(tran.from_tp.index + 1)
            # # handle the last note
            # tran = self.analysis.trns[-1]
            # to_note = tran.to_tp.nmap[self.analysis.cp_voice].pitch
            # if to_note.pnum() not in mel_minor:
            #     out.append(tran.to_tp.index + 1)
        else:
            for i, p in enumerate(self.pitches):
                if (p.pnum() not in self.analysis.key.scale()):
                    out.append(self.indices[i] + 1)
        return out


class MelodicIntChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "Check the intervals of the melody \
            for compliance with father Laitz's unbreakable and \
                indisputable laws of the construction of objectively \
                    perfect music")
        self.intervals = []
        self.indices = [i.index for i in self.analysis.tps]
        for t in self.analysis.trns:
            from_note = t.from_tp.nmap[self.analysis.cp_voice]
            to_note = t.to_tp.nmap[self.analysis.cp_voice]
            assert (type(from_note) == type(to_note) == Note), MELODY_ERROR
            self.intervals.append(Interval(from_note.pitch, to_note.pitch))
            # the indices of the first note in each interval
            self.indices.append(t.from_tp.index + 1)

    def apply(self):
        tests = {
            19: self.check_mel_consonant(0),
            20: self.check_num_int('is_unison', s1_settings['MAX_UNI']),
            21: self.check_num_int('is_fourth', s1_settings['MAX_4TH']),
            22: self.check_num_int('is_fifth', s1_settings['MAX_5TH']),
            23: self.check_num_int('is_sixth', s1_settings['MAX_6TH']),
            24: self.check_num_int('is_seventh', s1_settings['MAX_7TH']),
            25: self.check_num_int('is_octave', s1_settings['MAX_8VA']),
            26: self.check_num_int('is_octave', s1_settings['MAX_LRG']),
            27: self.check_consec_leap(4, s1_settings['MAX_CONSEC_LEAP']),
            28: self.check_consec_int_samedir(3),
            29: self.check_int_reverse(s1_settings['STEP_THRESHOLD'])
        }
        for key in tests:
            if tests[key] != []:
                for note in tests[key]:
                    self.analysis.results.append(result_strings[key].format(note))

    def check_mel_consonant(self, num):
        out = []
        count = 0
        for i, inter in enumerate(self.intervals):
            if not (inter.is_consonant()
                    or (inter.semitones() <= 2 and inter.is_second())):
                count += 1
                if count > num:
                    out.append(self.indices[i] + 1)
        return out

    def check_num_int(self, attr, num):
        out = []
        count = 0
        for i, inter in enumerate(self.intervals):
            fct = getattr(inter, str(attr))
            if fct():
                count += 1
                if count > num:
                    out.append(self.indices[i] + 1)
        return out

    def check_num_large(self, size, num):
        out = []
        count = 0
        for i, inter in enumerate(self.intervals):
            if inter.lines_and_spaces() > size:
                count += 1
                if count > num:
                    out.append(self.indices[i] + 1)

    def check_consec_leap(self, size, num):
        out = []
        count = 0
        last = self.intervals[0]
        for trans, inter in zip(self.analysis.trns[1:], self.intervals[1:]):
            if last.lines_and_spaces() > size and inter.lines_and_spaces() > size:
                count += 1
            else:
                count = 0
            if count >= num:
                out.append(trans.from_tp.index + 1)
            last = inter
        return out

    def check_consec_int_samedir(self, num):
        out = []
        count = 0
        last = self.intervals[0]
        for trans, inter in zip(self.analysis.trns[1:], self.intervals[1:]):
            check = ((last.is_ascending() and inter.is_descending())
                     or (last.is_descending() and inter.is_descending()))
            if check and (last.lines_and_spaces() == inter.lines_and_spaces()):
                count += 1
            else:
                count = 0
            if count >= num:
                out.append(trans.from_tp.index + 1)
            last = inter
        return out

    def check_int_reverse(self, threshold):
        out = []
        last = self.intervals[0]
        for trans, inter in zip(self.analysis.trns[1:], self.intervals[1:]):
            check1 = (last.lines_and_spaces() >= threshold and last.is_ascending()
                      and inter.lines_and_spaces() == 2 and inter.is_descending())
            check2 = (last.lines_and_spaces() >= threshold and last.is_descending()
                      and inter.lines_and_spaces() == 2 and inter.is_ascending())
            if not (last.lines_and_spaces() < threshold or check1 or check2):
                out.append(trans.from_tp.index + 1)
            last = inter
        return out


class HarmonicStaticIntChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "Check the static intervals between the cp/cf \
            for compliance with father Laitz's unbreakable and \
                indisputable laws of the construction of objectively \
                    perfect music")

    def apply(self):
        tests = {
            9: self.check_voice_cross(),
            10: self.check_voice_cross(overlap=False),
            12: self.check_dis_int()
        }
        for key in tests:
            if tests[key] != []:
                for note in tests[key]:
                    self.analysis.results.append(result_strings[key].format(note))

    def check_voice_cross(self, overlap=True):
        out = []
        for timepoint in self.analysis.tps:
            upper_note = timepoint.nmap['P1.1'].pitch.keynum()
            lower_note = timepoint.nmap['P2.1'].pitch.keynum()
            if overlap:
                check = getattr(lower_note, '__eq__')
            else:
                check = getattr(lower_note, '__gt__')
            if check(upper_note):
                out.append(timepoint.index + 1)
        return out

    def check_dis_int(self, strong=True):
        consonant_ints = [
            Interval('P8'),
            Interval('M6'),
            Interval('m6'),
            Interval('P5'),
            Interval('M3'),
            Interval('m3'),
            Interval('P1')
        ]
        out = []
        for timepoint in self.analysis.tps:
            upper_note = timepoint.nmap['P1.1'].pitch
            lower_note = timepoint.nmap['P2.1'].pitch
            current_inter = Interval(lower_note, upper_note)
            current_inter.sign = abs(current_inter.sign)
            # print(timepoint.index, " :vertical interval: ", current_inter.string(), " ", lower_note, " ", upper_note)
            if (((timepoint.beat != Ratio(0)) ^ strong)
                    and all(not current_inter.matches(i) for i in consonant_ints)):
                out.append(timepoint.index + 1)
        return out



class HarmonicMovingIntChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "Check the moving intervals between the cp/cf \
            for compliance with father Laitz's unbreakable and \
                indisputable laws of the construction of objectively \
                    perfect music")
        self.intervals = []
        self.indices = [i.index for i in self.analysis.tps]
        for t in self.analysis.trns:
            cp_note = t.from_tp.nmap[self.analysis.cp_voice]
            cf_note = t.to_tp.nmap[self.analysis.cf_voice]
            if self.analysis.cp_voice == 'P1.1':
                self.intervals.append(Interval(cf_note.pitch, cp_note.pitch))
            else:
                self.intervals.append(Interval(cp_note.pitch, cf_note.pitch))
            # the indices of the first note in each interval
            self.indices.append(t.from_tp.index + 1)

    def apply(self):
        tests = {
            0: self.check_consec_ints('is_unison'),
            1: self.check_consec_ints('is_fifth'),
            2: self.check_consec_ints('is_octave'),
            # 3: self.check_direct_ints('is_unison'),
            4: self.check_direct_ints('is_fifth'),
            5: self.check_direct_ints('is_octave'),
            13: self.check_consec_parallel(s1_settings['MAX_PARALLEL'])
        }
        for key in tests:
            if tests[key] != []:
                for note in tests[key]:
                    self.analysis.results.append(result_strings[key].format(note))

    def check_consec_ints(self, attr):
        out = []
        last = self.intervals[0]
        for trans, inter in zip(self.analysis.trns[1:], self.intervals[1:]):
            fct1 = getattr(last, str(attr))
            fct2 = getattr(inter, str(attr))
            if fct1() and fct2():
                out.append(trans.from_tp.index + 1)
            last = inter
        return out

    # if there is SIMILAR motion (not parallel or contrary) and
    # the soprano moves by skip or leap all to a certain interval
    def check_direct_ints(self, attr):
        out = []
        for tran in self.analysis.trns:
            upper_from_note = tran.from_tp.nmap['P1.1'].pitch
            upper_to_note = tran.to_tp.nmap['P1.1'].pitch
            lower_to_note = tran.to_tp.nmap['P2.1'].pitch
            sop_int = Interval(upper_from_note, upper_to_note)
            to_int = Interval(lower_to_note, upper_to_note)
            check = getattr(to_int, attr)
            # print(upper_to_note)
            # print(lower_to_note)
            # print(tran.from_tp.index, " ", to_int.string())
            if (HarmonicMovingIntChecks.check_motion_type(tran) == 'SIM'
                    and sop_int.lines_and_spaces() > 3
                    and check()):
                out.append(tran.from_tp.index + 1)
        return out

    def check_consec_parallel(self, num):
        out = []
        count = 0
        for tran in self.analysis.trns:
            # print(HarmonicMovingIntChecks.check_motion_type(tran))
            if HarmonicMovingIntChecks.check_motion_type(tran) == 'PAR':
                count += 1
            else:
                count = 0
            if count >= num:
                out.append(tran.from_tp.index + 1)
        return out

    @staticmethod
    def check_motion_type(trans):
        """a helper function to check the motion type of two voices
        from the given transition object"""
        # 1. contrary (CON)
            # different directions
        # 2. parallel (PAR)
            # same direction same intervals
        # 3. similar (SIM)
            # same direction different intervals
        # 4. oblique (OBL)
            # one voice stationary, other moves
        upper_left = trans.from_tp.nmap['P1.1']
        upper_right = trans.to_tp.nmap['P1.1']
        upper_int = Interval(upper_left.pitch, upper_right.pitch)
        lower_left = trans.from_tp.nmap['P2.1']
        lower_right = trans.to_tp.nmap['P2.1']
        lower_int = Interval(lower_left.pitch, lower_right.pitch)
        # print(trans.from_tp.index, " :UPPER_INT: ", upper_int)
        # print(trans.from_tp.index, " :LOWER_INT: ", lower_int)
        if ((lower_left.pitch == lower_right.pitch)
                ^ (upper_left.pitch == upper_right.pitch)):
            return 'OBL'
        if ((upper_int.is_ascending() and lower_int.is_ascending())
                ^ (upper_int.is_descending() and lower_int.is_descending())):
            if upper_int != lower_int:
                return 'SIM'
            return 'PAR'
        return 'CON'


# A class that implements a species counterpoint analysis of a given score.
# A SpeciesAnalysis has at least 5 attributes, you will very likely add more:
#
# * self.score  The score being analyzed.
# * self.species  The integer species number of the analysis, either 1 or 2.
# * self.settings  A settings dict for the analysis, either s1_settings or
# s2_settings.
# * self.rules  An ordered list of Rules that constitute your analysis.
# * self.results  A list of strings (see below) that constitute your analysis
# findings.
#
# You should call your analysis like this:
#
#   score = import_score(species1_xmlfile)
#   analysis = SpeciesAnalysis(score, 1, s1_settings)
#   analysis.submit_to_grading()
class SpeciesAnalysis(Analysis):
    # Initializes a species analysis.
    # @param score A score containing a two-part species composition.
    # @param species A counterpoint species number, either 1 or 2.
    def __init__(self, score, species):
        # Call the superclass and give it the score.
        super().__init__(score)
        if species not in [1, 2]:
            raise ValueError(f"'{species}' is not a valid species number.")
        # The integer species number for the analysis.
        self.species = species
        # A local copy of the analysis settings.
        self.settings = copy(s1_settings) if species == 1 else copy(s2_settings)
        # A list of strings that represent the findings of your analysis.
        self.results = []
        self.cp_voice = None
        self.cf_voice = None
        self.key = None
        self.timepoints = None
        self.rules = None
        self.tps = None
        self.trns = None

    # Use this function to perform whatever setup actions your rules require.
    def setup(self, args, kwargs):
        self.key = self.score.metadata['main_key']
        if ((self.key.string() == Key(0, Mode.MAJOR).string())
                or (self.key.string() == Key(-1, Mode.MINOR).string())):
            self.cp_voice = 'P1.1'
            self.cf_voice = 'P2.1'
        elif ((self.key.string() == Key(-3, Mode.MAJOR).string())
              or (self.key.string() == Key(0, Mode.MINOR).string())):
            self.cp_voice = 'P2.1'
            self.cf_voice = 'P1.1'
        self.tps = timepoints(self.score, measures=False,
                              trace=False)
        self.trns = [MyTransition(a, b) for a, b in zip(self.tps, self.tps[1:])]
        self.rules = [MelodicNoteChecks(self),
                      MelodicIntChecks(self),
                      HarmonicStaticIntChecks(self),
                      HarmonicMovingIntChecks(self)]
    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed.
    
    def submit_to_grading(self):
        self.analyze()
        # When you return your results to the autograder make sure you convert
        # it to a Python set, like this:
        return set(self.results)

###############################################################################


samples1 = [
    '1-001-B_zawang2.musicxml',
    '1-001-C_zawang2.musicxml',
    '1-005-A_hanzhiy2.musicxml',
    '1-005-D_hanzhiy2.musicxml',
    '1-006-B_hanzhiy2.musicxml',
    '1-006-C_hanzhiy2.musicxml',
    '1-007-B_davidx2.musicxml',
    '1-007-C_davidx2.musicxml',
    '1-008-B_davidx2.musicxml',
    '1-008-C_davidx2.musicxml',
    '1-010-B_weikeng2.musicxml',
    '1-010-C_weikeng2.musicxml',
    '1-011-B_weikeng2.musicxml',
    '1-011-C_weikeng2.musicxml',
    '1-012-B_erf3.musicxml',
    '1-012-C_erf3.musicxml',
    '1-013-B_erf3.musicxml',
    '1-013-C_erf3.musicxml',
    '1-018-B_ajyanez2.musicxml',
    '1-018-C_ajyanez2.musicxml',
    '1-019-A_ajyanez2.musicxml',
    '1-019-D_ajyanez2.musicxml',
    '1-022-B_mamn2.musicxml',
    '1-022-C_mamn2.musicxml',
    '1-030_B_chchang6.musicxml',
    '1-030_C_chchang6.musicxml',
    '1-030-B_cjrosas2.musicxml',
    '1-030-C_cjrosas2.musicxml',
    '1-031_B_chchang6.musicxml',
    '1-031_C_chchang6.musicxml',
    '1-031-B_cjrosas2.musicxml',
    '1-031-C_cjrosas2.musicxml',
    '1-034-A_caleqw2.musicxml',
    '1-034-B_caleqw2.musicxml',
    '1-034-C_caleqw2.musicxml',
    '1-035-B_caleqw2.musicxml',
    '1-035-C_caleqw2.musicxml',
    '1-036-B_sz18.musicxml',
    '1-036-C_sz18.musicxml',
    '1-037-A_sz18.musicxml',
    '1-037-D_sz18.musicxml'
]

samples2 = ['2-034-A_zawang2.musicxml', '2-028-C_hanzhiy2.musicxml',
            '2-000-B_sz18.musicxml', '2-003-A_cjrosas2.musicxml',
            '2-021-B_erf3.musicxml', '2-003_A_chchang6.musicxml',
            '2-009-C_mamn2.musicxml', '2-010-B_mamn2.musicxml',
            '2-034-C_zawang2.musicxml', '2-029-A_hanzhiy2.musicxml',
            '2-009-B_mamn2.musicxml', '2-021-C_erf3.musicxml']

if __name__ == '__main__':
    import os
    DIREC = os.path.dirname(__file__)
    for name in samples1[2:3]:
        f_name = f'{DIREC}/Species/{name}'
        # os.system('open "' + f_name + '"')
        s = import_score(f_name)
        print(name)
        a = SpeciesAnalysis(s, 1)
        print(a.submit_to_grading())
