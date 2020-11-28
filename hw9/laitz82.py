###############################################################################

## You can import from score, theory and any python module you want to use.

from .score import Pitch, Interval, Mode, import_score, Key
from .theory import Analysis, Rule, TimePoint, timepoints, Transition
from copy import copy
import math

melodic_checks = {
    # Pitch checks
    'MEL_START_NOTE': None,
    'MEL_CADENCE': None,
    'MEL_TESSITURA': None,
    'MEL_DIATONIC': None,
    # Melodic interval checks
    'INT_STEPWISE': None,
    'INT_CONSONANT': None,
    'INT_SIMPLE': None,
    'INT_NUM_LARGE': None,
    'INT_NUM_UNISON': None,
    'INT_NUM_SAMEDIR': None,
    # Leap checks
    'LEAP_RECOVERY': None,  
    'LEAP_NUM_CONSEC': None,
    # Shape checks
    'SHAPE_NUM_CLIMAX': None,
    'SHAPE_ARCHLIKE': None,
    'SHAPE_UNIQUE': None
}

# ------------------Rules------------------ #
class pitchChecks(Rule):

    def __init__(self, analysis):
        if (self.tps == self.melodic_id == self.trns == self.key == None):
            # TODO - fix AttributeErrors
            raise AttributeError("Setup has not been run yet!")
        # TODO - fix titles
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        self.pitches = []
        for tp in self.tps:
            assert (type(tp[self.melodic_id]) == Pitch), "Voice is not a melodic line!"
            self.pitches.append(tp[self.melodic_id])

    def apply(self):
        self.analysis.results['MEL_START_NOTE'] = True if self.check_start_note() else []
        self.analysis.results['MEL_CADENCE'] = True if self.check_mel_cadence() else []
        self.analysis.results['MEL_TESSITURA'] = True if self.check_mel_tessitura(Interval('M6')) else []
        self.analysis.results['MEL_DIATONIC'] = True if self.check_mel_diatonic() == [] else self.check_mel_diatonic()

    # MEL_START_NOTE
    def check_start_note(self):
        if (self.pitches[0].pnum() in {self.key.scale()[0], self.key.scale()[2], self.key.scale()[4]}):
            return True
        return False

    # MEL_CADENCE
    def check_mel_cadence(self):
        last_2_melody = (self.pitches[-2].pnum(), self.pitches[-1].pnum())
        scale_2_1 = (self.key.scale()[1], self.key.scale()[0])
        scale_7_1 = (self.key.scale()[6], self.key.scale()[0])
        if (last_2_melody == scale_2_1 or last_2_melody == scale_7_1):
            return True
        return False

    # MEL_TESSITURA
    def check_mel_tessitura(self, center_inter):
        max_midi = max(self.pitches).keynum()
        min_midi = min(self.pitches).keynum()
        median = (max_midi + min_midi) // 2
        low = center_inter.semitones() // 2
        high = center_inter.semitones() - low
        span_min = math.max(median - low, min_midi)
        span_max = math.min(median + high, max_midi)
        count = sum(x.keynum() in range(span_min, span_max + 1) for x in self.pitches)
        if (count / len(self.pitches) >= 0.75):
            return True
        return False

    # MEL_DIATONIC
    def check_mel_diatonic(self):
        out = []
        for i,p in enumerate(self.pitches):
            if (p.pnum() not in self.key.scale()):
                # note positions start on 1 NOT 0
                out.append(i + 1)
        return out

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")


class intervalChecks(Rule):

    def __init__(self, analysis):
        if (self.tps == self.melodic_id == self.trns == self.key == None):
            raise AttributeError("Setup has not been run yet!")
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.

    def apply(self):
        # TODO - apply rule
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # TODO - int_stepwise
    # TODO - int_consonant
    # TODO - INT_SIMPLE
    # TODO - IMT_NUM_LARGE
    # TODO - INT NUM UNISON
    # TODO - INT NUM SAMEDIR


    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print("I'm here!")


class leapChecks(Rule):

    def __init__(self, analysis):
        if (self.tps == self.melodic_id == self.trns == self.key == None):
            raise AttributeError("Setup has not been run yet!")
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.

    def apply(self):
        # TODO - apply rule
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # TODO - LEAP RECOVERY
    # TODO - LEAP NUMCONSEC

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print("I'm here!")


class shapeChecks(Rule):

    def __init__(self, analysis):
        if (self.tps == self.melodic_id == self.trns == self.key == None):
            raise AttributeError("Setup has not been run yet!")
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.
        self.notes = self.score.getPart()

    def apply(self):
        # TODO - apply rule
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # TODO - SHAPE NUM CLIMAX
    # TODO - SHAPE ARCHLIKE
    # TODO - SHAPE UNIQUE

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print("I'm here!")


class MyMelodicAnalysis(Analysis):
    def __init__(self, score):
        super().__init__(score)
        self.results = copy(melodic_checks)
        self.rules = [
            pitchChecks(self),
            intervalChecks(self),
            leapChecks(self),
            shapeChecks(self)]
        self.melodic_id = None
        self.tps = None
        self.trns = None
        self.key = None

    # def cleanup(self):
    #     self.melody, self.intervals, self.motions = [], [], []

    def setup(self, args, kwargs):
        assert len(args) == 1, "Usage: analyze(<pvid>), pass the pvid of the voice to analyze."
        self.melodic_id = args[0]
        self.tps = timepoints(self.score, span=True, measures=False, trace=True)
        self.trns = [Transition(a, b) for a,b in zip(self.tps, self.tps[1])]
        # set the key to the main_key in the metadata of the score. Else, set
        # the key to the key of the first bar in the score
        try:
            self.key = self.score.metadata['main_key']
        except KeyError:
            self.key = self.score.get_part('P' + args[0]).staffs[int(args[0][-1:]) - 1].key
            assert (type(self.key) == Key), "Could not get key from input. Cannot continue analysis."
        except Exception:
            self.key = Key(0, Mode.MAJOR)
            print('Setting key to C major; no valid key could be extracted from the score.')

    # can also use this function as a top-level call for testing
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results

