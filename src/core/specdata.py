from dataclasses import dataclass
from enum import Enum

@dataclass
class SpecData:
    """
    Data class for Scanning Tunneling Spectroscopy (STS) parameters.

    The SpecData class is a data class that holds the parameters related to Scanning Tunneling Spectroscopy (STS),
    including the mode (e.g., Point, Line, Region), start, stop, step, and delay_time.

    Attributes:
        mode (SpecMode): The Spectroscopy mode, which can be one of the values from the SpecMode enum (e.g., Point, Line, Region).
        start (float): The starting value for the STS measurement.
        stop (float): The stopping value for the STS measurement.
        step (float): The step size between successive STS measurements.
        delay_time (float): The delay time between STS measurements (in seconds).
    """

    SpecMode = Enum('SpecMode', ['Point', 'Line', 'Region'])
    """
    Enumeration for the different modes of Scanning Tunneling Spectroscopy (STS).

    The SpecMode enumeration defines the possible modes for performing Scanning Tunneling Spectroscopy (STS),
    which include Point, Line, and Region modes.
    """

    mode: SpecMode
    start: float
    stop: float
    step: float
    delay_time: float
