import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import utils


# ---- Button Events ----

def convertButton():
    global inputPath
    if inputPath:
        print("Starting graphite...")
        utils.graphite(inputPath, "temp.png", blockSize) 
        convertProgress(100)
        outputImage = window.findChild(QtWidgets.QLabel, "outputImage")
        pixmap = QtGui.QPixmap("temp.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(outputImage.width(), outputImage.height())
            outputImage.setPixmap(pixmap)
    else:
        print("No inputPath!")

def chooseInputImage():
    global inputPath
    inputImage = window.findChild(QtWidgets.QLabel, "inputImage") 
    path = utils.pick_image("open")
    pixmap = QtGui.QPixmap(path)
    if not pixmap.isNull():
        inputPath = path
        pixmap = pixmap.scaled(inputImage.width(), inputImage.height())
        inputImage.setPixmap(pixmap)
        convertProgress(0)


def chooseOutputImage():
    pass

def blockSizeSlider():
    blockSize = blockSlider.value()
    blockNumber.display(blockSize)

def blockCalcDropdown():
    blockStrategy = blockCalc.currentText()

def convertProgress(percent):
    window.findChild(QtWidgets.QProgressBar, "convertProgress").setValue(percent)


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
    w.findChild(QtWidgets.QComboBox, "blockCalcDropdown").currentTextChanged.connect(blockCalcDropdown)


# ---- Main ----

# Startup PyQt code
appctxt = ApplicationContext()
window = uic.loadUi("window.ui")
window.show()
register_ui(window)

inputPath = ""

# Initializing block size elements
blockSlider = window.findChild(QtWidgets.QSlider, "blockSizeSlider")
blockNumber = window.findChild(QtWidgets.QLCDNumber, "blockSizeNumber")
blockCalc = window.findChild(QtWidgets.QComboBox, "blockCalcDropdown")
blockSize = blockSlider.value()
blockNumber.display(blockSize)
blockStrategy = blockCalc.currentText()


# Exit PyQt code
exit_code = appctxt.app.exec_()      
sys.exit(exit_code)

'''def script_main():
    graphite("images/Durer_Self.jpg", "images/output-Durer-self.jpg", 32)'''



