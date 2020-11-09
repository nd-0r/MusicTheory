###############################################################################


# Do not alter, add, or delete import statements
from .durational import Durational
from .pitch import Pitch


class Note (Durational):

    def __init__(self, pitch, dur, marks=[]):
        pass

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __gt__(self, other):
        pass

    def string(self):
        pass
