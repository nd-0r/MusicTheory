###############################################################################

# Do not alter, add, or delete import statements
from .durational import Durational


class Rest (Durational):

    def __init__(self, dur):
        pass

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    def string(self):
        pass

    @classmethod
    def pad(cls, dur):
        pass

    def is_pad(self):
        pass


