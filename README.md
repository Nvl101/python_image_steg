# python_image_steg
python image steganography scripts

### usage:
* ```steg.py```: writes file into an image. make sure you retain the original copy.
* ```unsteg.py```: input original image and steg image, it can retrieve the original file with filename.

### notes:
* Currently supports png and bmp formats. For jpeg file, need to convert using ```standard_convert_jpg_to_png.py```.
* Can steg one file into an image. Make sure the image is at least twice larger than your file.
