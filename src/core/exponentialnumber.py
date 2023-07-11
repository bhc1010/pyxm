from __future__ import annotations
from decimal import Decimal

class ExponentialNumber:
    prefix_map = {'-12' : 'p',
                  '-9'  : 'n', 
                  '-6'  : '\u03BC', 
                  '-3'  : 'm', 
                  '0'   : ' ',
                  '3'   : 'k'}

    def default():
        return ExponentialNumber(0.0, 0)

    def __init__(self, sig: float, exp: int):
        self.sig = sig
        self.exp = exp

    def __repr__(self) -> str:
        try:
            return f'{round(self.sig, 3)} {self.prefix()}'
        except:
            return f'{self.sig}e{self.exp}'

    def copy(self):
        return ExponentialNumber(self.sig, self.exp)

    def prefix(self) -> str:
        return self.prefix_map[str(self.exp)]
    
    def to_float(self) -> float:
        return self.sig * 10 ** (self.exp)
    
    def from_float(x: float) -> ExponentialNumber:
        (_, digits, exponent) = Decimal(x).as_tuple()
        exp =  len(digits) + exponent - 3

        ## TODO: There has got to be a better way to do this. Clipping?
        if 0 < exp and exp < 3:
            exp = 3
        elif -3 < exp and exp < 0:
            exp = 0
        elif -6 < exp and exp < -3:
            exp = -3
        elif -9 < exp and exp < -6:
            exp = -6
        elif -12 < exp and exp < -9:
            exp = -6
        elif exp < -12:
            exp = -12

        sig =  round(float(Decimal(x).scaleb(-exp).normalize()), 3)
        
        return ExponentialNumber(sig, exp)
