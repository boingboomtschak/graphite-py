import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import utils, scales


# ---- Button Events ----

def convertButton():
    global inputPath
    global blockStrategy
    global blockSize
    global blockScale
    if inputPath:
        button = window.findChild(QtWidgets.QPushButton, "convertButton")
        button.setEnabled(False)
        convertStatus("Processing average...", "yellow")
        if blockStrategy == "Averaged":
            print("Starting averaged graphite...")
            utils.graphite_avg(inputPath, "temp.png", blockSize, blockScale) 
        elif blockStrategy == "Sampled":
            print("Starting sampled graphite...")
            utils.graphite_smp(inputPath, "temp.png", blockSize, blockScale)
        else:
            print("ERROR: Invalid block strategy!")
        convertProgress(100)
        button.setEnabled(True)
        outputImage = window.findChild(QtWidgets.QLabel, "outputImage")
        pixmap = QtGui.QPixmap("temp.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(outputImage.width(), outputImage.height())
            outputImage.setPixmap(pixmap)
        convertStatus("Processing complete!", "green")
    else:
        print("No inputPath!")
        convertStatus("Invalid input path!", "red")

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
        convertStatus("... Waiting ...", "black")


def chooseOutputImage():
    pass

def blockSizeSlider():
    global blockSize
    blockSize = blockSlider.value()
    blockNumber.display(blockSize)

def blockCalcDropdown():
    global blockStrategy
    blockStrategy = blockCalc.currentText()

def scaleDropdown():
    global blockScale
    textScale = scaleDropdown.currentText()
    if textScale == "7 Shade":
        blockScale = scales.SEVEN_SHADE
    elif textScale == "7 Shade (R)":
        blockScale = scales.SEVEN_SHADE_REVERSED
    elif textScale == "14 Shade":
        blockScale = scales.FOURTEEN_SHADE
    elif textScale == "14 Shade (R)":
        blockScale = scales.FOURTEEN_SHADE_REVERSED
    else:
        blockScale = None

# ---- UI Methods ----

def convertStatus(message, color):
    cs = window.findChild(QtWidgets.QLabel, "convertStatus")
    cs.setText(message)
    cs.setStyleSheet('color: ' + color)


def convertProgress(percent):
    window.findChild(QtWidgets.QProgressBar, "convertProgress").setValue(percent)

def register_ui(w):
    w.findChild(QtWidgets.QPushButton, "convertButton").clicked.connect(convertButton)
    w.findChild(QtWidgets.QPushButton, "chooseInputImage").clicked.connect(chooseInputImage)
    w.findChild(QtWidgets.QPushButton, "chooseOutputImage").clicked.connect(chooseOutputImage)
    w.findChild(QtWidgets.QSlider, "blockSizeSlider").valueChanged.connect(blockSizeSlider)
    w.findChild(QtWidgets.QComboBox, "blockCalcDropdown").currentTextChanged.connect(blockCalcDropdown)
    w.findChild(QtWidgets.QComboBox, "scaleDropdown").currentTextChanged.connect(scaleDropdown)


# ---- Main ----

if __name__ == "__main__":
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
    scaleDropdown = window.findChild(QtWidgets.QComboBox, "scaleDropdown")
    blockScale = None


    # Exit PyQt code
    exit_code = appctxt.app.exec_()      
    sys.exit(exit_code)

'''def script_main():
    graphite("images/Durer_Self.jpg", "images/output-Durer-self.jpg", 32)'''



