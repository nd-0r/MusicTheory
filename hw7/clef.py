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

    ALTO = (0, MIDDLE_LINE, 0)
    BARITONE = (1, TOP_LINE, 0)
    BARITONE_F = (2, MIDDLE_LINE, 0)
    BASS = (3, UPPER_MIDDLE_LINE, 0)
    BASS_15MA = (4, UPPER_MIDDLE_LINE, -15)
    BASS_8VA = (5, UPPER_MIDDLE_LINE, -8)
    FRENCH_VIOLIN = (6, BOTTOM_LINE, 0)
    MEZZO_SOPRANO = (7, LOWER_MIDDLE_LINE, 0)
    PERCUSSION = (8, MIDDLE_LINE, 0)
    SOPRANO = (9, BOTTOM_LINE, 0)
    SUB_BASS = (10, TOP_LINE, 0)
    TENOR = (11, UPPER_MIDDLE_LINE, 0)
    TENOR_TREBLE = (12, None, 0)  # what is this?
    TREBLE = (13, LOWER_MIDDLE_LINE, 0)
    TREBLE_15MA = (14, LOWER_MIDDLE_LINE, 15)
    TREBLE_8VA = (15, LOWER_MIDDLE_LINE, 8)

    def linespace(self):
        return self[1]

    def transposition(self):
        return self[2]
