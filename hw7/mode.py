###############################################################################
# See mode.html for module documentation.

# Do not add or modify import statements.
from enum import IntEnum


class Mode (IntEnum):
    # Create enums here...
    MAJOR = 0
    DORIAN = 1
    PHRYGIAN = 2
    LYDIAN = 3
    MIXOLYDIAN = 4
    MINOR = 5
    LOCRIAN = 6
    IONIAN = MAJOR
    AEOLIAN = MINOR

    def short_name(self):
        return self.name[0: 3]

    def tonic_degree(self):
        return self.value
