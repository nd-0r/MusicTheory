###############################################################################

# Do not alter, add, or delete import statements
from .ratio import Ratio


class Durational:

    def __init__(self, dur):
        if (not isinstance(dur, Ratio)):
            raise TypeError(f'cannot initialize duration to an object of type: {type(dur)}')
        self.dur = dur

    def string(self):
        return dur.string()

    def get_pvid(self):
        