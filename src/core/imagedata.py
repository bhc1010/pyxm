from core.tasksetdata import TaskSetData

class ImageData:
    def __init__(self, data: TaskSetData):
        self.size = data.size
        self.x_offset = data.x_offset
        self.y_offset = data.y_offset
        self.bias = data.bias
        self.set_point = data.set_point
        self.line_time = data.line_time
        self.lines_per_frame = data.lines_per_frame
        self.repetitions = data.repetitions