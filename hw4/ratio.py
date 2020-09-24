###############################################################################
# ratio.py : A class that implements fractional numbers.
# See ratio.html for module documentation.

from math import gcd, pow
from decimal import Decimal
from collections import namedtuple


# A namedtuple base class for Ratio with num and den properties.
RatioBase = namedtuple('RatioBase', ['num', 'den'])


class Ratio (RatioBase):

    def __new__(cls, num, den=None):
        pass

    
    def __str__(self):
        pass


    def __repr__(self):
        pass


    def __mul__(self, other):
        pass

    
    # Implements right side multiplication (same code as __mul__)
    __rmul__ = __mul__


    def __truediv__(self, other):
        pass


    def __rtruediv__(self, other):
        pass

    
    def __invert__(self):
        pass


    def __add__(self, other):
        pass

    
    # Implements right side addition (same code as __add__)
    __radd__ = __add__


    def __neg__(self):
        pass
    

    def __sub__(self, other):
        pass
    

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
    

    def compare(self, other):
        pass


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
