from speech2action import speech2action
import sys

from PyQt5.QtCore import Qt, QCoreApplication

from PyQt5.QtWidgets import QApplication

from window_design import My_MainWindow

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # 自适应分辨率

    app = QApplication(sys.argv)

    window = My_MainWindow()
    window.show()

    sys.exit(app.exec_())