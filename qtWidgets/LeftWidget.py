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
    
        # FPS bar
        self.fps_layout = QHBoxLayout()
        self.fps_title = QLabel('Normal FPS')
        self.fps = QLabel('', self)
        self.fps.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')

        self.fps_layout.addWidget(self.fps_title)
        self.fps_layout.addWidget(self.fps)
        self.layout.addLayout(self.fps_layout)

        # スペーシング
        spc = QSpacerItem(16, 16, QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.fps.setText(str(self.th.pred_time))
