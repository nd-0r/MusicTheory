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
        temp = self.get_strings()
        assert(len(temp) == 4)
        return str(f'<Bar: {self.bid} {temp[0]} {temp[1]} {temp[2]} {temp[3]} {hex(id(self))}>')

    # <Bar: 0 Treble A-Major 2/4 STANDARD>
    def __repr__(self):
        temp = self.get_strings()
        assert(len(temp) == 4)
        return str(f'<Bar: {self.bid} {temp[0]} {temp[1]} {temp[2]} {temp[3]}>')

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
    
    def get_strings(self):
        out = []
        try:
            out.append(self.clef.name.title())
        except Exception:
            out.append('')
        try:
            out.append(self.key.string())
        except Exception:
            out.append('')
        try:
            out.append(self.meter.string())
        except Exception:
            out.append('')
        try:
            out.append(self.barline.name)
        except Exception:
            out.append('')        
        return out

if __name__ == "__main__":
    # add your testing code here.
    pass
