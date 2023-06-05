# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QComboBox, QFrame, QMainWindow,
    QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from native.scanarea import ScanArea
from native.scientificspinbox import ScientificSpinBox
from native.tasklist import TaskList
from native.task import Task
from native.togglebutton import ToggleButton
import qtawesome as fa

from core.exponentialnumber import ExponentialNumber
from core.taskdata import TaskData
from core.specdata import SpecData
from datetime import datetime

class Ui_MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ## ------ Window Settings ------ ##
        self.setWindowTitle("STM Automator")
        self.resize(1400, 800)
        self.centralwidget = QWidget(self)

        ## ------ Toolbar ------ ##
        self.toolbar = QFrame(self.centralwidget, objectName='toolbar')
        self.toolbar.setFixedHeight(26)

        self.menu = ToggleButton(objectName='bars')
        self.left_space = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.play = ToggleButton(objectName='play')
        self.pause = ToggleButton(objectName='pause')
        self.stop = ToggleButton(objectName='stop')
        self.right_space = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.settings = ToggleButton(objectName='cog')

        self.menu.setCheckable(False)
        self.settings.setCheckable(False)

        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar_layout.setSpacing(0)
        self.toolbar_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_layout.addWidget(self.menu)
        self.toolbar_layout.addItem(self.left_space)
        self.toolbar_layout.addWidget(self.play)
        self.toolbar_layout.addWidget(self.pause)
        self.toolbar_layout.addWidget(self.stop)
        self.toolbar_layout.addItem(self.right_space)
        self.toolbar_layout.addWidget(self.settings)

        ## ---------- Content ----------##
        self.content = QFrame(self.centralwidget, objectName="content_frame")

        ## Scan Area
        self.scan_area_frame = QFrame(self.content, objectName="scan_area_frame")
        self.scan_area_frame.setMinimumWidth(500)
        
        self.scan_area = ScanArea(self.scan_area_frame)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHeightForWidth(True)
        self.scan_area.setSizePolicy(sizePolicy)

        self.scan_area_layout = QGridLayout(self.scan_area_frame)
        self.scan_area_layout.setContentsMargins(0, 7, 0, 0)
        self.scan_area_layout.addWidget(self.scan_area, 0, 0, 1, 1)

        ## Options
        self.options_frame = QFrame(self.content, objectName="options_frame")
        self.options_frame.setMinimumWidth(350)
        self.options_frame.setMaximumWidth(375)

        # Scan Options
        self.scan_options = QGroupBox("Image Options")
        self.scan_options.setFlat(True)
        self.scan_options.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lines_per_frame_label = QLabel("Lines per frame")
        self.lines_per_frame = QComboBox()
        self.lines_per_frame.addItems([f'{2**n}' for n in range(3, 13)])
        self.lines_per_frame.setCurrentIndex(5)
        self.lines_per_frame.setFixedWidth(150)

        self.scan_size_label = QLabel("Size")
        self.scan_size = ScientificSpinBox()
        self.scan_size.setBounds(lower=ExponentialNumber(2.5, -12), upper=ExponentialNumber(3, -6))
        self.scan_size.setValue(ExponentialNumber(100, -9))
        self.scan_size.setUnits('m')

        self.x_offset_label = QLabel("X offset")
        self.x_offset = ScientificSpinBox()
        self.x_offset.setBounds(lower=ExponentialNumber(-1.5, -6), upper=ExponentialNumber(1.5, -6))
        self.x_offset.setValue(ExponentialNumber(0, -9))
        self.x_offset.setUnits('m')

        self.y_offset_label = QLabel("Y offset")
        self.y_offset = ScientificSpinBox()
        self.y_offset.setBounds(lower=ExponentialNumber(-1.5, -6), upper=ExponentialNumber(1.5, -6))
        self.y_offset.setValue(ExponentialNumber(0, -9))
        self.y_offset.setUnits('m')

        self.scan_speed_label = QLabel("Scan speed")
        self.scan_speed = ScientificSpinBox()
        self.scan_speed.setBounds(lower=ExponentialNumber(2.5, -12), upper=ExponentialNumber(1, -6))
        self.scan_speed.setValue(ExponentialNumber(100, -9))
        self.scan_speed.setUnits('m/s')

        self.line_time_label = QLabel("Line time")
        self.line_time = ScientificSpinBox()
        self.line_time.setBounds(lower=ExponentialNumber(2.5, -12), upper=ExponentialNumber(1000, 0))
        self.line_time.setValue(ExponentialNumber(1, 0))
        self.line_time.setUnits('s')

        self.scan_options_layout = QGridLayout()
        self.scan_options_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.scan_options_layout.setHorizontalSpacing(6)
        self.scan_options_layout.addWidget(self.lines_per_frame_label, 0, 0, 1, 1)
        self.scan_options_layout.addWidget(self.lines_per_frame, 0, 1, 1, 1)
        self.scan_options_layout.addWidget(self.scan_size_label, 1, 0, 1, 1)
        self.scan_options_layout.addWidget(self.scan_size, 1, 1, 1, 1)
        self.scan_options_layout.addWidget(self.x_offset_label, 2, 0, 1, 1)
        self.scan_options_layout.addWidget(self.x_offset, 2, 1, 1, 1)
        self.scan_options_layout.addWidget(self.y_offset_label, 3, 0, 1, 1)
        self.scan_options_layout.addWidget(self.y_offset, 3, 1, 1, 1)
        self.scan_options_layout.addWidget(self.scan_speed_label, 4, 0, 1, 1)
        self.scan_options_layout.addWidget(self.scan_speed, 4, 1, 1, 1)
        self.scan_options_layout.addWidget(self.line_time_label, 5, 0, 1, 1)
        self.scan_options_layout.addWidget(self.line_time, 5, 1, 1, 1)
        self.scan_options.setLayout(self.scan_options_layout)

        # Voltage Options
        self.voltage_options = QGroupBox("Voltage Options", self.options_frame)
        self.voltage_options.setFlat(True)

        self.start_voltage_label = QLabel("Start voltage", self.voltage_options)
        self.start_voltage = ScientificSpinBox()
        self.start_voltage.setBounds(lower=ExponentialNumber(-5, 0), upper=ExponentialNumber(5, 0))
        self.start_voltage.setValue(ExponentialNumber(200, -3))
        self.start_voltage.setUnits('V')

        self.stop_voltage_label = QLabel("Stop voltage", self.voltage_options)
        self.stop_voltage = ScientificSpinBox()
        self.stop_voltage.setBounds(lower=ExponentialNumber(-5, 0), upper=ExponentialNumber(5, 0))
        self.stop_voltage.setValue(ExponentialNumber(1, 0))
        self.stop_voltage.setUnits('V')

        self.step_voltage_label = QLabel("Step voltage", self.voltage_options)
        self.step_voltage = ScientificSpinBox()
        self.step_voltage.setBounds(lower=ExponentialNumber(-5, 0), upper=ExponentialNumber(5, 0))
        self.step_voltage.setValue(ExponentialNumber(100, -3))
        self.step_voltage.setUnits('V')

        self.voltage_options_layout = QGridLayout()
        self.voltage_options_layout.addWidget(self.start_voltage_label, 0, 0, 1, 1)
        self.voltage_options_layout.addWidget(self.start_voltage, 0, 1, 1, 1)
        self.voltage_options_layout.addWidget(self.stop_voltage_label, 1, 0, 1, 1)
        self.voltage_options_layout.addWidget(self.stop_voltage, 1, 1, 1, 1)
        self.voltage_options_layout.addWidget(self.step_voltage_label, 2, 0, 1, 1)
        self.voltage_options_layout.addWidget(self.step_voltage, 2, 1, 1, 1)
        self.voltage_options.setLayout(self.voltage_options_layout)

        self.sts_options = QGroupBox("Spectroscopy Options", self.options_frame)
        self.sts_options.setFlat(True)

        self.sts_mode_label = QLabel("Spectroscopy mode", self.sts_options)
        self.sts_mode = QComboBox(self.sts_options)
        self.sts_mode.addItems(["Point Spectroscopy", "Spec on a Line", "All"])

        self.sts_start_voltage_label = QLabel("Start voltage", self.sts_options)
        self.sts_start_voltage = ScientificSpinBox()
        self.sts_start_voltage.setBounds(lower=ExponentialNumber(-5, 0), upper=ExponentialNumber(5, 0))
        self.sts_start_voltage.setValue(ExponentialNumber(-1, 0))
        self.sts_start_voltage.setUnits('V')

        self.sts_stop_voltage_label = QLabel("Stop voltage", self.sts_options)
        self.sts_stop_voltage = ScientificSpinBox()
        self.sts_stop_voltage.setBounds(lower=ExponentialNumber(-5, 0), upper=ExponentialNumber(5, 0))
        self.sts_stop_voltage.setValue(ExponentialNumber(1, 0))
        self.sts_stop_voltage.setUnits('V')

        self.sts_step_voltage_label = QLabel("Step voltage", self.sts_options)
        self.sts_step_voltage = ScientificSpinBox()
        self.sts_step_voltage.setBounds(lower=ExponentialNumber(-5, 0), upper=ExponentialNumber(5, 0))
        self.sts_step_voltage.setValue(ExponentialNumber(25, -3))
        self.sts_step_voltage.setUnits('V')

        self.sts_options_layout = QGridLayout()
        self.sts_options_layout.addWidget(self.sts_mode_label, 0, 0, 1, 1)
        self.sts_options_layout.addWidget(self.sts_mode, 0, 1, 1, 1)
        self.sts_options_layout.addWidget(self.sts_start_voltage_label, 1, 0, 1, 1)
        self.sts_options_layout.addWidget(self.sts_start_voltage, 1, 1, 1, 1)
        self.sts_options_layout.addWidget(self.sts_stop_voltage_label, 2, 0, 1, 1)
        self.sts_options_layout.addWidget(self.sts_stop_voltage, 2, 1, 1, 1)
        self.sts_options_layout.addWidget(self.sts_step_voltage_label, 3, 0, 1, 1)
        self.sts_options_layout.addWidget(self.sts_step_voltage, 3, 1, 1, 1)
        self.sts_options.setLayout(self.sts_options_layout)

        # Add task
        self.options_spacing = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.task_name = QLineEdit(self.options_frame, objectName="task_name")
        self.add_task_btn = QPushButton("Add Task", self.options_frame, objectName="add_task_btn")

        # Options layout
        self.options_frame_layout = QVBoxLayout(self.options_frame)
        self.options_frame_layout.setSpacing(2)
        self.options_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.options_frame_layout.addWidget(self.scan_options)
        self.options_frame_layout.addWidget(self.voltage_options)
        self.options_frame_layout.addWidget(self.sts_options)
        self.options_frame_layout.addItem(self.options_spacing)
        self.options_frame_layout.addWidget(self.task_name)
        self.options_frame_layout.addWidget(self.add_task_btn)

        ## Task List
        self.task_list = TaskList(title="Task List", objectName='task_list')
        self.task_list.setMinimumWidth(300)
        self.task_list.setMaximumWidth(525)
        
        self.content_layout = QHBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.addWidget(self.scan_area_frame)
        self.content_layout.addWidget(self.options_frame)
        self.content_layout.addWidget(self.task_list)
        self.content_layout.setSpacing(10)

        self.window_layout = QVBoxLayout(self.centralwidget)
        self.window_layout.addWidget(self.toolbar)
        self.window_layout.addWidget(self.content)

        self.setCentralWidget(self.centralwidget)
        self.setup_connections()

    def setup_connections(self):
        self.add_task_btn.clicked.connect(self.add_task)
        self.task_name.returnPressed.connect(self.add_task)

    def add_task(self):
        task_data = TaskData(name=self.task_name.text(),
                             date=datetime.now(),
                             time_to_finish=0,
                             lines_per_frame=int(self.lines_per_frame.currentText()),
                             size=self.scan_size.value.to_float(),
                             x_offset=self.x_offset.value.to_float(),
                             y_offset=self.y_offset.value.to_float(),
                             scan_speed=self.scan_speed.value.to_float(),
                             line_time=self.line_time.value.to_float(),
                             start_voltage=self.start_voltage.value.to_float(),
                             stop_voltage=self.stop_voltage.value.to_float(),
                             step_voltage=self.step_voltage.value.to_float())
        task = Task(self.task_name.text(), data=task_data)
        task.adjustTextWidth()
        self.task_list.add_task(task)
