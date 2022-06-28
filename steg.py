# -*- coding: utf-8 -*-
# steg algorithms on whiteboard

"""
Part II, creating Steg with 
import 256-EAX from personal laptop

It has bugs possibly, but will not appear in Jira for sure
supports single picture carrying single file
can use zipfile and pycrypto to zip and encrypt
"""

import sys
from tkinter import filedialog
from PIL import Image #, ImageTK
import numpy as np

VERBOSE = True

vprint = lambda *args, **kwargs: print(*args, **kwargs) if VERBOSE else None

# image array
vprint('First, choose an image')
image_path = filedialog.askopenfilename(filetypes=[
    ('image','.png'),
    ('image','jpg'),
    ('image','bmp'),
    ])

if image_path == '':
    sys.exit()

with Image.open(image_path) as im:
    array_image = np.asarray(im)
    array_image = array_image.astype('uint8')
    image_shape = array_image.shape
    # standard procedure: flatten 'C', in 1:RGB 2:RGB... format
    array_image = array_image.flatten('C')
    #.reshape(
    #    image_shape[0] * image_shape[1] * 3, 1).flatten('F')
vprint('\tOK\n')

# file array
vprint('Next, choose a file to write')
file_path = filedialog.askopenfilename()
if file_path == '':
    sys.exit()
with open(file_path,'rb') as file:
    array_file = np.asarray(list(file.read()))
vprint('\tOK\n')

np.random.get_state()

# steg, the interesting part
image_length = len(array_image)
file_length = len(array_file)

if file_length > image_length/4:
    raise ValueError('file must be smaller than 1/4 of image')

quadual_split = lambda x, a = 64, b = 16, c = 4: \
    (x // a, x % a // b, x % a % b // c, x % a % b % c)
max_byte = 3
# we pad file length, to make the noise even
# last 16 bytes to show file size
pad_length = (len(array_image) - len(array_file) * 4) - 16
array_file_expanded = np.apply_along_axis(quadual_split,0,array_file).T
array_file_expanded = array_file_expanded.flatten('C').astype('uint8')
array_pad = np.random.randint(0,3,size=pad_length).astype('uint8')
# last 16 bytes shows the file size
quarternary = lambda x, a=15, b=0:\
    [x % (4**(p + 1)) // (4**p) for p in np.arange(a,b,-1)] +\
        [x % 4**(b + 1)]
array_file_length = np.array(
[file_length % (4**(p + 1)) // (4**p) for p in
     np.arange(15,0,-1,dtype='int64')] + \
    [file_length % 4],
dtype='uint8'
)
array_delta_abs = np.concatenate(
    (array_file_expanded, array_pad, array_file_length)
    ).flatten('F')
array_delta_abs = array_delta_abs.astype('uint8')

bool_do_plus = np.random.randint(0, 1, size=image_length)
bool_do_plus[(array_delta_abs + array_image) < 256]=0
bool_do_plus[array_delta_abs > array_image]=1
bool_do_plus = bool_do_plus.astype('int8')
bool_plus_minus = bool_do_plus * 2 - 1
array_delta_abs = array_delta_abs.astype('int8')
array_delta = array_delta_abs * bool_plus_minus

array_new_image = array_image + array_delta
array_new_image = array_new_image.astype('uint8')
array_new_image = array_new_image.reshape(image_shape)

# birth of new image
with Image.fromarray(array_new_image) as im:
    new_image_path = image_path[::-1].replace('.','.wen_',1)[::-1]
    new_image_path = new_image_path.replace('.jpg','.png')
    im.save(new_image_path)

vprint('Done.')
