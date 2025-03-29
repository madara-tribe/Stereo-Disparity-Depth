import argparse
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QPushButton
from PySide6.QtCore import QSize
from Qt6widgets import second_window


class MainWindow(QMainWindow):
    def __init__(self, opt):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Stereo")
        self.opt = opt
        pybutton = QPushButton('Start', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(100,32)
        pybutton.move(50, 50)
        
    def clickMethod(self):
        print('Clicked Pyqt button.')
        seconWin = second_window(self.opt)
        seconWin.show()
        mainWin.close()
        
def main(opt):
    app = QApplication(sys.argv)
    mainWin = MainWindow(opt)
    mainWin.show()
    sys.exit(app.exec_())
    
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rpath', type=str, default='data/right/tsukuba_r.png', help='right img')
    parser.add_argument('--lpath', type=str, default='data/left/tsukuba_l.png', help='left img')
    #parser.add_argument('--rpath', type=str, default='data/right/000048.jpg', help='right img')
    #parser.add_argument('--lpath', type=str, default='data/left/000048.jpg', help='left img')
    parser.add_argument('--numDisparities', type=int, default=20, help='numDisparities param')
    parser.add_argument('--blockSize', type=int, default='2', help='blockSize param')
    opt = parser.parse_args()
    try:
        main(opt)
    except KeyboardInterrupt:
        sys.exit(1)
        raise
