import sys
import os
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets, uic
from PIL import Image


BLOCK_SIZE = 40
IMAGE_PATH = "Albrecht_Durer.jpg"

# Takes average alpha value for block (0-255), returns value scaled into one of 7 shades
def scale_block(alpha):
    if alpha < 36:
        return 36 # shade 1
    elif alpha < 72:
        return 72 # shade 2
    elif alpha < 108:
        return 108 # shade 3
    elif alpha < 144:
        return 144 # shade 4
    elif alpha < 180:
        return 180 # shade 5
    elif alpha < 216:
        return 216 # shade 6
    else:
        return 255 # shade 7

def main():
    # Startup PyQt code
    appctxt = ApplicationContext()
    window = uic.loadUi("window.ui")
    im = Image.open(IMAGE_PATH)
    window.show()

    # Exit PyQt code
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
