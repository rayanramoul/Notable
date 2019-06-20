import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class app():
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        w = QtWidgets.QWidget()
        b = QtWidgets.QLabel(w)
        b.setText("NEURALOPS")
        w.setGeometry(100,100,200,50)
        b.move(50,20)
        w.setWindowTitle("NEURALOPS")
        w.show()
        sys.exit(app.exec_())