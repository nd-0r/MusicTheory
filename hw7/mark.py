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
    NIENTE = DYNAMIC + 0
    PPPP = DYNAMIC + 1
    PPP = DYNAMIC + 2
    PP = DYNAMIC + 3
    P = DYNAMIC + 4
    MP = DYNAMIC + 5
    MF = DYNAMIC + 6
    F = DYNAMIC + 7
    FF = DYNAMIC + 8
    FFF = DYNAMIC + 9
    FFFF = DYNAMIC + 10
    SFZ = DYNAMIC + 11
    CRESCENDO = DYNAMIC + 12
    CRESCENDO_END = DYNAMIC + 13
    DECRESCENDO = DYNAMIC + 14
    DECRESCENDO_END = DYNAMIC + 15

    TENUTO = ARTICULATION + 0
    DETATCHED = ARTICULATION + 1
    STACCATO = ARTICULATION + 2
    STACCATISSIMO = ARTICULATION + 3
    ACCENT = ARTICULATION + 4
    MARCATO = ARTICULATION + 5

    TRILL = ORNAMENT + 0
    MORDENT = ORNAMENT + 1
    TURN = ORNAMENT + 2

    FERMATA = TEMPORAL + 0
    ACCEL = TEMPORAL + 1
    DEACCEL = TEMPORAL + 2

    def rank(self):
        return self.value & 0b0000000011111111

    def group(self):
        return (self.value & 0b1111111100000000) >> 8
