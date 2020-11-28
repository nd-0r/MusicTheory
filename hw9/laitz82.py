###############################################################################

## You can import from score, theory and any python module you want to use.

from .score import Pitch, Interval, Mode, import_score, Key
from .theory import Analysis, Rule, TimePoint, timepoints
from copy import copy

# A template directory that is copied into your analysis.
# Consult the documentation for more information.

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
            raise AttributeError("Setup has not been run yet!")
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.
        self.pitches = []
        for tp in self.tps:
            assert (type(tp[self.melodic_id]) == Pitch), "Voice is not a melodic line!"
            self.pitches.append(tp[self.melodic_id])

    def apply(self):
        # TODO - apply rule
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    # MEL_START_NOTE
    def check_start_note(self):
        if (self.pitches[0].pnum in {self.key.scale()[0], self.key.scale()[2], self.key.scale()[4]}):
            return True
        return False

    # MEL_CADENCE
    def check_mel_cadence(self):
        last_2_melody = (self.pitches[-2].pnum, self.pitches[-1].pnum)
        scale_2_1 = (self.key.scale()[1], self.key.scale()[0])
        scale_7_1 = (self.key.scale()[6], self.key.scale()[0])
        if (last_2_melody == scale_2_1 or last_2_melody == scale_7_1):
            return True
        return False

    # TODO - MEL_CADENCE
    # TODO - mel_tessitura
    # TODO - mel_diatonic

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print("I'm here!")


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
    # TODO - int_coinsonant
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


# A class representing a melodic analysis of a voice in a score. The class
# has three attributes to begin with, you will likely add more attributes.
# Consult the documentation for more information.
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
        # be sure to get the transition iterator inside the rules classes
        

    # You can define a cleanup function if you want.
    # def cleanup(self):
    #     self.melody, self.intervals, self.motions = [], [], []

    # You MUST define a setup function. A first few steps are
    # done for you, you can add more steps as you wish.
    def setup(self, args, kwargs):
        assert len(args) == 1, "Usage: analyze(<pvid>), pass the pvid of the voice to analyze."
        # melodic_id is the voice to analyze passed in by the caller.
        # you will want to use this when you access the timepoints
        self.melodic_id = args[0]
        self.tps = timepoints(self.score, span=True, measures=False, trace=True)
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
        # TODO - implement transitions

    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results

