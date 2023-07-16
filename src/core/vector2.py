from dataclasses import dataclass

@dataclass
class Vector2:
    """
        Represents a 2D vector with x and y components.

        Attributes:
            x (float): The x component of the 2D vector.
            y (float): The y component of the 2D vector.
    """
    x: float
    y: float
