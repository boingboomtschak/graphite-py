import sys
import os
import numpy
import multiprocessing
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PIL import Image
from utils import *






# ---- Button Events ----

def convertButton():
    print("convertButton clicked!")

def chooseInputImage():
    inputImage = window.findChild(QtWidgets.QLabel, "inputImage") 
    pixmap = QtGui.QPixmap(pick_image("open"))
    if not pixmap.isNull():
        pixmap = pixmap.scaled(inputImage.width(), inputImage.height())
        inputImage.setPixmap(pixmap)

def chooseOutputImage():
    pass

def blockSizeSlider():
    blockSize = blockSlider.value()
    blockNumber.display(blockSize)

# ---- UI Methods ----

'''
def register_ui_paths(window):
    return {
        "inputImage": window.findChild(QtWidgets.QLabel, "inputImage"),
        "outputImage": window.findChild(QtWidgets.QLabel, "outputImage"),
        "convertButton": window.findChild(QtWidgets.QPushButton, "convertButton"),
        "convertProgress": window.findChild(QtWidgets.QProgressBar, "convertProgress"),
        "chooseInputImage": window.findChild(QtWidgets.QPushButton, "chooseInputImage"),
        "chooseOutputImage": window.findChild(QtWidgets.QPushButton, "chooseInputImage"),
        "blockSizeSlider": window.findChild(QtWidgets.QSlider, "blockSizeSlider"),
        "blockSizeLabel": window.findChild(QtWidgets.QLabel, "blockSizeLabel"),
        "blockSizeNumber": window.findChild(QtWidgets.QLCDNumber, "blockSizeNumber"),
        "blockCalcDropdown": window.findChild(QtWidgets.QComboBox, "blockCalcDropdown"),
        "blockCalcLabel": window.findChild(QtWidgets.QLabel, "blockCalcLabel"),
    }
'''

def register_ui(w):
    w.findChild(QtWidgets.QPushButton, "convertButton").clicked.connect(convertButton)
    w.findChild(QtWidgets.QPushButton, "chooseInputImage").clicked.connect(chooseInputImage)
    w.findChild(QtWidgets.QPushButton, "chooseOutputImage").clicked.connect(chooseOutputImage)
    w.findChild(QtWidgets.QSlider, "blockSizeSlider").valueChanged.connect(blockSizeSlider)

# ---- Main ----


# Startup PyQt code
appctxt = ApplicationContext()
window = uic.loadUi("window.ui")
window.show()
register_ui(window)

# Initializing block size elements
blockSlider = window.findChild(QtWidgets.QSlider, "blockSizeSlider")
blockNumber = window.findChild(QtWidgets.QLCDNumber, "blockSizeNumber")
blockSize = blockSlider.value()
blockNumber.display(blockSize)


# Exit PyQt code
exit_code = appctxt.app.exec_()      
sys.exit(exit_code)

'''def script_main():
    graphite("images/Durer_Self.jpg", "images/output-Durer-self.jpg", 32)'''



