###############################################################################

# Do not alter, add, or delete import statements
from .ratio import Ratio
from .part import Part


class Score:

    def __init__(self, metadata={}, parts=[]):
        if (not isinstance(metadata, dict)):
            raise TypeError(f'Invalid metadata type: {type(metadata)}')
        self.metadata = metadata
        self.parts = []
        for p in parts:
            self.add_part(p)


    def __str__(self):
        try:
            title = self.metadata['work_title']
        except KeyError:
            try:
                title = self.metadata['movement_title']
            except KeyError:
                title = '(untitled)'
        return str(f'<Score: S{title} {hex(id(self))}>')

    def __repr__(self):
        try:
            title = self.metadata['work_title']
        except KeyError:
            try:
                title = self.metadata['movement_title']
            except KeyError:
                title = '(untitled)'
        return str(f'<Score: S{title}>')

    def __iter__(self):
        return iter(self.parts)

    def get_metadata(self, key, default=None):
        try:
            return self.metadata[key]
        except KeyError:
            return default

    def set_metadata(self, key, value):
        self.metadata[key] = value
        return value

    def add_part(self, part):
        if (not isinstance(part, Part)):
            raise TypeError(f'Invalid part type: {type(part)}')
        self.parts.append(part)

    def part_ids(self):
        return [p.id for p in self.parts]

    def num_parts(self):
        return len(self.parts)

    def get_part(self, pid):
        for p in self.parts:
            if (p.partid == pid):
                return p
        return None

    def print_all_repr(self):
        reprs = []
        indent = '  '
        reprs.append(repr(self))
        for p in self.parts:
            reprs.append(indent + repr(p))
            for s in p.staffs:
                reprs.append(2*indent + repr(s))
                for b in s.bars:
                    reprs.append(3*indent + repr(b))
                    for v in b.voices:
                        reprs.append(4*indent + repr(v))
                        for n in v.notes:
                            reprs.append(5*indent + repr(n))
        return reprs

    def print(self):
        print('\n'.join(self.print_all_repr()))

