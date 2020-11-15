###############################################################################

# Do not alter, add, or delete import statements
from .durational import Durational
from .note import Note


class Chord(Durational):

    def __init__(self, notes):
        last = notes[0]
        for n in notes:
            if ((not isinstance(n, Note)) or (n.dur != last.dur)):
                raise TypeError('Invalid list of notes')
            last = n
        self.notes = notes
        # not sure... can a chord be assigned to multiple voices?
        self.voice = []
        super().__init__(notes[0].dur)

    def __str__(self):
        return str(f'<Chord: {self.string()} {hex(id(self))}>')

    def __repr__(self):
        return str(f'<Chord: {self.string()}>')

    def string(self):
        return str(f'{Chord.list_string(self.notes)} {self.dur.string()}')

    @staticmethod
    def list_string(l):
        out = '('
        for element in l[:-1]:
            out += str(element) + ', '
        out += str(l[-1]) + ')'
        return out