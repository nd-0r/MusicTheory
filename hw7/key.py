###############################################################################
# See key.html for module documentation.

# Do not add or modify import statements.
from .pitch import Pitch
from .mode import Mode
from .interval import Interval


class Key:

    _diatonic_intervals = ['P1', 'M2', 'm3', 'P4', 'P5', 'M6', 'M7']

    def __init__(self, signum, mode):
        if (isinstance(signum, int)):
            if (-7 > signum > 7):
                raise ValueError(f'Cannot use signum {signum}')
            self.signum = signum
            if (isinstance(mode, Mode)):
                self.mode = mode
            else:
                try:
                    self.mode = Mode[mode.upper()].value
                except Exception:
                    raise TypeError("mode must be an enum or a valid str")
        else:
            raise TypeError("signum must be an int")

    def __str__(self):
        return ''

    def __repr__(self):
        return ''

    def string(self):
        k = self.tonic().name
        m = self.mode.name.lower()
        if ('n' in k):
            k = k[:-1]
        return (k + '-' + m)

    def get_base_pitch(self):
        if (self.signum < -1):
            return Pitch.fromKeynum(69 + ((self.signum * 7) % 12), 'b')
        elif (self.signum > 5):
            return Pitch.fromKeynum(69 + ((self.signum * 7) % 12), 's')
        return Pitch.fromKeynum(69 + ((self.signum * 7) % 12))

    def tonic(self):
        p = self.get_base_pitch()
        i = self._diatonic_intervals[self.mode.value]
        return Interval(i).transpose(p).pnum()

    def scale(self):
        out = []
        for interval in self._diatonic_intervals:
            out.append(Interval(interval).transpose(self.get_base_pitch).pnum)
        return out[self.mode.value:] + out[:self.mode.value]
