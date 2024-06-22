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
        txt_format = 'font-family: Times New Roman; font-size: 15px; color: black; background-color: azure'
        # disparity params
        self.disp_layout = QHBoxLayout()
        self.disp_title = QLabel('Disparity')
        self.disp = QLabel('', self)
        self.disp.setStyleSheet(txt_format)
        self.disp_layout.addWidget(self.disp_title)
        self.disp_layout.addWidget(self.disp)
        
        # distance params
        self.distance_layout = QHBoxLayout()
        self.distance_title = QLabel('Distance [cm]')
        self.distance = QLabel('', self)
        self.distance.setStyleSheet(txt_format)
        self.distance_layout.addWidget(self.distance_title)
        self.distance_layout.addWidget(self.distance)
        
        # X params
        self.realX_layout = QHBoxLayout()
        self.realX_title = QLabel('real X [cm]')
        self.realX = QLabel('', self)
        self.realX.setStyleSheet(txt_format)
        self.realX_layout.addWidget(self.realX_title)
        self.realX_layout.addWidget(self.realX)
        
        # angle Y params
        self.realY_layout = QHBoxLayout()
        self.realY_title = QLabel('real Y [cm]')
        self.realY = QLabel('', self)
        self.realY.setStyleSheet(txt_format)
        self.realY_layout.addWidget(self.realY_title)
        self.realY_layout.addWidget(self.realY)
        
        # real x angle
        self.real_x_angle_layout = QHBoxLayout()
        self.real_x_angle_title = QLabel('real x angle [deg]')
        self.real_x_angle = QLabel('', self)
        self.real_x_angle.setStyleSheet(txt_format)
        self.real_x_angle_layout.addWidget(self.real_x_angle_title)
        self.real_x_angle_layout.addWidget(self.real_x_angle)
        
        # real y angle
        self.real_y_angle_layout = QHBoxLayout()
        self.real_y_angle_title = QLabel('real y angle [deg]')
        self.real_y_angle = QLabel('', self)
        self.real_y_angle.setStyleSheet(txt_format)
        self.real_y_angle_layout.addWidget(self.real_y_angle_title)
        self.real_y_angle_layout.addWidget(self.real_y_angle)
        
    def setUI(self):
        # set each layouts
        self.setLayouts()
        
        self.layout.addLayout(self.disp_layout)
        self.layout.addLayout(self.distance_layout)
        self.layout.addLayout(self.realX_layout)
        self.layout.addLayout(self.realY_layout)
        self.layout.addLayout(self.real_x_angle_layout)
        self.layout.addLayout(self.real_y_angle_layout)
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
        self.realX.setText(str(self.th.realX))
        self.realY.setText(str(self.th.realY))
        self.real_x_angle.setText(str(self.th.real_x_angle))
        self.real_y_angle.setText(str(self.th.real_y_angle))
