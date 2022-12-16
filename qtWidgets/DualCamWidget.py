import os, sys
import numpy as np
import cv2
import time
from PySide6.QtCore import Slot, QSize
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget)

from qtWidgets.RightVideoTread import Thread

class DualCamWidget(QWidget):
    def __init__(self, parent=None, opt=None):
        super().__init__(parent)
        self.parent = parent
        self.opt = opt
        self.vid_size = opt.vid_size
        self.displayH, self.displayW = opt.vid_size*3, opt.vid_size*3
        
        self.setup_ui()
        self.set_thread(opt)
        self.predictbar.setText('Now Loading')
        
        
    def set_thread(self, opt):
        self.th = Thread(self, opt=opt)
        self.th.updateFrame.connect(self.setImage)
        self.th.updateFrame.connect(self.plot_fps)
        
    def setup_ui(self):
        """Initialize widgets.
        """
        self.set1_widget_layout()
        self.set2_main_layout()
        
    def set1_widget_layout(self):
        # Predicted time bar
        self.predictor_layout = QHBoxLayout()
        self.predictor_title = QLabel('Latency')
        self.predictbar = QLabel('', self)
        self.predictbar.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.predictbar.setFixedSize(QSize(200, 40))
        self.predictor_layout.addWidget(self.predictor_title)
        self.predictor_layout.addWidget(self.predictbar)
        
        # button
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)
        
        # video widget
        self.video_display = QLabel()
        self.video_display.setFixedSize(QSize(self.displayH, self.displayW))
        
    def set2_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.video_display)
        self.main_layout.addWidget(self.start_button)
        self.main_layout.addLayout(self.predictor_layout)
        self.setLayout(self.main_layout)
        
    def plot_fps(self, event):
        self.predictbar.setText(str(self.th.pred_time*1000)+"[ms]")
 
    def return_thread(self):
        return self.th
        
    @Slot()
    def start(self):
        print("Starting...")
        self.th.start()
        
    @Slot(QImage)
    def setImage(self, image):
        self.video_display.setPixmap(QPixmap.fromImage(image))
   
