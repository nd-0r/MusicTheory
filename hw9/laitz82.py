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
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print("I'm here!")


class intervalChecks(Rule):

    def __init__(self, analysis):
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print("I'm here!")


class leapChecks(Rule):

    def __init__(self, analysis):
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

    def display(self, index):
        print('-------------------------------------------------------------------')
        print(f"Rule {index+1}: {self.title}")
        print("I'm here!")


class shapeChecks(Rule):

    def __init__(self, analysis):
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "Check that the starting note is tonic, mediant, or dominant")
        # Now initialize whatever attributes your rule defines.
        self.notes = self.score.getPart()

    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

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
        self.tps = timepoints(self.score, span=True, measures=False)
        # add transitions

    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results

