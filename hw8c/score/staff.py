###############################################################################

from .bar import Bar


class Staff:

    def __init__(self, staffid):
        self.id = staffid
        self.bars = []
        self.part = None

    def __str__(self):
        return str(f'<Staff: {self.id} {hex(id(self))}>')

    def __repr__(self):
        return str(f'<Staff: {self.id}>')

    def __iter__(self):
        return iter(bars)

    def add_bar(self, bar):
        if (not isinstance(bar, Bar)):
            raise TypeError(f'Invalid type: {type(bar)}')
        self.bars.append(bar)

    def bar_ids(self):
        return [b.id for b in self.bars]

    def num_bars(self):
        return len(self.bars)