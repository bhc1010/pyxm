from __future__ import annotations
from decimal import Decimal

class ExponentialNumber:
    """
    Class representing a number in exponential notation.

    This class allows representing a number in the form of 'sig x 10^exp',
    where 'sig' is the significand and 'exp' is the exponent.

    Attributes:
        prefix_map (dict): A mapping of exponents to their corresponding SI prefixes.
        sig (float): The significand of the exponential number.
        exp (int): The exponent of the exponential number.
    """

    prefix_map = {'-12': 'p',
                  '-9': 'n', 
                  '-6': '\u03BC', 
                  '-3': 'm', 
                  '0': ' ',
                  '3': 'k'}

    @staticmethod
    def default() -> ExponentialNumber:
        """
        Static method to create a new ExponentialNumber with default values.

        Returns:
            ExponentialNumber: A new ExponentialNumber object with sig = 0.0 and exp = 0.
        """
        return ExponentialNumber(0.0, 0)

    def __init__(self, sig: float, exp: int):
        """
        Initialize an ExponentialNumber with the specified significand and exponent.

        Args:
            sig (float): The significand of the exponential number.
            exp (int): The exponent of the exponential number.
        """
        self.sig = sig
        self.exp = exp

    def __repr__(self) -> str:
        """
        Return the string representation of the ExponentialNumber.

        Returns:
            str: The string representation of the ExponentialNumber in the form 'sig x 10^exp'.
        """
        try:
            return f'{round(self.sig, 3)} {self.prefix()}'
        except:
            return f'{self.sig}e{self.exp}'

    def copy(self) -> ExponentialNumber:
        """
        Create a copy of the ExponentialNumber.

        Returns:
            ExponentialNumber: A new ExponentialNumber object with the same sig and exp as the original.
        """
        return ExponentialNumber(self.sig, self.exp)

    def prefix(self) -> str:
        """
        Get the SI prefix corresponding to the exponent.

        Returns:
            str: The SI prefix for the current exponent, or an empty string if no prefix exists.
        """
        return self.prefix_map[str(self.exp)]

    def to_float(self) -> float:
        """
        Convert the ExponentialNumber to its floating-point representation.

        Returns:
            float: The floating-point representation of the ExponentialNumber.
        """
        return self.sig * 10 ** (self.exp)

    @staticmethod
    def from_float(x: float) -> ExponentialNumber:
        """
        Create an ExponentialNumber from a floating-point value.

        Args:
            x (float): The floating-point value.

        Returns:
            ExponentialNumber: The ExponentialNumber representation of the floating-point value.
        """
        (_, digits, exponent) = Decimal(x).as_tuple()
        exp = len(digits) + exponent - 3

        # TODO: There has got to be a better way to do this. Clipping?
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

        sig = round(float(Decimal(x).scaleb(-exp).normalize()), 3)

        return ExponentialNumber(sig, exp)
