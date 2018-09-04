# -*- coding: utf-8 -*-
"""Image cropper

This module crops images (png by default) in a directory.  

Example:

    $ python image_crop.py img/orig img/cropped 0 0 640 480

"""

import sys
from os import listdir
from os.path import isfile, join, basename
from PIL import Image

def get_image(image_dir, extension='.png'):
    files = [f for f in listdir(image_dir) if isfile(join(image_dir, f))]
    return [join(image_dir, f) for f in files if extension in f]

def crop_and_save(in_dir, out_dir, start_x, start_y, end_x, end_y):
    for i in get_image(in_dir):
        im = Image.open(i)
        im.crop((start_x, start_y, end_x, end_y)).save(join(out_dir, basename(i)))

if __name__ == '__main__':
    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    start_x = int(sys.argv[3])
    start_y = int(sys.argv[4])
    end_x = int(sys.argv[5])
    end_y = int(sys.argv[6])

    crop_and_save(in_dir, out_dir, start_x, start_y, end_x, end_y)
