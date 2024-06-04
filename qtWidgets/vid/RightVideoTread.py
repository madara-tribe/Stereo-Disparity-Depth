import time
import cv2
import numpy as np
import onnxruntime
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage

from yolov7s.common import letterbox, preprocess, onnx_inference, post_process
from yolov7s.dist_calcurator import prams_calcurator
cuda = False


class Thread(QThread):
    updateFrame = Signal(QImage)
    def __init__(self, parent=None, opt=None, hyp=None):
        QThread.__init__(self, parent)
        self.opt = opt
        self.hyp = hyp
        #self.resizeW, self.resizeH = self.hyp['display_width'], self.hyp['display_height']
        self.capR = cv2.VideoCapture(opt.rvid_path)
        self.capL = cv2.VideoCapture(opt.lvid_path)
        self.pred_time = 0
        self.angleX = self.angleY = self.distance = self.disparity = 0
        self.vid_side = opt.vid_size
        self.conf_thres = opt.conf_thres
        self.max_disparity = opt.max_disparity
        self.min_disparity = opt.min_disparity
        self.TIMEOUT = opt.frame_interval
        self.count = 0
        self.Rstack = self.Lstack = []
        self.init_onnx_model()
        
    def frame_reset(self):
        self.Rstack = []
        self.Lstack = []
        self.count = 0
        
    def openCV2Qimage(self, cvImage):
        cvImage = cv2.resize(cvImage, (self.vid_side*2, self.vid_side))
        height, width, channel = cvImage.shape
        bytesPerLine = channel * width
        cvImageRGB = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
        image = QImage(cvImageRGB, width, height, bytesPerLine, QImage.Format_RGB888)
        return image
        
    def init_onnx_model(self):
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
        self.session = onnxruntime.InferenceSession(self.opt.onnx_path, providers=providers)
        IN_IMAGE_H = self.session.get_inputs()[0].shape[2]
        IN_IMAGE_W = self.session.get_inputs()[0].shape[3]
        self.new_shape = (IN_IMAGE_W, IN_IMAGE_H)
    
    def qt_onnx_inference(self, frame):
        ori_images = [frame.copy()]
        resized_image, ratio, dwdh = letterbox(frame, new_shape=self.new_shape, auto=False)
        input_tensor = preprocess(resized_image)
        outputs = onnx_inference(self.session, input_tensor)
        pred_output, coordinate_x, coordinate_y = post_process(outputs, ori_images, ratio, dwdh, self.conf_thres)
        return pred_output[0], coordinate_x, coordinate_y
    
    def run(self):
        """Read frame from camera and repaint QLabel widget.
        """
        while self.capR.isOpened() and self.capL.isOpened():
            retR, frameR = self.capR.read()
            retL, frameL = self.capL.read()
            if frameL is None or frameR is None:
                continue
            self.Rstack.append(frameR)
            self.Lstack.append(frameL)
            self.count += 0.01
            if (time.time() - self.count) > self.TIMEOUT:
                wlen, hlwn = frameR.shape[:2]
                start = time.time()
                frameR_, Rx, Ry = self.qt_onnx_inference(frameR)
                frameL_, Lx, Ly = self.qt_onnx_inference(frameL)
                output = np.concatenate((frameR_, frameL_), axis=1)
                if Rx >0 and Lx > 0:
                    disparity = abs(Rx-Lx)
                    if disparity <= self.max_disparity and disparity > self.min_disparity:
                        self.disparity, self.distance, self.angleX, self.angleY = prams_calcurator(self.hyp, disparity, width=wlen, height=hlwn, x=int((Rx+Lx)/2), y=int((Ry+Ly)/2))
                # Creating and scaling QImage
                img = self.openCV2Qimage(output)
                scaled_img = img.scaled(self.vid_side*3, self.vid_side*3, Qt.KeepAspectRatio)
                self.pred_time = np.round((time.time() - start), decimals=5)
                # Emit signal
                self.updateFrame.emit(scaled_img)
                self.frame_reset()
        self.capR.release()
        self.capL.release()
        

    
