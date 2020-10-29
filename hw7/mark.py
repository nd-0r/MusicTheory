###############################################################################
# See mark.html for module documentation.

# Do not add or modify import statements.
from enum import IntEnum

# Mark group constants 0-3 left-shifted 8 bits.
DYNAMIC = 0 << 8
ARTICULATION = 1 << 8
ORNAMENT = 2 << 8
TEMPORAL = 3 << 8


class Mark (IntEnum):
    # Create enums here...

    def rank(self):
        pass

    def group(self):
       pass
