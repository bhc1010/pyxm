import time, os
import socket

from core.vector2 import Vector2

class STM():
    _buffer_size = 1024

    def __init__(self, ip: str = '127.0.0.1', port: int = 12600):
        self.ip = ip
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.port))

    def drop(self):
        self.socket.close()

    def send(self, msg: str, out_dtype: type = str):
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
        cmd = f'StartProcedure, {procedure_name}\n'
        return self.send(cmd)

    def set_bias(self, bias: float):
        cmd = f'SetSWParameter, STM Bias, Value, {bias}\n'
        result = self.send(cmd)

        while 'Done' not in str(result):
            result = self.send(cmd)

        return result

    def set_scan_size(self, size: float):
        cmd = f'SetSWParameter, Scan Area Window, Scan Area Size, {size}'
        return self.send(cmd)

    def set_scan_pos(self, pos: Vector2):
        cmd = f'SetSWParameter, Scan Area Window, X Offset, {pos.x}'
        self.send(cmd)
        cmd = f'SetSWParameter, Scan Area Window, Y Offset, {pos.y}'
        return self.send(cmd)

    def set_scan_count(self, scan_count:int):
        cmd = f'SetSWSubItemParameter, Scan Area Window, Scan Settings, Scan Count, {scan_count}\n'
        return self.send(cmd)
    
    def get_time_remaining(self):
        now = time.time()

        cmd = "GetSWSubItemParameter, Scan Area Window, Scan Settings, Lines Per Frame\n"
        Lines = self.send(cmd, float)

        cmd = "GetSWParameter, Scan Area Window, Line Time\n"
        LineTime = self.send(cmd, float)

        cmd = "GetSWSubItemParameter, Scan Area Window, Scan Settings, Over Scan Count\n"
        OverScanCount = self.send(cmd, float)

        ScanTime = 2*(Lines+OverScanCount)*LineTime

        return now + ScanTime

    def get_save_path(self):
        cmd = "GetSWSubItemParameter, Scan Area Window, MeasureSave, Save Path\n"
        return os.path.normpath(self.send(cmd, str))