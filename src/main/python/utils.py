import numpy, multiprocessing, statistics, threading, random
from PyQt5 import QtWidgets
from PIL import Image


# ---- Image Methods ----

# Takes average brightness value for block (0-255), returns value scaled into one of 7 shades
def scale_block(value):
    if value < 36:
        return 36 # shade 1
    elif value < 72:
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




def old_graphite(input_path, output_path, block_factor):
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
    out_canvas.save(output_path, "PNG")




def graphite_avg_box(im, l, r, t, b): # image, left, right, top, bottom
    brightness = int(numpy.average([[statistics.mean(im.getpixel((x, y))) for y in range(t, b)] for x in range(l, r)]))
    im.paste((brightness, brightness, brightness), (l, t, r, b))

def graphite_avg(input_path, output_path, bfactor, scale=False):
    im = Image.open(input_path)
    w, h = im.size
    bsize = w // bfactor
    processes = []
    print("Processing image...")
    rnum = 0
    rows = {}
    for a in range(0, h, bsize):
        if a + bsize > h:
            row = im.crop((0, a, w, h))
        else:
            row = im.crop((0, a, w, a + bsize))
        p = threading.Thread(target=image_row, args=(row, rnum, bsize, graphite_avg_box, rows))
        processes.append(p)        
        rnum += 1
    [p.start() for p in processes]
    [p.join() for p in processes]
    paste_h = 0
    for i in range(rnum):
        if paste_h + bsize <= h:
            im.paste(rows[i], (0, paste_h, w, paste_h + bsize))
        else:
            im.paste(rows[i], (0, paste_h, w, h))
        paste_h += bsize
    print("Processing complete!")
    print("Saving image...")
    im.save(output_path, "PNG")


def image_row(im, row_num, bsize, algo, rows):
    print("{} algorithm on row {} with block size {}".format(algo.__name__, row_num, bsize))
    imw, imh = im.size
    for a in range(0, imw, bsize):
        if a + bsize <= imw:
            graphite_avg_box(im, a, a+bsize, 0, imh)
        else:
            graphite_avg_box(im, a, imw, 0, imh)
    rows[row_num] = im

def graphite_smp_box(im, l, r, t, b):
    x = random.randint(l, r-1)
    y = random.randint(t, b-1)
    brightness = int(statistics.mean(im.getpixel((x, y))))
    im.paste((brightness, brightness, brightness), (l, t, r, b))

def graphite_smp(input_path, output_path, bfactor, scale=False):
    im = Image.open(input_path)
    w, h = im.size
    bsize = w // bfactor
    print("Processing image...")
    for a in range(0, h, bsize):
        for b in range(0, w, bsize):
            if (a + bsize <= h) and (b + bsize <= w):
                graphite_smp_box(im, b, b + bsize, a, a + bsize)
            elif (b + bsize <= h):
                graphite_smp_box(im, b, b + bsize, a, h)
            else:
                graphite_smp_box(im, b, w, a, h)
    print("Processing complete!")
    print("Saving image...")
    im.save(output_path, "PNG")


    
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