import argparse
import sys, os
import signal
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QDockWidget
from PySide6.QtCore import Qt
from qtWidgets.DualCamWidget import DualCamWidget
from qtWidgets.LeftWidget import LeftWidget
from yolov7s.image_inference import image_inference

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--qt', action='store_true', help='inference movie at QT')
    parser.add_argument('--image', action='store_true', help='single image inference')
    parser.add_argument('--vid', action='store_true', help='movie inference')
    parser.add_argument('--img_path', type=str, default='data/images/bus.jpg', help='image path')
    parser.add_argument('--onnx_path', type=str, default='yolov7Tiny_640_640.onnx', help='image path')
    parser.add_argument('--cpu', type=str, default='True', help='if cpu is None, use CUDA')
    parser.add_argument('--per_frames', type=int, default=5, help='num frames to predict at each thread for reducing device burden')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='conf threshold for NMS or postprocess')
    parser.add_argument('--max_disparity', type=int, default=200, help='max disparity')
    parser.add_argument('--rvid_path', type=str, default='data/right.mp4', help='right video path')
    parser.add_argument('--lvid_path', type=str, default='data/left.mp4', help='left video path')
    parser.add_argument('--vid_size', type=int, default=250, help='Display video size')
    opt = parser.parse_args()
    return opt

    
class MyMainWindow(QMainWindow):
    def __init__(self, opt, parent=None):
        super(MyMainWindow, self).__init__(parent)
        
        # RIGHT Side camera widget
        here_path = os.path.dirname(os.path.abspath(__file__))
        self.plot_layout = QVBoxLayout()
        self.right_widget = DualCamWidget(self, opt)
        self.plot_layout.addWidget(self.right_widget)
        self.setCentralWidget(self.right_widget)
        
        # Left side widget
        th = self.right_widget.return_thread()
        self.leftDock = QDockWidget("Left Widget", self)
        self.leftside = LeftWidget(self, th)
        self.leftDock.setWidget(self.leftside)
 
        self.leftDock.setAllowedAreas(Qt.LeftDockWidgetArea
                                   | Qt.RightDockWidgetArea)
        self.leftDock.setFeatures(QDockWidget.DockWidgetMovable
                                  | QDockWidget.DockWidgetFloatable \
                                  #|QDockWidget.DockWidgetVerticalTitleBar)
                                  )
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftDock)
 
   
def main(opt):
    if opt.qt:
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        app = QApplication(sys.argv)
        W = opt.vid_size*4
        H = opt.vid_size*3
        try:
            w = MyMainWindow(opt)
            w.setWindowTitle("PySide Layout on QMainWindow")
            w.resize(W, H)
            w.show()
            app.exec_()
        except KeyboardInterrupt:
            app.shutdown()
        sys.exit()
    elif opt.image:
        image_inference(opt)
    elif opt.vid:
        os.system('python3 yolov7s/movie_inference.py')
    else:
        print("add option --qt or --image or --vid")
        sys.exit(1)
        
if __name__ == '__main__':
    opt = get_parser()
    main(opt)
