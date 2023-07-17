import time, os
import socket

from core.vector2 import Vector2

class STM():
    """
        Represents an STM (Scanning Tunneling Microscope) controller.

        This class provides an interface to control an STM device over a TCP/IP connection.
        It allows communication with the STM device to execute various procedures and set parameters.

        Attributes:
            _buffer_size (int): The buffer size used for receiving data from the STM device over the socket.
            ip (str): The IP address of the STM device.
            port (int): The port number for the TCP/IP connection to the STM device.
            socket (socket.socket): The socket object used for communication with the STM device.

        Methods:
            __init__(self, ip: str = '127.0.0.1', port: int = 12600): Initializes the STM instance.
            connect(self): Establishes a TCP/IP connection with the STM device.
            drop(self): Closes the TCP/IP connection with the STM device.
            send(self, msg: str, out_dtype: type = str) -> out_dtype: Sends a message to the STM device and receives the response.
            start_procedure(self, procedure_name: str) -> str: Starts an STM procedure by its name.
            set_bias(self, bias: float) -> str: Sets the STM bias value.
            set_scan_size(self, size: float) -> str: Sets the scan area size.
            set_scan_pos(self, pos: Vector2) -> str: Sets the scan area position.
            set_scan_count(self, scan_count:int) -> str: Sets the number of scans to be performed.
            get_save_path(self) -> str: Retrieves the save path for the measurement data from the STM device.
    """

    _buffer_size = 1024

    def __init__(self, ip: str = '127.0.0.1', port: int = 12600):
        """
            Initializes the STM instance.

            Args:
                ip (str): The IP address of the STM device. Default is '127.0.0.1'.
                port (int): The port number for the TCP/IP connection to the STM device. Default is 12600.
        """
        self.ip = ip
        self.port = port
        self.socket = None

    def connect(self) -> None:
        """
            Establishes a TCP/IP connection with the STM device.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def drop(self) -> None:
        """
            Closes the TCP/IP connection with the STM device.
        """
        self.socket.close()

    def send(self, msg: str, out_dtype: type = str):
        """
            Sends a message to the STM device and receives the response.

            Args:
                msg (str): The message to be sent to the STM device.
                out_dtype (type): The data type of the expected output. Default is 'str'.

            Returns:
                out_dtype: The response from the STM device with the specified data type.

            This method sends a message to the STM device and waits for a response. The response is converted to the specified data type, 
            which is 'str' by default. If the conversion fails, the method attempts to receive the response again and tries the conversion 
            once more. The method then returns the converted response.
        """
        self.connect()
        time.sleep(0.1)
        self.socket.send(msg.encode())
        result = self.socket.recv(STM._buffer_size).decode()

        try:
            out = out_dtype(result)
        except:
            result = self.socket.recv(STM._buffer_size).decode()
            out = out_dtype(result)

        self.drop()
        return out

    def start_procedure(self, procedure_name: str) -> str:
        """
            Starts an STM procedure by its name.

            Args:
                procedure_name (str): The name of the procedure to be started.

            Returns:
                str: The result of the STM procedure.

            This method initiates the specified STM procedure by sending a command to the STM device with the given procedure name.
            The response from the STM device, if available, is returned as a string.
        """
        cmd = f'StartProcedure, {procedure_name}\n'
        print("Starting procedure")
        result = self.send(cmd)
        print(result)
        return result

    def set_bias(self, bias: float) -> str:
        """
            Sets the STM bias value.

            Args:
                bias (float): The bias value to be set.

            Returns:
                str: The response from the STM device after setting the bias value.

            This method sets the bias voltage value on the STM device by sending a command with the specified bias value.
            The method will continue to attempt to set the bias until the response from the STM device includes the word 'Done'.
            The response indicating that the operation is successful will be returned as a string.

            If the response does not contain 'Done', it means the operation may not have been completed yet, and the method will
            keep retrying until the 'Done' response is received or a timeout occurs.

            Note: It is recommended to set an appropriate timeout value when calling this method to avoid infinite retries
            in case of communication issues with the STM device.
        """
        cmd = f'SetSWParameter, STM Bias, Value, {bias}\n'
        result = self.send(cmd)

        while 'Done' not in str(result):
            result = self.send(cmd)

        return result

    def set_scan_size(self, size: float) -> str:
        """
        Sets the scan area size.

        Args:
            size (float): The size of the scan area to be set.

        Returns:
            str: The response from the STM device after setting the scan area size.

        This method sets the scan area size on the STM device by sending a command with the specified size value.
        The method waits for the STM device to acknowledge the operation and returns the response as a string.
        """
        cmd = f'SetSWParameter, Scan Area Window, Scan Area Size, {size}'
        return self.send(cmd)

    def set_scan_pos(self, pos: Vector2) -> str:
        """
            Sets the scan area position.

            Args:
                pos (Vector2): The position of the scan area to be set.

            Returns:
                str: The response from the STM device after setting the scan area position.

            This method sets the scan area position on the STM device by sending commands with the specified position values (x and y).
            The method waits for the STM device to acknowledge the operations and returns the response as a string.
        """
        cmd = f'SetSWParameter, Scan Area Window, X Offset, {pos.x}'
        self.send(cmd)
        cmd = f'SetSWParameter, Scan Area Window, Y Offset, {pos.y}'
        return self.send(cmd)

    def set_line_time(self, line_time: float) -> str:
        """
            Sets the time taken to acquire one line of data.

            Args:
                line_time (float): The time taken to acquire one line of data.

            Returns:
                str: The response from the STM device after setting the line time.

            This method sets the time taken to acquire one line of data on the STM device by sending a command with the specified line_time value.
            The method waits for the STM device to acknowledge the operation and returns the response as a string.
        """
        cmd = f'SetSWParameter, Scan Area Window, Line Time, {line_time}'
        return self.send(cmd)

    def set_lines_per_frame(self, lines_per_frame: int) -> str:
        """
            Sets the number of lines to be scanned to complete one frame.

            Args:
                lines_per_frame (int): The number of lines to be scanned to complete one frame.

            Returns:
                str: The response from the STM device after setting the lines per frame.

            This method sets the number of lines to be scanned to complete one frame on the STM device 
            by sending a command with the specified lines_per_frame value.
            The method waits for the STM device to acknowledge the operation and returns the response as a string.
        """
        cmd = f'SetSWParameter, Scan Area Window, Scan Settings, Lines Per Frame, {lines_per_frame}'
        return self.send(cmd)

    def set_scan_count(self, scan_count:int) -> str:
        """
            Sets the number of scans to be performed.

            Args:
                scan_count (int): The number of scans to be set.

            Returns:
                str: The response from the STM device after setting the scan count.

            This method sets the number of scans to be performed on the STM device 
            by sending a command with the specified scan_count value.
            The method waits for the STM device to acknowledge the operation and returns the response as a string.
        """
        cmd = f'SetSWSubItemParameter, Scan Area Window, Scan Settings, Scan Count, {scan_count}\n'
        return self.send(cmd)

    def get_save_path(self) -> str:
        """
            Retrieves the save path for the measurement data from the STM device.

            Returns:
                str: The save path for the measurement data.

            This method sends a command to the STM device to retrieve the save path for the measurement data.
            The response containing the save path is returned as a string.
        """
        cmd = "GetSWSubItemParameter, Scan Area Window, MeasureSave, Save Path\n"
        return os.path.normpath(self.send(cmd, str))
