import argparse
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from Qt6Widget import RightCamWidget

class MyMainWindow(QMainWindow):
    def __init__(self, opt, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.plot_layout = QVBoxLayout()
        self.right_widget = RightCamWidget(self, opt)
        self.plot_layout.addWidget(self.right_widget)
        self.setCentralWidget(self.right_widget)
    
        
def main(opt):
    app = QApplication(sys.argv)
    w = MyMainWindow(opt)
    w.setWindowTitle("PySide Layout on QMainWindow")
    w.resize(opt.width+200, opt.height+200)
    w.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--yolov7_onnx_path', type=str, default='weights/yolov7Tiny_640_640.onnx', help='image path')
    parser.add_argument('--midas_onnx_path', type=str, default='weights/model-f6b98070.onnx', help='onnx midas weight model')
    parser.add_argument('--cpu', type=str, default='True', help='if cpu is None, use CUDA')
    
    parser.add_argument('--conf-thres', type=float, default=0.25, help='conf threshold for NMS or postprocess')
    parser.add_argument('--video_path', type=str, default='data/outdriving.mov', help='right video path')
    parser.add_argument('--height', type=int, default=600, help='height of movie')
    parser.add_argument('--width', type=int, default=1100, help='width of of movie')
    opt = parser.parse_args()
    try:
        main(opt)
    except KeyboardInterrupt:
        sys.exit(1)
        raise
