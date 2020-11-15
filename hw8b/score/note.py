###############################################################################


# Do not alter, add, or delete import statements
from .durational import Durational
from .pitch import Pitch


class Note (Durational):

    def __init__(self, pitch, dur, marks=[]):
        if (not isinstance(pitch, Pitch)):
            raise TypeError(f'Invalid pitch type: {Type(pitch)}')
        super().__init__(dur)
        self.pitch = pitch
        self.marks = marks
        self.voice = None

    def __str__(self):
        return str(f'<{self.__class__}: {self.string()} {hex(id(self))}>')

    def __repr__(self):
        return str(f'<{self.__class__}: {self.string()}>')

    def __lt__(self, other):
        return self.pitch.__lt__(other)

    def __le__(self, other):
        return self.pitch.__le__(other)

    def __eq__(self, other):
        return self.pitch.__eq__(other)

    def __ne__(self, other):
        return self.pitch.__ne__(other)

    def __ge__(self, other):
        return self.pitch.__ge__(other)

    def __gt__(self, other):
        return self.pitch.__gt__(other)

    def string(self):
        return str(f'{self.pitch.string()} {self.dur.string()}')
