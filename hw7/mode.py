###############################################################################
# See mode.html for module documentation.

# Do not add or modify import statements.
from enum import IntEnum


class Mode (IntEnum):
    # Create enums here...
    IONIAN = 0
    DORIAN = 1
    PHRYGIAN = 2
    LYDIAN = 3
    MIXOLYDIAN = 4
    AEOLIAN = 5
    LOCRIAN = 6
    MAJOR = IONIAN
    MINOR = AEOLIAN

    def short_name(self):
        return Mode(self).name[0: 3]  # I dunno...

    def tonic_degree(self):
        return self.value
