###############################################################################

from .ratio import Ratio
from .durational import Durational


class Voice:

    def __init__(self, voiceid):
        self.id = voiceid
        self.bar = []
        self.notes = []

    def __str__(self):
        return str(f'<Voice: {self.id} {hex(id(self))}')

    def __repr__(self):
        return str(f'<Voice: {self.id}>')

    def __iter__(self):
        return iter(self.notes)

    def add_note(self, note):
        if (not isinstance(note, Durational)):
            raise TypeError(f'Invalid type: {type(note)}')
        self.notes.append(note)

    def dur(self):
        out = Ratio(0)
        for n in self.notes:
            out += n.dur
        return out

    def get_pvid(self):
        return 'P' + str(self.partid) + '.' + str(self.id)

