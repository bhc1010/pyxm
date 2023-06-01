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
        return f'{self.sig}e{self.exp}'

    def copy(self):
        return ExponentialNumber(self.sig, self.exp)

    def prefix(self) -> str:
        return self.prefix_map[str(self.exp)]
    
    def to_float(self) -> float:
        return self.sig * 10 ** (self.exp)
    