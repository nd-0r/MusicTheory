###############################################################################
# See mark.html for module documentation.

# Do not add or modify import statements.
from enum import IntEnum

# Mark group constants 0-3 left-shifted 8 bits.
DYNAMIC = 0
ARTICULATION = 1
ORNAMENT = 2
TEMPORAL = 3


class Mark (IntEnum):
    # Create enums here...
    NIENTE = (DYNAMIC << 8) + 0
    PPPP = (DYNAMIC << 8) + 1
    PPP = (DYNAMIC << 8) + 2
    PP = (DYNAMIC << 8) + 3
    P = (DYNAMIC << 8) + 4
    MP = (DYNAMIC << 8) + 5
    MF = (DYNAMIC << 8) + 6
    F = (DYNAMIC << 8) + 7
    FF = (DYNAMIC << 8) + 8
    FFF = (DYNAMIC << 8) + 9
    FFFF = (DYNAMIC << 8) + 10
    SFZ = (DYNAMIC << 8) + 11
    CRESCENDO = (DYNAMIC << 8) + 12
    CRESCENDO_END = (DYNAMIC << 8) + 13
    DECRESCENDO = (DYNAMIC << 8) + 14
    DECRESCENDO_END = (DYNAMIC << 8) + 15

    TENUTO = (ARTICULATION << 8) + 0
    DETATCHED = (ARTICULATION << 8) + 1
    STACCATO = (ARTICULATION << 8) + 2
    STACCATISSIMO = (ARTICULATION << 8) + 3
    ACCENT = (ARTICULATION << 8) + 4
    MARCATO = (ARTICULATION << 8) + 5

    TRILL = (ORNAMENT << 8) + 0
    MORDENT = (ORNAMENT << 8) + 1
    TURN = (ORNAMENT << 8) + 2

    FERMATA = (TEMPORAL << 8) + 0
    ACCEL = (TEMPORAL << 8) + 1
    DEACCEL = (TEMPORAL << 8) + 2

    def rank(self):
        return self.value & 0b0000000011111111

    def group(self):
        return (self.value & 0b1111111100000000) >> 8
