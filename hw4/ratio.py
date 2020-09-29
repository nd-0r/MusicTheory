###############################################################################
# ratio.py : A class that implements fractional numbers.
# See ratio.html for module documentation.

from math import gcd, pow
from decimal import Decimal
from collections import namedtuple

# A namedtuple base class for Ratio with num and den properties.
RatioBase = namedtuple('RatioBase', ['num', 'den'])


class Ratio (RatioBase):

    # implement gcd
    def __new__(cls, num, den=None):
        hnum = None
        hden = None
        gcdiv = None

        if den == 0:
            raise ZeroDivisionError

        if isinstance(num, float) and den == None:
            tmp = Decimal(str(num)).as_integer_ratio()
            hnum = tmp[0]
            hden = tmp[1]
        elif isinstance(num, int) and den == None:
            hnum = num
            hden = 1
        elif isinstance(num, int) and isinstance(den, int):
            hnum = num
            hden = den
        elif isinstance(num, str) and den == None:
            tmp = num.split('/')
            hnum = int(tmp[0].strip())
            hden = int(tmp[1].strip())
        else:
            raise TypeError(f'Ratio with {num}, {den} is not a valid ratio')
        
        if hden < 0:
            hnum = -hnum
            hden = -hden

        gcdiv = gcd(hnum, hden)
        hnum = hnum // gcdiv
        hden = hden // gcdiv

        assert hden > 0, f'There is a problem with hden: {hden}'

        self = super(Ratio, cls).__new__(cls, hnum, hden)
        return self

    
    def __str__(self):
        print(f'<Ratio: {self.num}/{self.den} {hex(id(self))}>')


    def __repr__(self):
        return str(f'Ratio("{self.num}/{self.den}")')


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
            return Ratio(self.float() / other)
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
        if isinstance(other, Ratio):
            return Ratio((other.num * self.den) - (self.num * other.den), (self.den * other.den))
        elif isinstance(other, int):
            return Ratio((other * self.den) - self.num, self.den)
        elif isinstance(other, float):
            return Ratio(other - (self.num / self.den))
        else:
            raise TypeError(f'Ratio cannot be subtracted from {type(other)}')


    def __mod__(self, other):
        if not isinstance(other, Ratio):
            raise TypeError(f'Cannot perform modular arithmetic with Ratio and {type(other)}')
        dtmp = other.den * self.den
        ntmpself = self.num * other.den
        ntmpother = other.num * self.den
        return Ratio(ntmpself - (ntmpother * (ntmpself // ntmpother)), dtmp)


    def __pow__(self, other):
        out = None
        if isinstance(other, int):
            out = Ratio(int(pow(self.num, abs(other))), abs(int(pow(self.den, other))))
            if other < 0:
                return out.reciprocal()
            return out
        elif isinstance(other, Ratio):
            out = Ratio(pow(self.num, abs(other.float())), pow(self.den, abs(other.float())))
            if other.float() < 0:
                return out.reciprocal()
            return out
        elif isinstance(other, float):
            out = Ratio(pow(self.num, abs(other)), pow(self.den, abs(other)))
            if other.float() < 0:
                return out.reciprocal()
            return out
        else:
            raise TypeError(f'Cannot raise a ratio to the power of type {type(other)}')


    def __rpow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return pow(other, self.float())
        else:
            raise TypeError(f'Cannot raise type {type(other)} to fractional power')


    def __lt__(self, other):
        if self.compare(other) < 0:
            return True
        return False

    
    def __le__(self, other):
        if self.compare(other) <= 0:
            return True
        return False

    
    def __eq__(self, other):
        if self.compare(other) == 0:
            return True
        return False


    def __ne__(self, other):
        if self.compare(other) != 0:
            return True
        return False


    def __ge__(self, other):
        if self.compare(other) >= 0:
            return True
        return False


    def __gt__(self, other):
        if self.compare(other) > 0:
            return True
        return False


    def __hash__(self):
        return hash(tuple(self.num, self.den))
    

    # if less, return -1; if equal, return 0; if greater than, return 1
    # this method might present rounding issues because I convert the float 
    #   to a ratio and then compare the ratio
    def compare(self, other):
        tmp = None
        if isinstance(other, Ratio):
            tmp = other
        elif isinstance(other, int):
            tmp = Ratio(other * self.den, self.den)
        elif isinstance(other, float):
            tmp = Ratio(other)
        else:
            raise TypeError(f'Ratio cannot be compared to {type(other)}')
        diff = (self.num * tmp.den) - (tmp.num * self.den)
        if diff < 0:
            return -1
        elif diff == 0:
            return 0
        else:
            return 1

    # generators and closures
    @staticmethod
    def lcm(a, b):
        if isinstance(a, int) and isinstance(b, int):
            return int((a * b) // gcd(a, b))
        else:
            raise TypeError(f'Cannot find the least common multiple of a type {type(a)} and a type {type(b)}')

    
    def string(self):
        if self.num == 0:
            return "zero"
        
        counts = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
        teencounts = ('ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventen', 'eighteen', 'nineteen')
        ints = ('first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth')
        teens = ('tenth', 'eleventh', 'twelth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth')
        tens = ('twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety')

        out = None
        ntmp = None
        dtmp = None

        if abs(self.num) < 10:
            ntmp = counts[self.num - 1]
        elif abs(self.num) < 20:
            ntmp = teencounts[self.num % 10]
        elif abs(self.num) < 100:
            if self.num % 10 == 0:
                ntmp = tens[self.num // 10 - 2]
            else:
                ntmp = tens[self.num // 10 - 2] + "-" + counts[self.num % 10 - 1]
        else:
            raise ValueError(f'Cannot convert numerator to natural string')

        if abs(self.den) < 10 and abs(self.den) > 1:
            if abs(self.den) == 2 and abs(self.num) > 1:
                dtmp = "halves"
            elif abs(self.den) == 2:
                dtmp = "half"
            elif abs(self.den) == 4 and abs(self.num) > 1:
                dtmp = "quarters"
            elif abs(self.den) == 4:
                dtmp = "quarter"
            elif abs(self.num) != 1:
                dtmp = ints[self.den - 1] + "s"
            else:
                dtmp = ints[self.den - 1]
        elif abs(self.den) < 20:
            if abs(self.num) != 1:
                dtmp = teens[self.den % 10] + "s"
            else:
                dtmp = teens[self.den % 10]
        elif abs(self.den) < 100:
            if abs(self.den) % 10 == 0:
                dtmp = tens[self.den // 10 - 2][0:-1] + "ieth"
            else:
                dtmp = tens[self.den // 10 - 2] + "-" + ints[self.den % 10 - 1]
            if abs(self.num) != 1:
                dtmp = dtmp + "s"
        else:
            raise ValueError(f'Cannot convert denominator to natural string')
        
        assert isinstance(ntmp, str) and isinstance(dtmp, str), f'ntmp: {type(ntmp)} \n dtmp: {type(dtmp)}'

        out = ntmp + " " + dtmp
        if self.num < 0:
            out = "negative " + out
        
        return out


    def reciprocal(self):
        return self.__invert__()


    def dotted(self, dots=1):
        if not (isinstance(dots, int)):
            raise TypeError(f'Cannot accept dots as type {type(dots)}')
        elif dots < 0:
            raise ValueError(f'Cannot have a negative amount of dots')
        return Ratio.dotter(self, dots)


    def tuplets(self, num, intimeof=1):
        self *= intimeof
        return tuple(self.tup(num) for _ in range(0, num))

    
    def tup(self, num):
        if not (isinstance(num, int)):
            raise TypeError(f'Cannot accept number of divisions as type {type(num)}')
        elif num < 0:
            raise ValueError(f'Cannot have negative divisions')
        return self / num

    
    def float(self):
        return float(self.num / self.den)


    def seconds(self, tempo=60, beat=None):
        if not ((isinstance(beat, int) or beat == None) and isinstance(tempo, int)):
            raise TypeError(f'Cannot calculate time with tempo type: {type(tempo)} and beat type {type(beat)}')
        if (beat != None and beat < 0) or tempo < 0:
            raise ValueError(f'Cannot calculate time when beat or tempo is less than zero')
        bps = tempo * 60
        if beat != None:
            beats = self / beat
        else:
            beats = self.num
        return float(bps * beats)

    @staticmethod
    def dotter(frac, dots):
        assert isinstance(dots, int), f'dots is not an integer.'
        if dots == 0:
            return frac
        return Ratio.dotter(frac + (frac / 2), dots - 1)


if __name__ == '__main__':
    print("Testing...")
    
    # add whatever test code you want here!

    print("Done!")
