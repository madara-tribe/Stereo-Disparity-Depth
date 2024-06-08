import argparse
import sys
import yaml
import signal
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QDockWidget
from PySide6.QtCore import Qt
from qtWidgets.img.DualCamWidget import DualCamWidget as imgDualCamWidget
from qtWidgets.img.ImgLeftWidget import ImgLeftWidget
from qtWidgets.vid.DualCamWidget import DualCamWidget as vidDualCamWidget
from qtWidgets.vid.VidLeftWidget import VidLeftWidget


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', action='store_true', help='single image inference')
    parser.add_argument('--vid', action='store_true', help='movie inference')
    parser.add_argument('--onnx_path', type=str, default='yolov7Tiny_640_640.onnx', help='image path')
    parser.add_argument('--cpu', type=str, default='True', help='if cpu is None, use CUDA')
    parser.add_argument('--frame_interval', type=int, default=50, help='interval time to reduce device burden')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='conf threshold for NMS or postprocess')
    parser.add_argument('--max_disparity', type=int, default=500, help='max disparity')
    parser.add_argument('--min_disparity', type=int, default=40, help='max disparity')
    parser.add_argument('--rimg_path', type=str, default='data/right/image_039.png', help='right img path')
    parser.add_argument('--limg_path', type=str, default='data/left/image_039.png', help='left img path')
    parser.add_argument('--rvid_path', type=str, default='data/right.mp4', help='right video path')
    parser.add_argument('--lvid_path', type=str, default='data/left.mp4', help='left video path')
    parser.add_argument('--vid_size', type=int, default=250, help='Display video size')
    parser.add_argument('--hyp', type=str, default='hyp.waveshare.imx219.83.yaml', help='waveshare IMX219-83 hyperparameters path')
    opt = parser.parse_args()
    return opt

    
class ImgMainWindow(QMainWindow):
    def __init__(self, opt, hyp, parent=None):
        super(ImgMainWindow, self).__init__(parent)
        
        # RIGHT Side camera widget
        self.plot_layout = QVBoxLayout()
        self.right_widget = imgDualCamWidget(self, opt, hyp)
        self.plot_layout.addWidget(self.right_widget)
        self.setCentralWidget(self.right_widget)
        
        # Left side widget
        th = self.right_widget.return_thread()
        self.leftDock = QDockWidget("Left Widget", self)
        self.leftside = ImgLeftWidget(self, th)
        self.leftDock.setWidget(self.leftside)
 
        self.leftDock.setAllowedAreas(Qt.LeftDockWidgetArea
                                   | Qt.RightDockWidgetArea)
        self.leftDock.setFeatures(QDockWidget.DockWidgetMovable
                                  | QDockWidget.DockWidgetFloatable \
                                  )
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)
 
class VidMainWindow(QMainWindow):
    def __init__(self, opt, hyp, parent=None):
        super(VidMainWindow, self).__init__(parent)
        
        # RIGHT Side camera widget
        self.plot_layout = QVBoxLayout()
        self.right_widget = vidDualCamWidget(self, opt, hyp)
        self.plot_layout.addWidget(self.right_widget)
        self.setCentralWidget(self.right_widget)
        
        # Left side widget
        th = self.right_widget.return_thread()
        self.leftDock = QDockWidget("Left Widget", self)
        self.leftside = VidLeftWidget(self, th)
        self.leftDock.setWidget(self.leftside)
 
        self.leftDock.setAllowedAreas(Qt.LeftDockWidgetArea
                                   | Qt.RightDockWidgetArea)
        self.leftDock.setFeatures(QDockWidget.DockWidgetMovable
                                  | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)
        
def main(opt, hyp):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    W = opt.vid_size*4
    H = opt.vid_size*3
    if opt.img:
        try:
            w = ImgMainWindow(opt, hyp)
            w.setWindowTitle("PySide Layout on QMainWindow")
            w.resize(W, H)
            w.show()
            app.exec_()
        except KeyboardInterrupt:
            app.shutdown()
    elif opt.vid:
        try:
            w = VidMainWindow(opt, hyp)
            w.setWindowTitle("PySide Layout on QMainWindow")
            w.resize(W, H)
            w.show()
            app.exec_()
        except KeyboardInterrupt:
            app.shutdown()
            sys.exit()
    else:
        print("add option --img or --vid")
    sys.exit()
        
if __name__ == '__main__':
    opt = get_parser()
    with open(opt.hyp, errors='ignore') as f:
        hyp = yaml.safe_load(f)
    main(opt, hyp)
