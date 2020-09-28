###############################################################################
# ratio.py : A class that implements fractional numbers.
# See ratio.html for module documentation.

from math import gcd, pow
from decimal import Decimal
from collections import namedtuple

# def tup(self, num):
#     self.num
#     return Ratio(num, whatever)

# A namedtuple base class for Ratio with num and den properties.
RatioBase = namedtuple('RatioBase', ['num', 'den'])


class Ratio (RatioBase):

    # implement gcd and accomodation of negatives
    def __new__(cls, num, den=None):
        hnum = None
        hden = None

        if den == 0:
            raise ZeroDivisionError

        if isinstance(num, float) and den == None:
            tmp = Decimal(str(num)).as_integer_ratio()
            hnum = tmp[0]
            hden = tmp[1]
        elif isinstance(num, int) and den == None:
            hnum = num
            hden = 1
        elif isinstance((num, den), (int, int)):
            hnum = num
            hden = den
        elif isinstance(num, str) and den == None:
            tmp = num.split('/')
            hnum = int(tmp[0])
            hden = int(tmp[1])
        else:
            raise TypeError(f'Ratio with {num}, {den} is not a valid ratio')

        self = super(Ratio, cls).__new__(cls, hnum, hden)
        return self

    
    def __str__(self):
        print(f'<Ratio: {self.num}/{self.den} {hex(id(self))}>')


    def __repr__(self):
        print(f'Ratio("{self.num}/{self.den}")')


    def __mul__(self, other):
        if isinstance(other, Ratio):
            return Ratio(self.num * other.num, self.den * other.den)
        elif isinstance(other, int):
            return Ratio(self.num * other, self.den)
        elif isinstance(other, float):
            return Ratio((self.num / self.den) * other)
        else:
            raise TypeError(f'Ratio cannot be multiplied by {type(other)}')

    
    # Implements right side multiplication (same code as __mul__)
    __rmul__ = __mul__


    def __truediv__(self, other):
        if isinstance(other, Ratio):
            return Ratio(self.num * other.den, self.den * other.num)
        elif isinstance(other, int):
            return Ratio(self.num, self.den * other)
        elif isinstance(other, float):
            return Ratio((self.num / self.den) / other)
        else:
            raise TypeError(f'Ratio cannot be divided by {type(other)}')

    # Ratio / Ratio, int / Ratio, float / Ratio - check for divide by 0
    def __rtruediv__(self, other):
        if isinstance(other, Ratio):
            return Ratio(self.den * other.num, self.num * other.den)
        elif isinstance(other, int):
            return Ratio(self.den * other, self.num)
        elif isinstance(other, float):
            return Ratio(other / (self.num / self.den))
        else:
            raise TypeError(f'{type(other)} cannot be divided by Ratio')

    
    def __invert__(self):
        return Ratio(self.den, self.num)


    def __add__(self, other):
        if isinstance(other, Ratio):
            return Ratio((self.num * other.den) + (other.num * self.den), (self.den * other.den))
        elif isinstance(other, int):
            return Ratio(self.den * other, self.num)
        elif isinstance(other, float):
            return Ratio(other / (self.num / self.den))
        else:
            raise TypeError(f'{type(other)} cannot be added to Ratio')
    
    # Implements right side addition (same code as __add__)
    __radd__ = __add__


    def __neg__(self):
        return Ratio(- self.num, self.den)
    

    def __sub__(self, other):
        if isinstance(other, Ratio):
            return Ratio((self.num * other.den) - (other.num * self.den), (self.den * other.den))
        elif isinstance(other, int):
            return Ratio(self.num - (other * self.den), self.den)
        elif isinstance(other, float):
            return Ratio((self.num / self.den) - other)
        else:
            raise TypeError(f'{type(other)} cannot be subtracted from Ratio')
    

    def __rsub__(self, other):
        pass


    def __mod__(self, other):
        pass


    def __pow__(self, other):
        pass


    def __rpow__(self, other):
        pass


    def __lt__(self, other):
        pass

    
    def __le__(self, other):
        pass

    
    def __eq__(self, other):
        pass


    def __ne__(self, other):
        pass


    def __ge__(self, other):
        pass


    def __gt__(self, other):
        pass


    def __hash__(self):
        pass
    

    # if less, return -1; if equal, return 0; if greater than, return 1
    def compare(self, other):
        pass

    # generators and closures
    @staticmethod
    def lcm(a, b):
        pass

    
    def string(self):
        pass


    def reciprocal(self):
        pass


    def dotted(self, dots=1):
        pass


    def tuplets(self, num, intimeof=1):
        pass


    def tup(self, num):
        pass


    def float(self):
        pass


    def seconds(self, tempo=60, beat=None):
        pass


if __name__ == '__main__':
    print("Testing...")
    
    # add whatever test code you want here!

    print("Done!")
