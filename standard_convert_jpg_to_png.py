# -*- coding: utf-8 -*-
"""
the standard method to convert jpg to png
why use png? because we all love precision.

@author: zhouyu12
"""

from tkinter import filedialog
from PIL import Image #, ImageTK
import numpy as np

# main_parser = argparse.ArgumentParser(description='')
# main_parser.add_argument('-i','--input',action='store_value',help='input file path')

image_input_path = filedialog.askopenfilename(filetypes=[
    ('JPEG image','.jpg')
    ])
image_output_path = image_input_path.replace('.jpg','.png')

with Image.open(image_input_path) as im:
    array_image = np.asarray(im)
    array_image = array_image.astype('uint8')

with Image.fromarray(array_image) as im:
    im.save(image_output_path)
