###############################################################################
# See key.html for module documentation.

# Do not add or modify import statements.
from .pitch import Pitch
from .mode import Mode
from .interval import Interval


class Key:

    _diatonic_intervals = ['P1', 'M2', 'M3', 'P4', 'P5', 'M6', 'M7']

    def __init__(self, signum, mode):
        if (isinstance(signum, int)):
            if (signum > 7 or signum < -7):
                raise ValueError(f'Cannot use signum {signum}')
            self.signum = signum
            if (isinstance(mode, Mode)):
                self.mode = mode
            else:
                try:
                    self.mode = Mode[mode.upper()]
                except Exception:
                    raise TypeError("mode must be an enum or a valid str")
        else:
            raise TypeError("signum must be an int")

    # '<Key: C-Major (0 sharps or flats) 0x10c03c050>'
    def __str__(self):
        if (self.signum == 0):
            s_or_f = '(0 sharps or flats)'
        elif (self.signum < -1):
            s_or_f = f'({abs(self.signum)} flats)'
        elif (self.signum < 0):
            s_or_f = '(1 flat)'
        elif (self.signum > 1):
            s_or_f = f'({abs(self.signum)} sharps)'
        else:
            s_or_f = '(1 sharp)'
        # return str(f'<Key: {self.string()} {s_or_f} {hex(id(self))}>')
        return str(f'<Key: {self.string()} {s_or_f}>')

    # 'Key(4, "Dorian")'
    def __repr__(self):
        return f'Key({self.signum}, "{Mode(self.mode).name.title()}")'

    def string(self):
        k = self.tonic().name
        m = self.mode.name.title()
        if ('n' in k):
            k = k[:-1]
        return (k + '-' + m)

    def get_base_pitch(self):
        if (self.signum < -1):
            return Pitch.from_keynum(60 + ((self.signum * 7) % -12), 'b')
        elif (self.signum > 5):
            return Pitch.from_keynum(60 + ((self.signum * 7) % 12), 's')
        elif (self.signum == -1):
            return Pitch.from_keynum(60 + ((self.signum * 7) % -12))
        return Pitch.from_keynum(60 + ((self.signum * 7) % 12))

    def tonic(self):
        p = self.get_base_pitch()
        i = self._diatonic_intervals[self.mode.value]
        return Interval(i).transpose(p).pnum()

    def scale(self):
        out = []
        for interval in self._diatonic_intervals:
            out.append(
                Interval(interval).transpose(self.get_base_pitch()).pnum()
                )
        return out[self.mode.value:] + out[:self.mode.value]
