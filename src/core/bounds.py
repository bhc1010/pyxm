from core.exponentialnumber import ExponentialNumber

class Bounds:
    """
    Class representing a range of values with upper and lower bounds.

    This class is used to represent a range of values with upper and lower bounds.
    It allows clamping a given value to ensure it stays within the defined range.

    Attributes:
        lower (ExponentialNumber): The lower bound of the range.
        upper (ExponentialNumber): The upper bound of the range.
    """

    @staticmethod
    def default() -> 'Bounds':
        """
        Static method to create a new Bounds object with default ExponentialNumber bounds.

        Returns:
            Bounds: A new Bounds object with default ExponentialNumber bounds.
        """
        return Bounds(ExponentialNumber.default(), ExponentialNumber.default())

    def __init__(self, lower: ExponentialNumber, upper: ExponentialNumber):
        """
        Initialize a Bounds object with the specified lower and upper bounds.

        Args:
            lower (ExponentialNumber): The lower bound of the range.
            upper (ExponentialNumber): The upper bound of the range.
        """
        self.lower = lower
        self.upper = upper

    def clamp(self, value: ExponentialNumber) -> ExponentialNumber:
        """
        Clamp the given value to ensure it stays within the defined range.

        If the given value is outside the range, it will be set to the nearest boundary value.

        Args:
            value (ExponentialNumber): The value to be clamped.

        Returns:
            ExponentialNumber: The clamped value that stays within the defined range.
        """
        if value.to_float() < self.lower.to_float():
            value = self.lower.copy()
        elif value.to_float() > self.upper.to_float():
            value = self.upper.copy()
        return value
