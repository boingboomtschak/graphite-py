from PyQt5 import QtWidgets

# ---- Image Methods ----

# Takes average brightness value for block (0-255), returns value scaled into one of 7 shades
def scale_block(value):
    if value < 36:
        return 36 # shade 1
    elif value < 108:
        return 72 # shade 2
    elif value < 108:
        return 108 # shade 3
    elif value < 144:
        return 144 # shade 4
    elif value < 180:
        return 180 # shade 5
    elif value < 216:
        return 216 # shade 6
    else:
        return 255 # shade 7

def avg_block(block):
    # Get average brightness of block
    brightness = numpy.average([numpy.average([(block.getpixel((w, h))[0] + block.getpixel((w, h))[1] + block.getpixel((w, h))[2]) / 3 for h in range(block.size[1])]) for w in range(block.size[0])])
    # Scale brightness to set color shades
    brightness = scale_block(brightness)
    # Fill block with average scaled brightness
    block.paste((brightness, brightness, brightness), (0, 0, block.size[0], block.size[1]))
    # Return altered block
    return block

def graphite(input_path, output_path, block_factor):
    im = Image.open(input_path)
    w, h = im.size
    block_size = w // block_factor
    # Subdivide image into blocks
    blocks = []
    for hblock in range(0, h, block_size):
        row = []
        for wblock in range(0, w, block_size):
            if(hblock + block_size <= h and wblock + block_size <= w):
                row.append(im.crop((wblock, hblock, wblock + block_size, hblock + block_size)))
            else:
                row.append(im.crop((wblock, hblock, w, h)))
        blocks.append(row)
    # Call image to convert block into block filled with average brightness
    blocks = [[avg_block(b) for b in a] for a in blocks]
    #blocks = [map(avg_block, x) for x in blocks]
    out_canvas = Image.new("RGB", (w, h))
    for a in range(0, h, block_size):
        for b in range(0, w, block_size):
            if (a + block_size <= h and b + block_size <= w):
                out_canvas.paste(blocks[a//block_size][b//block_size], (b, a, b + block_size, a + block_size))
            else:
                out_canvas.paste(blocks[a//block_size][b//block_size], (b, a, w, h))
    out_canvas.save(output_path, "JPEG")
    
def pick_image(mode):
    if mode == "open":
        filePicker = QtWidgets.QFileDialog()
        filePicker.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        filePicker.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        filePicker.setNameFilter("Images (*.png *.jpg)")
        im_path = None
        if filePicker.exec_():
            files = filePicker.selectedFiles()
            if len(files) >= 1:
                im_path = files[0]
        return im_path
    elif mode == "save":
        filePicker = QtWidgets.QFileDialog()
        filePicker.setFileMode(QtWidgets.QFileDialog.AnyFile)
        filePicker.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        filePicker.setNameFilter("Images (*.png *.jpg)")
        im_path = None
        if filePicker.exec_():
            files = filePicker.selectedFiles()
            if len(files) >= 1:
                im_path = files[0]
        return im_path