import numpy, multiprocessing, statistics, threading, random
from PyQt5 import QtWidgets
from PIL import Image


# --- Image Methods ---

# Takes average brightness value for block (0-255), returns value scaled into one of 7 shades
def scale_block(value, scale):
    if not scale:
        return value
    scale_keys = list(scale.keys())
    scale_keys.sort()
    for i in range(len(scale_keys)-1):
        if value > scale_keys[i] and value <= scale_keys[i+1]:
            return scale_keys[i]
    return scale_keys[-1]
            

# --- Graphite (Averaged) --- 

def graphite_avg_box(im, l, r, t, b): # image, left, right, top, bottom
    brightness = int(numpy.average([[statistics.mean(im.getpixel((x, y))) for y in range(t, b)] for x in range(l, r)]))
    im.paste((brightness, brightness, brightness), (l, t, r, b))

def graphite_avg(input_path, output_path, bfactor, scale=None):
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
    print("Starting thread with {} algorithm on row {} with block size {}".format(algo.__name__, row_num, bsize))
    imw, imh = im.size
    for a in range(0, imw, bsize):
        if a + bsize <= imw:
            graphite_avg_box(im, a, a+bsize, 0, imh)
        else:
            graphite_avg_box(im, a, imw, 0, imh)
    rows[row_num] = im

# -- Graphite (Sampled) --- 

def graphite_smp_box(im, l, r, t, b, scale=None):
    x = random.randint(l, r-1)
    y = random.randint(t, b-1)
    brightness = int(statistics.mean(im.getpixel((x, y))))
    if scale:
        brightness = scale_block(brightness, scale)
    im.paste((brightness, brightness, brightness), (l, t, r, b))

def graphite_smp(input_path, output_path, bfactor, scale=None):
    im = Image.open(input_path)
    w, h = im.size
    bsize = w // bfactor
    print("Processing image...")
    for a in range(0, h, bsize):
        for b in range(0, w, bsize):
            if (a + bsize <= h) and (b + bsize <= w):
                graphite_smp_box(im, b, b + bsize, a, a + bsize, scale)
            elif (b + bsize <= w):
                graphite_smp_box(im, b, b + bsize, a, h, scale)
            else:
                graphite_smp_box(im, b, w, a, h, scale)
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