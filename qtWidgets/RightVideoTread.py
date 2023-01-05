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
    def __init__(self, parent=None, opt=None):
        QThread.__init__(self, parent)
        self.opt = opt
        self.capR = cv2.VideoCapture(opt.rvid_path)
        self.capL = cv2.VideoCapture(opt.lvid_path)
        self.pred_time = 0
        self.disparity = 0
        self.distance = 0
        self.angleX = 0
        self.angleY = 0
        self.vid_side = opt.vid_size
        self.conf_thres = opt.conf_thres
        self.per_frames = opt.per_frames
        self.max_disparity = opt.max_disparity
        self.min_disparity = opt.min_disparity
        self.Rstack = []
        self.Lstack = []
        self.init_onnx_model()
        
    def frame_reset(self):
        self.Rstack = []
        self.Lstack = []
        
    def openCV2Qimage(self, cvImage):
        resizedW, resizedW = self.vid_side*2, self.vid_side
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
        dim = (self.vid_side*2, self.vid_side)
        while self.capR.isOpened() and self.capL.isOpened():
            try:
                retR, frameR = self.capR.read()
                retL, frameL = self.capL.read()
                self.Rstack.append(frameR)
                self.Lstack.append(frameL)
                if not retR and not retL:
                    break
            except Exception as e:
                print(e)
                continue
            if len(self.Rstack)==self.per_frames and len(self.Lstack)==self.per_frames:
                start = time.time()
                frameR_, Rx, Ry = self.qt_onnx_inference(self.Rstack[-1])
                frameL_, Lx, Ly = self.qt_onnx_inference(self.Lstack[-1])
                frames = np.concatenate((frameR_, frameL_), axis=1)
                #frames_ = cv2.resize(frames, dim)
                if Rx >0 and Lx > 0:
                    self.disparity = abs(Rx-Lx)
                    if self.disparity <= self.max_disparity and self.disparity > self.min_disparity:
                        h, w = frames.shape[:2]
                        self.distance, self.angleX, self.angleY = prams_calcurator(self.disparity, width=w, x=Rx, y=Ry)
                        texts = 'disp:{}, distance(z):{}, angleX:{}, angleY : {}'.format(self.disparity, self.distance, self.angleX, self.angleY)
                        cv2.putText(frames, texts, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, [225, 255, 255],thickness=2)
                # Creating and scaling QImage
                img = self.openCV2Qimage(frames)
                scaled_img = img.scaled(self.vid_side*3, self.vid_side*3, Qt.KeepAspectRatio)
                self.pred_time = np.round((time.time() - start), decimals=5)
                # Emit signal
                self.updateFrame.emit(scaled_img)
                self.frame_reset()
        self.capR.release()
        self.capL.release()
        sys.exit(-1)

    
