from PySide6.QtCore import *

import time

class TaskWorker(QRunnable):
    """
    Worker thread for STM tasks
    """

    @Slot()
    def run(self):
        print(f"Thread start on {QThread.currentThread()}")
        time.sleep(5)
        print("Thread complete")