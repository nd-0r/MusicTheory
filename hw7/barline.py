###############################################################################
# See barline.html for module documentation.

# Do not add or modify import statements.
from enum import Enum, auto


class Barline (Enum):
    # Create enums here...
    DASHED = auto()
    DOTTED = auto()
    FINAL_DOUBLE = auto()
    HEAVY = auto()
    INTERIOR_DOUBLE = auto()
    LEFT_REPEAT = auto()
    MIDDLE_REPEAT = auto()
    RIGHT_REPEAT = auto()
    SHORT = auto()
    STANDARD = auto()
    TICKED = auto()
