###############################################################################

# You can import from score, theory, and any python system modules you want.
# if it's not a whole note, it's wrong
# only one rest allowed, and it must be in the first position
# raised leading tone and raised 6th has to be at the end in minor

from .score import Note, Pitch, Rest, Interval, Ratio, Key, Mode, import_score
from .theory import Analysis, Rule, timepoints
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
    'At #{}: consecutive unisons',
    'At #{}: consecutive fifths',
    'At #{}: consecutive octaves',
    'At #{}: direct unisons',
    'At #{}: direct fifths',
    'At #{}: direct octaves',
    'At #{}: consecutive unisons in cantus firmus notes',  # if species 2
    'At #{}: consecutive fifths in cantus firmus notes',   # if species 2
    'At #{}: consecutive octaves in cantus firmus notes',  # if species 2
    'At #{}: voice overlap',
    'At #{}: voice crossing',
    'At #{}: forbidden weak beat dissonance',   # vertical dissonance
    'At #{}: forbidden strong beat dissonance',  # vertical dissonance
    'At #{}: too many consecutive parallel intervals',  # parallel vert ints

    # MELODIC RESULTS
    'At #{}: forbidden starting pitch',
    'At #{}: forbidden rest',
    'At #{}: forbidden duration',
    'At #{}: missing melodic cadence',
    'At #{}: forbidden non-diatonic pitch',
    'At #{}: dissonant melodic interval',
    'At #{}: too many melodic unisons',         # 'MAX_UNI' setting
    'At #{}: too many leaps of a fourth',       # 'MAX_4TH' setting
    'At #{}: too many leaps of a fifth',        # 'MAX_5TH' setting
    'At #{}: too many leaps of a sixth',        # 'MAX_6TH' setting
    'At #{}: too many leaps of a seventh',      # 'MAX_7TH' setting
    'At #{}: too many leaps of an octave',      # 'MAX_8VA' setting
    'At #{}: too many large leaps',             # 'MAX_LRG' setting
    'At #{}: too many consecutive leaps',        # 'MAX_CONSEC_LEAP' setting
    'At #{}: too many consecutive intervals in same direction',
    'At #{}: missing reverse by step recovery',  # 'STEP_THRESHOLD' setting
    'At #{}: forbidden compound melodic interval',
    ]


# Rules
SETUP_WARNING = "Setup has not been run yet!"
MELODY_ERROR = "Voice is not a melody!"


class MelodicNoteChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "My very first rule.")
        # TODO - add other instance vars
        if (self.analysis.tps is self.analysis.cp_voice
           is self.analysis.trns is self.analysis.key is None):
            raise AttributeError(SETUP_WARNING)
        self.pitches = []
        self.indices = []
        for tp in self.analysis.tps:
            current_tp = tp.nmap[self.analysis.cp_voice]
            assert (isinstance(current_tp, Note)), MELODY_ERROR
            self.pitches.append(current_tp.pitch)
            self.indices.append(tp.index)

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # might need to fix this later to accomodate the "above the cf" case
    def check_start_pitch(self):
        if (isinstance(self.analysis.tps[0].nmap[self.analysis.cf_voice], Note)
                and self.pitches[0].pnum() in {self.analysis.key.scale()[0],
                                               self.analysis.key.scale()[4]}):
            return True
        if self.pitches[0].pnum() == self.analysis.key.scale()[0]:
            return True
        return False

    # TODO
    def check_rests(self):
        pass

    # TODO
    def check_durations(self):
        pass

    # TODO
    def check_mel_cadence(self):
        pass

    # TODO
    def check_diatonic(self):
        pass

    # TODO
    def display(self, index):
        print('--------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


class MelodicIntChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "My very first rule.")

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # TODO
    def check_num_int(self, inter, num):
        pass

    # TODO
    def check_consec_leap(self, num):
        pass

    # TODO
    def check_consec_int_samedir(self, num):
        pass

    # TODO
    def check_int_reverse(self, threshold):
        pass

    # TODO
    def display(self, index):
        print('--------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


class HarmonicStaticIntChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "My very first rule.")

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # TODO
    def check_voice_overlap(self):
        pass

    # TODO
    def check_voice_cross(self):
        pass

    # TODO
    def check_dis_int(self, strong=True):
        pass

    # TODO
    def display(self, index):
        print('--------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


class HarmonicMovingIntChecks(Rule):

    def __init__(self, analysis):
        super().__init__(analysis, "My very first rule.")

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # TODO
    def check_consec_ints(self):
        pass

    # TODO
    def check_direct_ints(self):
        pass

    # TODO
    def check_consec_parallel(self):
        pass

    # TODO
    def display(self, index):
        print('--------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


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
            raise ValueError(f"'{species}' is not a valid species number 1 or 2.")
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

    # Use this function to perform whatever setup actions your rules require.
    def setup(self, args, kwargs):
        self.key = self.score.metadata['main_key']
        if (self.key == Key(0, Mode.MAJOR) or self.key == Key(-1, Mode.MINOR)):
            self.cp_voice = 'P1.1'
            self.cf_voice = 'P2.1'
        elif (self.key == Key(-3, Mode.MAJOR)
              or self.key == Key(0, Mode.MINOR)):
            self.cp_voice = 'P2.1'
            self.cf_voice = 'P1.1'
        self.timepoints = timepoints(self.score, measures=False,
                                     trace=False)
        self.rules = []
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


samples1 = ['1-018-C_ajyanez2.musicxml', '1-019-A_ajyanez2.musicxml',
            '1-005-A_hanzhiy2.musicxml', '1-008-C_davidx2.musicxml',
            '1-030_C_chchang6.musicxml', '1-011-B_weikeng2.musicxml',
            '1-037-A_sz18.musicxml', '1-012-B_erf3.musicxml',
            '1-030-C_cjrosas2.musicxml']

samples2 = ['2-034-A_zawang2.musicxml', '2-028-C_hanzhiy2.musicxml',
            '2-000-B_sz18.musicxml', '2-003-A_cjrosas2.musicxml',
            '2-021-B_erf3.musicxml', '2-003_A_chchang6.musicxml',
            '2-009-C_mamn2.musicxml', '2-010-B_mamn2.musicxml',
            '2-034-C_zawang2.musicxml', '2-029-A_hanzhiy2.musicxml',
            '2-009-B_mamn2.musicxml', '2-021-C_erf3.musicxml']

if __name__ == '__main__':
    import os
    DIREC = os.path.dirname(__file__)
    for name in samples1:
        s = import_score(f'{DIREC}/Species/{name}')
        a = SpeciesAnalysis(s, 1)
        a.submit_to_grading()
