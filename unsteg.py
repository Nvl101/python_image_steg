# -*- coding: utf-8 -*-
"""
Part III, 

inputting two images, one original, one new
extract array delta
write file into zip/txt

@author: zhouyu12
"""

from PIL import Image #, ImageTK
from tkinter import filedialog
import numpy as np
import os, sys

verbose = True
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

vprint = lambda *args, **kwargs: print(*args, **kwargs) if verbose else None

vprint('First, choose the original image')
image_path_original = filedialog.askopenfilename(filetypes=[
    ('image','.png'),
    ('image','bmp'),
    ])

if image_path_original == '':
    sys.exit()
    
with Image.open(image_path_original) as im:
    array_image_original = np.asarray(im)
    array_image_original = array_image_original.astype('uint8')
    image_shape_original = array_image_original.shape
    array_image_original = array_image_original.flatten('C')
    #array_image_original.reshape(
    #    image_shape_original[0] * image_shape_original[1] * 3, 1).flatten('C')
vprint('\tOK\n')

vprint('Next, choose the new image')
image_path_new = filedialog.askopenfilename(filetypes=[
    ('image','.png'),
    ('image','.bmp'),
    ])

if image_path_new == '':
    sys.exit()
    
with Image.open(image_path_new) as im:
    array_image_new = np.asarray(im)
    array_image_new = array_image_new.astype('uint8')
    image_shape_new = array_image_new.shape
    array_image_new = array_image_new.flatten('C')
    #reshape(
    #    image_shape_new[0] * image_shape_new[1] * 3, 1).flatten('C')
if not image_shape_new == image_shape_original:
    raise ValueError('Images should be samely sized')
vprint('\tOK\n')

# the interesting part -----

# 4 quads to a (0,255) byte
quadual_assemble = lambda x, a=64, b= 16, c = 4: \
    x[0] * 64 + x[1] * 16 + x[2] * 4 + x[3]

# calculating length using last 16 bytes
quarternary_sum = lambda x:\
    int(sum(np.asarray(x) * 4**np.arange(15, -1, -1)))  
    
array_file_delta = np.abs(array_image_new.astype('int8') - 
                          array_image_original.astype('int8'))
array_file_size = np.abs(array_file_delta[-16:])
file_length = quarternary_sum(array_file_size)
array_file_delta = array_file_delta[:file_length*4]

# the interesting part, re-assemble array_file
array_file = array_file_delta.reshape(
    (int(len(array_file_delta) / 4), 4)
    )#.flatten('F')

array_file = np.apply_along_axis(quadual_assemble, 1, array_file)
array_file = array_file.astype('uint8')
file_content = array_file.tobytes()

# we got the file ready for output
output_file_name = input('Enter filename for output: ')
output_path = os.path.join(
    os.path.abspath('output'),
    output_file_name
)

with open(output_path,'wb') as file:
    file.write(file_content)

vprint(f'File written to: f{output_path}')