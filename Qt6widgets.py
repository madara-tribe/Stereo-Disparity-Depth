import cv2
import numpy as np
import matplotlib.pyplot as plt

from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QInputDialog
from PySide6.QtCore import QSize
from PySide6.QtGui import QImage, QPixmap
from utils import cal_disparity, add_color


class second_window(QWidget):
    def __init__ (self, opt):
        print ("start")
        QWidget.__init__(self)
        self.numDisparities = opt.numDisparities
        self.blockSize = opt.blockSize
        self.opt = opt
        self.cv2_is = True
        entire_layout = QHBoxLayout()
        
        # rught
        self.canvas_ui()
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.canvas)
        
        # left
        click_layout = QVBoxLayout()
        self.button_ui()
        click_layout.addWidget(self.pybutton)
        click_layout.addWidget(self.AnalizeButton)
        click_layout.addLayout(self.pb_num1_layout)
        click_layout.addLayout(self.pb_num2_layout)
        entire_layout.addLayout(click_layout)
        entire_layout.addLayout(right_layout)
        self.setLayout(entire_layout)
        
        
    def canvas_ui(self):
        self.video_size = QSize(640, 480)
        self.canvas = QLabel()
        self.canvas.setFixedSize(self.video_size)
    
        
    def button_ui(self):
        self.pybutton = QPushButton('Calcurate disparity', self)
        self.pybutton.clicked.connect(self.clickMethod)
        
        self.AnalizeButton = QPushButton('Pixel Analize', self)
        self.AnalizeButton.clicked.connect(self.analyzeClick)
        txt_format = 'font-family: Times New Roman; font-size: 15px; color: black; background-color: azure'
        
        ## 1
        self.pb_num1_layout = QHBoxLayout()
        self.pb_num1 = QPushButton('numDisparities')
        self.pb_num1.setFixedSize(120, 60) # size
        self.pb_num1.clicked.connect(self.show_dialog_num1)
        self.pb_num1_txt = QLabel('', self)
        self.pb_num1_txt.setStyleSheet(txt_format)
        self.pb_num1_layout.addWidget(self.pb_num1)
        self.pb_num1_layout.addWidget(self.pb_num1_txt)
        
       
        # 2
        self.pb_num2_layout = QHBoxLayout()
        self.pb_num2 = QPushButton('blockSize')
        self.pb_num2.setFixedSize(120, 60) # size
        self.pb_num2.clicked.connect(self.show_dialog_num2)
        self.pb_num2_txt = QLabel('', self)
        self.pb_num2_txt.setStyleSheet(txt_format)
        self.pb_num2_layout.addWidget(self.pb_num2)
        self.pb_num2_layout.addWidget(self.pb_num2_txt)
        
        
    def analyzeClick(self):
        Llab = cv2.imread(self.opt.lpath)
        Llab = cv2.cvtColor(Llab, cv2.COLOR_BGR2LAB)
        # surface map
        plt.figure(3)
        ax = plt.axes(projection='3d')
        y = range(Llab.shape[0])
        x = range(Llab.shape[1])
        X, Y = np.meshgrid(x, y)
        ax.plot_surface(X, Y, Llab[:,:,0])
        plt.show()
        
    def clickMethod(self):
        imgL = cv2.imread(self.opt.lpath, cv2.IMREAD_GRAYSCALE)#/255
        imgR = cv2.imread(self.opt.rpath, cv2.IMREAD_GRAYSCALE)#/255
        print(imgR.shape, imgR.max(), imgR.min())
        if self.cv2_is:
            stereo = cv2.StereoBM_create(numDisparities=self.numDisparities, blockSize=self.blockSize)
            disp = stereo.compute(imgL,imgR)
            h_, w_ = disp.shape[:2]
            disp = cv2.resize(disp, (int(w_/2), int(h_/2)))
        else:
            h_, w_ = imgR.shape[:2]
            imgL = cv2.resize(imgL, (int(w_/2), int(h_/2)))
            imgR = cv2.resize(imgR, (int(w_/2), int(h_/2)))
            disp = cal_disparity(imgL, imgR, self.blockSize)
        print(disp.shape, disp.max(), disp.min())
        disp = add_color(disp)
        image = QImage(disp, disp.shape[1], disp.shape[0],
                    disp.strides[0], QImage.Format_RGB888)
        self.canvas.setPixmap(QPixmap.fromImage(image))

    def show_dialog_num1(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'numDisparities:')
        self.numDisparities= value
        self.pb_num1_txt.setText(str(self.numDisparities))
        
    def show_dialog_num2(self):
        value, r = QInputDialog.getInt(self, 'Input dialog', 'blockSize:')
        self.blockSize = value
        self.pb_num2_txt.setText(str(self.blockSize))
