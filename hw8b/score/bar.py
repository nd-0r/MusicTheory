###############################################################################

# Do not alter, add, or delete import statements.
from .voice import Voice


class Bar:

    def __init__(self, bid, clef=None, key=None, meter=None, barline=None, partial=False):
        self.bid = bid
        self.clef = clef
        self.key = key
        self.meter = meter
        self.barline = barline
        self.partial = partial

    def __str__(self):
        return ""

    def __repr__(self):
        return ""

    def __iter__(self):
        pass

    def add_voice(self, voice):
        pass

    def voice_ids(self):
        pass

    def num_voices(self):
        pass


if __name__ == "__main__":
    # add your testing code here.
    pass
