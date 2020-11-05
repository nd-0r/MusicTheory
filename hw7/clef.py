###############################################################################
# See clef.html for module documentation.

# Do not add or modify import statements.
from enum import Enum

# Add the remaining Line-Space unit constants here
TOP_LINE = 8
TOP_SPACE = 7
UPPER_MIDDLE_LINE = 6
UPPER_MIDDLE_SPACE = 5
MIDDLE_LINE = 4
LOWER_MIDDLE_SPACE = 3
LOWER_MIDDLE_LINE = 2
BOTTOM_SPACE = 1
BOTTOM_LINE = 0


class Clef (Enum):
    # Create enums here...

    ALTO = (3, MIDDLE_LINE, 0)
    BARITONE = (5, TOP_LINE, 0)
    BARITONE_F = (12, MIDDLE_LINE, 0)
    BASS = (6, UPPER_MIDDLE_LINE, 0)
    BASS_15MA = (10, UPPER_MIDDLE_LINE, -15)
    BASS_8VA = (8, UPPER_MIDDLE_LINE, -8)
    FRENCH_VIOLIN = (14, BOTTOM_LINE, 0)
    MEZZO_SOPRANO = (2, LOWER_MIDDLE_LINE, 0)
    PERCUSSION = (15, MIDDLE_LINE, 0)
    SOPRANO = (1, BOTTOM_LINE, 0)
    SUB_BASS = (13, TOP_LINE, 0)
    TENOR = (4, UPPER_MIDDLE_LINE, 0)
    TENOR_TREBLE = (11, LOWER_MIDDLE_LINE, -8)
    TREBLE = (0, LOWER_MIDDLE_LINE, 0)
    TREBLE_15MA = (9, LOWER_MIDDLE_LINE, 15)
    TREBLE_8VA = (7, LOWER_MIDDLE_LINE, 8)

    def linespace(self):
        return self.value[1]

    def transposition(self):
        return self.value[2]
