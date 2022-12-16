import numpy as np

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import QTimer

class LeftWidget(QWidget):
    def __init__(self, parent=None, th = None):
        super(LeftWidget, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.cur_fps = 0
        self.th = th
        self.setUI()
        self.UpDate()
        
    def setUI(self):
    
        # x0 params
        self.x0_layout = QHBoxLayout()
        self.x0_title = QLabel('X0')
        self.x0 = QLabel('', self)
        self.x0.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.x0_layout.addWidget(self.x0_title)
        self.x0_layout.addWidget(self.x0)
        
        # distance params
        self.distance_layout = QHBoxLayout()
        self.distance_title = QLabel('Distance')
        self.distance = QLabel('', self)
        self.distance.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.distance_layout.addWidget(self.distance_title)
        self.distance_layout.addWidget(self.distance)
        
        # angle params
        self.angle_layout = QHBoxLayout()
        self.angle_title = QLabel('Angle')
        self.angle = QLabel('', self)
        self.angle.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.angle_layout.addWidget(self.angle_title)
        self.angle_layout.addWidget(self.angle)
        
        self.layout.addLayout(self.x0_layout)
        self.layout.addLayout(self.distance_layout)
        self.layout.addLayout(self.angle_layout)
        # スペーシング
        spc = QSpacerItem(100, 100, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addSpacerItem(spc)

        # 自身のレイアウトとして設定
        self.setLayout(self.layout)
           
    def UpDate(self):
        """Initialize camera.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot_bar)
        self.timer.start(30)
        
    def plot_bar(self):
        self.x0.setText(str(self.th.x0))
        self.distance.setText(str(self.th.distance))
        self.angle.setText(str(self.th.angle))
