import time
import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage

class Thread(QThread):
    updateFrame = Signal(QImage)
    def __init__(self, parent=None, opt=None):
        QThread.__init__(self, parent)
        self.opt = opt
        self.capR = cv2.VideoCapture(opt.rvid_path)
        self.capL = cv2.VideoCapture(opt.lvid_path)
        self.pred_time = 0
        self.vid_side = opt.vid_size
        
    def openCV2Qimage(self, cvImage):
        resizedW, resizedW = self.vid_side*2, self.vid_side
        cvImage = cv2.resize(cvImage, (self.vid_side*2, self.vid_side))
        height, width, channel = cvImage.shape
        bytesPerLine = channel * width
        cvImageRGB = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        image = QImage(cvImageRGB, width, height, bytesPerLine, QImage.Format_RGB888)
        return image
    
    def run(self):
        """Read frame from camera and repaint QLabel widget.
        """
        dim = (self.vid_side, self.vid_side)
        while True:
            start = time.time()
            frameR, frameL = self.capR.read()[1], self.capL.read()[1]
            frameR = cv2.resize(frameR, dim)
            frameL = cv2.resize(frameL, dim)
            frames = np.concatenate((frameR, frameL), axis=1)
            # Creating and scaling QImage
            img = self.openCV2Qimage(frames)
            scaled_img = img.scaled(self.vid_side*3, self.vid_side*3, Qt.KeepAspectRatio)
            self.pred_time = np.round((time.time() - start), decimals=5)
            # Emit signal
            self.updateFrame.emit(scaled_img)
        self.capR.release()
        self.capL.release()
        sys.exit(-1)

    
