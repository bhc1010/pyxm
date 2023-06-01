class Selection:
    def default():
        return Selection(0, 0)
    
    def __init__(self, start: int, end: int):
        self.update(start, end)


    def update(self, start, end):
        self.start = start
        self.end = end

    def shift(self, amount):
        self.start += amount
        self.end += amount