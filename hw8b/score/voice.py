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
        out = sum(self.notes.dur)

    def get_pvid(self):
        pass

