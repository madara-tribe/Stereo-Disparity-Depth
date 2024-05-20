from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import QTimer

class ImgLeftWidget(QWidget):
    def __init__(self, parent=None, th = None):
        super(ImgLeftWidget, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.cur_fps = 0
        self.th = th
        self.setUI()
        self.UpDate()
       
    def setLayouts(self):
        # disparity params
        self.disp_layout = QHBoxLayout()
        self.disp_title = QLabel('Disparity')
        self.disp = QLabel('', self)
        self.disp.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.disp_layout.addWidget(self.disp_title)
        self.disp_layout.addWidget(self.disp)
        
        # distance params
        self.distance_layout = QHBoxLayout()
        self.distance_title = QLabel('Distance [cm]')
        self.distance = QLabel('', self)
        self.distance.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.distance_layout.addWidget(self.distance_title)
        self.distance_layout.addWidget(self.distance)
        
        # angle X params
        self.angleX_layout = QHBoxLayout()
        self.angleX_title = QLabel('Angle X [deg]')
        self.angleX = QLabel('', self)
        self.angleX.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.angleX_layout.addWidget(self.angleX_title)
        self.angleX_layout.addWidget(self.angleX)
        
        # angle Y params
        self.angleY_layout = QHBoxLayout()
        self.angleY_title = QLabel('Angle Y [deg]')
        self.angleY = QLabel('', self)
        self.angleY.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.angleY_layout.addWidget(self.angleY_title)
        self.angleY_layout.addWidget(self.angleY)
        
    def setUI(self):
        # set each layouts
        self.setLayouts()
        
        self.layout.addLayout(self.disp_layout)
        self.layout.addLayout(self.distance_layout)
        self.layout.addLayout(self.angleX_layout)
        self.layout.addLayout(self.angleY_layout)
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
        self.disp.setText(str(self.th.disparity))
        self.distance.setText(str(self.th.distance))
        self.angleX.setText(str(self.th.angleX))
        self.angleY.setText(str(self.th.angleY))
