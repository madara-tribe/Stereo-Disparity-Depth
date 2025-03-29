import cv2
import time
import numpy as np
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import QSize, QTimer
from PySide6.QtGui import QImage, QPixmap
from depth_estimate import qt6_onnx_prepare, precise_dist
from midas.midas_utils import call_transform, midas_onnx_prediction
from yolov7s.common import obdetect_inference
        
        
class QtWidgetUI(QWidget):
    def __init__(self, parent, opt):
        super(QtWidgetUI, self).__init__(parent)
        self.VideoWidget(opt)
        self.FPSbar()
        self.PredictedTimeBar()
        
    def VideoWidget(self, opt):
        # video widget
        self.video_size = QSize(opt.width, opt.height)
        self.video_widget = QLabel()
        self.video_widget.setFixedSize(self.video_size)
        
    def FPSbar(self):
        # FPS bar
        self.fps_layout = QHBoxLayout()
        self.fps_title = QLabel('Constant FPS')
        self.fps = QLabel('', self)
        self.fps.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.fps_layout.addWidget(self.fps_title)
        self.fps_layout.addWidget(self.fps)
        self.fps.setText("now loading")
        
    
    def PredictedTimeBar(self):
        # Predicted time bar
        self.predictor_layout = QHBoxLayout()
        self.predictor_title = QLabel('Predicted time')
        self.predictbar = QLabel('', self)
        self.predictbar.setStyleSheet('font-family: Times New Roman; font-size: 15px; color: black; background-color: azure')
        self.predictor_layout.addWidget(self.predictor_title)
        self.predictor_layout.addWidget(self.predictbar)



class RightCamWidget(QWidget):
    def __init__(self, parent, opt):
        super().__init__(parent=parent)
        
        self.parent = parent
        self.cap = cv2.VideoCapture(opt.video_path)
        self.W, self.H = opt.width, opt.height
        self.video_size = QSize(self.W, self.H)
        self.TIMEOUT = 1
        self.cur_fps = 0
        self.old_timestamp = time.time()
        self.setup_onnx_env(opt)
        self.setup_ui(opt)
        self.setup_camera()
    
    def setup_onnx_env(self, opt):
        self.conf_thres = opt.conf_thres
        self.session, self.new_shape, self.midas_onnx_model = qt6_onnx_prepare(opt)
        self.transform, self.net_h, self.net_w = call_transform()
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
    def setup_ui(self, opt):
        self.rui = QtWidgetUI(self, opt)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.rui.video_widget)
        self.main_layout.addLayout(self.rui.predictor_layout)
        self.main_layout.addLayout(self.rui.fps_layout)
        self.setLayout(self.main_layout)
        
    def setup_camera(self):
        """Initialize camera.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_video_stream)
        self.timer.start(30)

    def display_video_stream(self):
        """Read frame from camera and repaint QLabel widget.
        """
        _, frame = self.cap.read()
        fps = (time.time() - self.old_timestamp) / self.TIMEOUT
        if (time.time() - self.old_timestamp) > self.TIMEOUT:
            start = time.time()
            """ when prediction adjust frame size """
            ##### START INFERENCE #####
            # midas inference
            depth_midas = cv2.resize(midas_onnx_prediction(frame.copy(), self.transform, self.midas_onnx_model, self.net_h, self.net_w), (self.frame_width, self.frame_height))
            # object detectioon inference
            pred_frame, mid_x, mid_y = obdetect_inference(frame.copy(), depth_midas, self.session, self.new_shape, self.conf_thres)
            self.predict_time = np.round((time.time() - start), decimals=5)
            ##### FINISH INFERENCE #####
            ### PLot Criteria ###
            pred_frame = precise_dist(pred_frame, px=int(self.frame_width/2), py=self.frame_height, title="CRITERIA Dist: ")
            ### Plot on Widget ###
            """ adjust video widget size """
            pred_frame = cv2.resize(pred_frame, (self.W, self.H))
            image = QImage(pred_frame, pred_frame.shape[1], pred_frame.shape[0],
                            pred_frame.strides[0], QImage.Format_RGB888)
            self.rui.video_widget.setPixmap(QPixmap.fromImage(image))
            self.old_timestamp = time.time()
            
            self.cur_fps = np.round(fps, decimals=3)
            self.rui.fps.setText(str(self.cur_fps))
            self.rui.predictbar.setText(str(self.predict_time*1000)+"[ms]")

