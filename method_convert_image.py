'''
Methods for converting image formats to png/bmp
'''

import os
import warnings
from typing import Union
import numpy as np
from PIL import Image #, ImageTK

NoneType = type(None)

def convert_image_paths(
    input_path: str,
    output_path: Union(str, NoneType) = None,
    overwrite: bool = False,
    verbose: bool = False,
    ) -> NoneType:
    '''
    INPUT:
    input_path, input file path to convert

    OUTPUT:
    output_path, output file path
    '''
    # OPTIONAL
    # verbose print
    vprint = lambda *args, **kwargs: print(*args, **kwargs) if verbose else None

    # OPTIONAL
    # checking validity of input and output file paths
    if not os.path.isfile(input_path):
        error_msg = f'Input file "{input_path}" not found.'
        raise FileNotFoundError(error_msg)
    if os.path.isfile(output_path) and not overwrite:
        error_msg = f'Output file "{output_path}" already exists.'
        raise FileExistsError(error_msg)

    # OPTIONAL
    # validating input / output file types
    get_suffix = lambda x: x.rsplit('.', 1)[-1]
    input_suffix = get_suffix(input_path)
    output_suffix = get_suffix(output_path)
    supported_input_types = {'jpg','png','bmp','ico',''}
    supported_output_types = {'png','bmp'}
    if input_suffix not in supported_input_types:
        error_msg = f'Unsupported file type for PIL: {input_suffix}'
        raise TypeError(error_msg)
    if output_suffix not in supported_output_types:
        warning_msg = f'Unsupported file type for steganography algorithms: {output_suffix}'
        warnings.warn(warning_msg)

    with Image.open(input_path) as im_input:
        array_image = np.asarray(im_input)
        array_image = array_image.astype('uint8')

    with Image.fromarray(array_image) as im_output:
        im_output.save(output_path)

    vprint(f'Converted image written to:\n{output_path}')
    return None
