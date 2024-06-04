import sys
sys.path.append('../yolov7s')
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
        self.hyp = hyp
        self.opt = opt
        self.resizeW, self.resizeH = self.hyp['display_width'], self.hyp['display_height']
        self.disparity = 0
        self.distance = 0
        self.angleX = 0
        self.angleY = 0
        self.vid_side = opt.vid_size
        self.conf_thres = opt.conf_thres
        self.max_disparity = opt.max_disparity
        self.min_disparity = opt.min_disparity
        self.init_onnx_model()

        
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
        print(resized_image.shape)
        input_tensor = preprocess(resized_image)
        outputs = onnx_inference(self.session, input_tensor)
        pred_output, coordinate_x, coordinate_y = post_process(outputs, ori_images, ratio, dwdh, self.conf_thres)
        return pred_output[0], int(coordinate_x), int(coordinate_y)
        
    def run(self):
        imgR = cv2.imread(self.opt.rimg_path)
        imgL = cv2.imread(self.opt.limg_path)
        start = time.time()
        outputR, Rx, Ry = self.qt_onnx_inference(imgR)
        outputL, Lx, Ly = self.qt_onnx_inference(imgL)
        cv2.circle(outputR, center=(Rx, Ry), radius=20, color=(0, 255, 255), thickness=-1)
        cv2.circle(outputL, center=(Lx, Ly), radius=20, color=(0, 255, 255), thickness=-1)
        output = np.concatenate((outputR, outputL), axis=1)
        print(Rx, Lx)
        if Rx >0 and Lx > 0:
            disparity = abs(Rx-Lx)
            wlen, hlwn = imgR.shape[:2]
            print('disparity', disparity, wlen, hlwn)
            if disparity <= self.max_disparity and disparity > self.min_disparity:
                self.disparity, self.distance, self.angleX, self.angleY = prams_calcurator(self.hyp, disparity, width=wlen, height=hlwn, x=int((Rx+Lx)/2), y=int((Ry+Ly)/2))
                # Creating and scaling QImage
                img = self.openCV2Qimage(output)
                scaled_img = img.scaled(self.vid_side*3, self.vid_side*3, Qt.KeepAspectRatio)
                self.pred_time = np.round((time.time() - start), decimals=5)
                # Emit signal
                self.updateFrame.emit(scaled_img)

    
