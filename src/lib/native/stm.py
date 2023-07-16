import time, os
import socket

from core.vector2 import Vector2

class STM():
    """
        Represents an STM (Scanning Tunneling Microscope) controller.

        This class provides an interface to control an STM device over a TCP/IP connection. It allows communication with the STM device to execute various procedures and set parameters.

        Attributes:
            _buffer_size (int): The buffer size used for receiving data from the STM device over the socket.
            ip (str): The IP address of the STM device.
            port (int): The port number for the TCP/IP connection to the STM device.
            socket (socket.socket): The socket object used for communication with the STM device.

        Methods:
            __init__(self, ip: str = '127.0.0.1', port: int = 12600): Initializes the STM instance.
            connect(self): Establishes a TCP/IP connection with the STM device.
            drop(self): Closes the TCP/IP connection with the STM device.
            send(self, msg: str, out_dtype: type = str): Sends a message to the STM device and receives the response.
            start_procedure(self, procedure_name: str): Starts an STM procedure by its name.
            set_bias(self, bias: float): Sets the STM bias value.
            set_scan_size(self, size: float): Sets the scan area size.
            set_scan_pos(self, pos: Vector2): Sets the scan area position.
            set_scan_count(self, scan_count:int): Sets the number of scans to be performed.
            get_save_path(self): Retrieves the save path for the measurement data from the STM device.
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

    def connect(self):
        """
            Establishes a TCP/IP connection with the STM device.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def drop(self):
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
        """
        self.connect()
        time.sleep(0.01)
        self.socket.send(msg.encode())
        result = self.socket.recv(STM._buffer_size).decode()

        try:
            out = out_dtype(result)
        except:
            result = self.socket.recv(STM._buffer_size).decode()
            out = out_dtype(result)

        self.drop()
        return out
    
    def start_procedure(self, procedure_name: str):
        """
            Starts an STM procedure by its name.

            Args:
                procedure_name (str): The name of the procedure to be started.

            Returns:
                str: The result of the STM procedure.
        """
        cmd = f'StartProcedure, {procedure_name}\n'
        return self.send(cmd)

    def set_bias(self, bias: float):
        """
            Sets the STM bias value.

            Args:
                bias (float): The bias value to be set.

            Returns:
                str: The response from the STM device after setting the bias value.
        """
        cmd = f'SetSWParameter, STM Bias, Value, {bias}\n'
        result = self.send(cmd)

        while 'Done' not in str(result):
            result = self.send(cmd)

        return result
    
    def set_setpoint(self, setpoint: float):
        cmd = f'SetSWParameter, STM Set Point, Value, {setpoint}\n'
        return self.send(cmd)

    def set_scan_size(self, size: float):
        """
            Sets the scan area size.

            Args:
                size (float): The size of the scan area to be set.

            Returns:
                str: The response from the STM device after setting the scan area size.
        """
        cmd = f'SetSWParameter, Scan Area Window, Scan Area Size, {size}'
        return self.send(cmd)

    def set_scan_pos(self, pos: Vector2):
        """
            Sets the scan area position.

            Args:
                pos (Vector2): The position of the scan area to be set.

            Returns:
                str: The response from the STM device after setting the scan area position.
        """
        cmd = f'SetSWParameter, Scan Area Window, X Offset, {pos.x}'
        self.send(cmd)
        cmd = f'SetSWParameter, Scan Area Window, Y Offset, {pos.y}'
        return self.send(cmd)

    def set_line_time(self, line_time: float):
        cmd = f'SetSWParameter, Scan Area Window, Line Time, {line_time}'
        return self.send(cmd)
    
    def set_lines_per_frame(self, lines_per_frame: int):
        cmd = f'SetSWParameter, Scan Area Window, Scan Settings, Lines Per Frame, {lines_per_frame}'
        return self.send(cmd)

    def set_scan_count(self, scan_count:int):
        """
            Sets the number of scans to be performed.

            Args:
                scan_count (int): The number of scans to be set.

            Returns:
                str: The response from the STM device after setting the scan count.
        """
        cmd = f'SetSWSubItemParameter, Scan Area Window, Scan Settings, Scan Count, {scan_count}\n'
        return self.send(cmd)
    
    def get_save_path(self):
        """
            Retrieves the save path for the measurement data from the STM device.

            Returns:
                str: The save path for the measurement data.
        """
        cmd = "GetSWSubItemParameter, Scan Area Window, MeasureSave, Save Path\n"
        return os.path.normpath(self.send(cmd, str))
