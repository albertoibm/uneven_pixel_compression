# Uneven pixels compression
The project consists of compressing images using pixels of different sizes. By doing so, several hundreds of pixels are cramped into a big one that is more or less the same color as the whole chunk.

The image is analised as candidate for a single big pixel using the variance of the color of the pixels. If the variance is greater than a certain threshold, then the candidate pixel is divided into two and each of them is analised and the process goes on until the pixels can't be split anymore.

The project contains five files: `blockpixel.py`, `codec.py`, `misc.py`, `visualizer.py` and `viewer.py`.

`codec.py` contains the functions used to write a compressed image into a file (e.g. `encode_file()`), 
to read the file and get the pixels that make the image (e.g. function `decode_file()`),
and to transform that list of big pixels into a string image (e.g. function `to_string()`).

`misc.py` initializes global variables and contains the class Bloque, which is what each pixel is represented with.

`visualizer.py` is used in case an *animation* of the pixels appearing in order is wanted. It depends on *pygame*.

`viewer.py` only displays a .dpi file.

The whole project uses PIL and numpy.

`blockpixel.py` is the main program. It takes up to five arguments and the image file to convert. The options it takes are:
-`-t value` for changing the threshold and get a more detailed image.
-`-m value` for changing the minimum size the pixels can take.
-`-v` for verbose mode.
-`-V` for visualization of the animation.
