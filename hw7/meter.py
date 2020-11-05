###############################################################################
# See meter.html for module documentation.

# Do not add or modify import statements.
from .ratio import Ratio


class Meter:

    def __init__(self, num, den):
        if num not in range(1, 17):
            raise ValueError(f'Invalid numerator: {num}')
        elif den not in {2 ** i for i in range(0, 6)}:
            raise ValueError(f'Invalid denominator: {den}')
        try:
            self.num = num
            self.den = den
        except TypeError:
            raise TypeError(f'Invalid numerator of type: {type(num)}'
                            f'or denominator of type: {type(den)}')

    def __str__(self):
        return str(f'<Meter: {self.num}/{self.den} {hex(id(self))}>')

    def __repr__(self):
        return str(f'Meter("{self.string()}")')

    def string(self):
        return f'{self.num}/{self.den}'

    def is_compound(self):
        return (self.num in (6, 9, 12, 15))

    def is_simple(self):
        return (self.num in (1, 2, 3, 4))

    def is_complex(self):
        return (self.num in (5, 7, 8, 10, 11, 13, 14))

    def is_duple(self):
        return (self.num in (2, 6))

    def is_triple(self):
        return (self.num in (3, 9))

    def is_quadruple(self):
        return (self.num in (4, 12))

    def is_quintuple(self):
        return (self.num in (5, 15))

    def is_septuple(self):
        return (self.num == 7)

    def beat(self):
        if (not(self.is_simple() or self.is_compound())):
            raise NotImplementedError('Cannot get beat for non-simple',
                                      'or non-compound rhythms yet')
        if (self.is_duple()):
            return Ratio(self.num // 2, self.den)
        elif (self.is_triple()):
            return Ratio(self.num // 3, self.den)
        elif (self.is_quadruple()):
            return Ratio(self.num // 4, self.den)
        elif (self.is_quintuple()):
            return Ratio(self.num // 5, self.den)
        elif (self.is_septuple()):
            return Ratio(self.num // 6, self.den)
        else:
            raise ValueError(f'Cannot get beat from meter: {self.string()}')

    def measure_dur(self):
        return Ratio(self.num, self.den)
