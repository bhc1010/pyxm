class Selection:
    """
    Represents a selection range between two positions in a sequence.

    The Selection class is used to represent a range between two positions (start and end) in a sequence, such as a
    string or a list. It provides methods to update the selection range and to shift the selection by a specified amount.

    Attributes:
        start (int): The starting index of the selection range.
        end (int): The ending index (exclusive) of the selection range.
    """

    @staticmethod
    def default():
        """
        Create a new Selection instance with default start and end positions.

        Returns:
            Selection: A Selection instance with start and end positions set to 0.
        """
        return Selection(0, 0)

    def __init__(self, start: int, end: int):
        """
        Initialize a Selection instance with the given start and end positions.

        Args:
            start (int): The starting index of the selection range.
            end (int): The ending index (exclusive) of the selection range.
        """
        self.update(start, end)

    def update(self, start: int, end: int):
        """
        Update the selection with new start and end positions.

        Args:
            start (int): The starting index of the selection range.
            end (int): The ending index (exclusive) of the selection range.
        """
        self.start = start
        self.end = end

    def shift(self, amount: int):
        """
        Shift the selection range by a specified amount.

        Args:
            amount (int): The amount to shift the selection range. A positive value will move the selection to the right,
                          and a negative value will move it to the left.
        """
        self.start += amount
        self.end += amount
