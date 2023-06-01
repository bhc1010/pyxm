from core.exponentialnumber import ExponentialNumber

class Bounds:
    def default():
        return Bounds(ExponentialNumber.default(), ExponentialNumber.default())
    
    def __init__(self, lower: ExponentialNumber, upper: ExponentialNumber):
        self.lower = lower
        self.upper = upper


    def clamp(self, value: ExponentialNumber) -> ExponentialNumber:
        if value.to_float() < self.lower.to_float():
            value = self.lower.copy()
        elif value.to_float() > self.upper.to_float():
            value = self.upper.copy()
        return value