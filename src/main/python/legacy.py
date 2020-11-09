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
