###############################################################################

# Do not alter, add, or delete import statements.
from .voice import Voice


class Bar:

    def __init__(self, bid, clef=None, key=None, meter=None, barline=None, partial=False):
        self.bid = bid
        self.clef = clef
        self.key = key
        self.meter = meter
        self.voices = []
        self.barline = barline
        self.partial = partial
        self.staff = None

    # <Bar: 0 Treble A-Major 2/4 STANDARD 0x109667790>
    def __str__(self):
        return str(f'<{self.__class__}: {self.bid} {self.clef.string()} {self.key.string()} {self.meter.string()} {self.barline.string()} {hex(id(self))}>')

    # <Bar: 0 Treble A-Major 2/4 STANDARD>
    def __repr__(self):
        return str(f'<{self.__class__}: {self.bid} {self.clef.string()} {self.key.string()} {self.meter.string()} {self.barline.string()}>')

    def __iter__(self):
        return iter(voices)

    def add_voice(self, voice):
        if (not isinstance(voice, Voice)):
            raise TypeError(f'Invalid voice type: {type(voice)}')
        self.voices.append(voice)

    def voice_ids(self):
        return [v.id for v in self.voices]

    def num_voices(self):
        return len(self.voices)


if __name__ == "__main__":
    # add your testing code here.
    pass
