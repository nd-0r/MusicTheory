###############################################################################

# Do not alter, add, or delete import statements
from .durational import Durational


class Rest (Durational):

    def __init__(self, dur):
        super().__init__(dur)
        self.pitch = None
        self.marks = None
        self.voice = None

    def __str__(self):
        return str(f'<{self.__class__}: {self.dur.string()} {hex(id(self))}>')

    def __repr__(self):
        return str(f'<{self.__class__}: {self.dur.string()}>')

    def string(self):
        return str(f'R {self.dur.string()}')

    @classmethod
    def pad(cls, dur):
        to_return = Rest(dur)
        to_return.pad = True
        return to_return

    def is_pad(self):
        return self.pad