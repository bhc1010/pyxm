from core.tasksetdata import TaskSetData

class ImageData:
    """
        Class representing image parameters for a Scanning Tunneling Microscope (STM) topography image.

        This class extracts relevant image-related data from a TaskSetData object,
        such as size, offsets, bias, set point, line time, lines per frame, and repetitions,
        which are essential for generating STM topography images.

        Attributes:
            size (float): The size of the image in meters, representing the area to be scanned.
            x_offset (float): The offset in the x-axis direction in meters, defining the starting position in the horizontal direction.
            y_offset (float): The offset in the y-axis direction in meters, defining the starting position in the vertical direction.
            bias (ExponentialNumber): The bias voltage applied during the STM imaging process.
            set_point (ExponentialNumber): The desired set point current during STM imaging.
            line_time (ExponentialNumber): The time taken to scan a single line in the image, influencing the scan speed.
            lines_per_frame (int): The number of lines in a single frame of the image, determining the image resolution.
            repetitions (int): The number of times the image is repeated during scanning to enhance data reliability.

        Note:
            The ImageData class provides an organized representation of the essential parameters
            required for generating Scanning Tunneling Microscope (STM) topography images.
    """

    def __init__(self, data: TaskSetData):
        """
        Initialize the ImageData object with data from TaskSetData.

        Args:
            data (TaskSetData): The TaskSetData object containing information about the image.
        """
        self.size = data.size
        self.x_offset = data.x_offset
        self.y_offset = data.y_offset
        self.bias = data.bias
        self.set_point = data.set_point
        self.line_time = data.line_time
        self.lines_per_frame = data.lines_per_frame
        self.repetitions = data.repetitions
