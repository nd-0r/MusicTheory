###############################################################################

## You can import from score, theory and any python module you want to use.

from .score import Pitch, Interval, Mode, import_score
from .theory import Analysis, Rule, timepoints
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

# superclass for pitch checks
class pitchCheck():
    pass

# superclass for melodic checks
class melodicIntervalCheck():
    pass

# superclass for leap checks
class leapCheck():
    pass

# superclass for shape checks
class shapeCheck():
    pass


class checkStartNote(Rule):

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


# A class representing a melodic analysis of a voice in a score. The class
# has three attributes to begin with, you will likely add more attributes.
# Consult the documentation for more information.
class MyMelodicAnalysis(Analysis):
    def __init__(self, score):
        # Call the superclass and give it the score. Don't change this line.
        super().__init__(score)
        # Copy the empty result checks template to this analysis. Don't
        # change this line
        self.results = copy(melodic_checks)
        # Create the list of rules this analysis runs. This example just
        # uses the demo Rule defined above.
        self.rules = [MyRule(self)]

    # You can define a cleanup function if you want.
    # def cleanup(self):
    #     self.melody, self.intervals, self.motions = [], [], []

    # You MUST define a setup function. A first few steps are
    # done for you, you can add more steps as you wish.
    def setup(self, args, kwargs):
        assert len(args) == 1, "Usage: analyze(<pvid>), pass the pvid of the voice to analyze."
        # melodic_id is the voice to analyze passed in by the caller.
        # you will want to use this when you access the timepoints
        melodic_id = args[0]
        tps = timepoints(self.score, span=True, measures=False)

    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results

