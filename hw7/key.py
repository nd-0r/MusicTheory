###############################################################################
# See key.html for module documentation.

# Do not add or modify import statements.
from .pitch import Pitch
from .mode import Mode
from .interval import Interval



class Key:

    def __init__(self, signum, mode):
        assert (isinstance(signum, int))
        assert (isinstance(mode, int))
        if (-7 > signum > 7):
            raise ValueError(f'Cannot use signum {signum}')
        if (0 > mode > 6):
            raise ValueError(f'Cannot use mode {mode}')
        self.signum = signum
        self.mode = mode

    def __str__(self):
        return ''

    def __repr__(self):
        return ''

    def string(self):
        if (self.signum < -1):
            k = Pitch.fromKeynum(69 + ((7 * 7) % 12), 'b').string()[:-1]
        elif (self.signum > 5):
            k = Pitch.fromKeynum(69 + ((7 * 7) % 12), 's').string()[:-1]
        else:
            k = Pitch.fromKeynum(69 + ((7 * 7) % 12)).string()[:-1]
        m = Mode(self.mode).name.lower()
        return (k + ' ' + m)

    def tonic(self):
        pass

    def scale(self):
        pass


