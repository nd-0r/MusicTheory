###############################################################################
# See key.html for module documentation.

# Do not add or modify import statements.
from .pitch import Pitch as P
from .mode import Mode
from .interval import Interval


class Key:

    _diatonic_intervals = ['P1', 'M2', 'm3', 'P4', 'P5', 'M6', 'M7']

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
            k = P.fromKeynum(69 + ((self.signum * 7) % 12), 'b').string()[:-1]
        elif (self.signum > 5):
            k = P.fromKeynum(69 + ((self.signum * 7) % 12), 's').string()[:-1]
        else:
            k = P.fromKeynum(69 + ((self.signum * 7) % 12)).string()[:-1]
        m = Mode(self.mode).name.lower()
        return (k + ' ' + m)

    def tonic(self):
        if (self.signum < -1):
            p = P.fromKeynum(69 + ((self.signum * 7) % 12), 'b').string()[:-1]
        elif (self.signum > 5):
            p = P.fromKeynum(69 + ((self.signum * 7) % 12), 's').string()[:-1]
        else:
            p = P.fromKeynum(69 + ((self.signum * 7) % 12)).string()[:-1]
        return Interval(self._diatonic_intervals[self.mode], p)

    def scale(self):
        pass


