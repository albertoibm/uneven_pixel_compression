from sys import argv
from misc import init_globals
from PIL import Image
init_globals()
fname = argv[1]
fopen = open(fname,'r')
strfile = ""
for linea in fopen:
    strfile += linea
from codec import decode_file, to_string
W,H,blocks = decode_file(strfile)
Image.frombytes("RGB",(W,H),to_string(blocks,(W,H))).show()
