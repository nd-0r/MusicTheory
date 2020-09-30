from enum import Enum, IntEnum, auto

# Project: complete this implementation

class ScaleDegrees (Enum):
    # Degree enums, values are the semitonal content of the
    # major scale degrees
    SD1 = 
    SD2 = 
    SD3 = 
    SD4 = 
    SD5 = 
    SD6 = 
    SD7 = 

    # Inflection enums, values -1 to 1
    LOWERED = 
    DIATONIC = 
    RAISED = 

    # ScaleDegree enums, each is a tuple: (degree, inflection)
    TONIC =  ()
    RAISED_TONIC =  ()
    LOWERED_TONIC = ()

    # ...define remaining scale degrees here...


    
    def degree(self):
        """Returns the degree enum for this enum.
        Hint: the first tuple value of this enum
        will be the value of the degree enum."""
        
        return 0
    

    def inflection(self):
        """Returns the inflection enum for this enum.
        Hint: the second tuple value of this enum
        will be the value of the inflection enum."""
        
        return 0

    
    def semitones(self):
        """Returns the number of semitones in this
        scale degree.  Hint: Use the values of degrees
        and inflectons to determine the semitonal content""
        
        return 0
