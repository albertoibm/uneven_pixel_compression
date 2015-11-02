from misc import *
from math import log,ceil
import numpy
from PIL import Image
def to_string(blocks,size):
    imgarray = numpy.array(Image.new("RGB",size))
    for b in blocks:
        imgarray[b.y:b.y+b.height,b.x:b.x+b.width]=b.colour
    return Image.fromarray(imgarray).tobytes()
def bitlen(n):
    return int(ceil(log(n+1,2)))
def encode_file(size, blocks):
    L = len(blocks)
    minbithor = bitlen(size[0])
    minbitver = bitlen(size[1])
    bksz = minbithor * 2 + minbitver * 2 + 24
    header = [0x20,0xb2,0x49,0x4d,0x47,size[0]>>8,size[0]&0xff,\
            size[1]>>8,size[1]&0xff, bksz,\
                L>>24, L>>16&0xff, L>>8&0xff, L&0xff,\
                0xbe, 0x70]
    if bksz * L > size[0] * size[1] * 24:
        print "WARNING: The file size is going to be higher than an uncompressed image"
        print "Do you want to continue? (y/N) "
        if raw_input().upper() != 'Y':
            return 0
    filestr = ''.join(map(chr,header))
    towrite = "" ## string based
    for b in blocks:
        ## Using strings instead of ints cause the bits that are left for the next loop are dropped if they are 0. information is lost
        if debug:
            print b.x,b.y,b.width,b.height,b.colour[0],b.colour[1],b.colour[2]
        towrite += format(b.x,'0%db'%minbithor)
        towrite += format(b.y,'0%db'%minbitver)
        towrite += format(b.width,'0%db'%minbithor)
        towrite += format(b.height,'0%db'%minbitver)
        towrite += format(b.colour[0],'08b')
        towrite += format(b.colour[1],'08b')
        towrite += format(b.colour[2],'08b')
        while len(towrite) >= 8:
            filestr += chr(int(towrite[:8],2))
            towrite = towrite[8:]
    filestr += chr(0xbe)+chr(0x71)
    return filestr
def decode_file(str_file):
    header = str_file[:16]
    str_file = str_file[16:]
    if not header.startswith(' \xb2IMG'):
        print "File is not DPI type"
        return 0
    header = map(ord,header)
    W = (header[5]<<8) + header[6]
    H = (header[7]<<8) + header[8]
    bksz = header[9]
    nblocks = (header[10]<<24) + (header[11]<<16) + (header[12]<<8) + header[13]
    mbh = bitlen(W)
    mbv = bitlen(H)
    blocks = []
    bits = ""
    j = 0
    if verbose:
        print "Block size: %d"%bksz
        print "Number of blocks: %d"%nblocks
        print "Image width: %d"%W
        print "Image height: %d"%H
    if (header[14]<<8) + header[15] != 0xbe70:
        print "Something went wrong with the header"
        return 0
    for i in range(nblocks):
        while len(bits) < bksz:
            bits += format(ord(str_file[j]),'08b')
            j += 1
        x = int(bits[:mbh],2)
        y = int(bits[mbh:mbh+mbv],2)
        width = int(bits[mbh+mbv:2*mbh+mbv],2)
        height = int(bits[2*mbh+mbv:2*(mbh+mbv)],2)
        r = int(bits[bksz-24:bksz-16],2)
        g = int(bits[bksz-16:bksz-8],2)
        b = int(bits[bksz-8:bksz],2)
        if debug:
            print x,y,width,height,r,g,b
        blocks.append(Bloque((x,y),(width,height),colour=(r,g,b)))
        bits = bits[bksz:]
    if (ord(str_file[j])<<8)+ord(str_file[j+1]) != 0xbe71:
        print "Something went wrong."
        if debug:
            print map(hex,map(ord,str_file[-10:]))
    return W,H,blocks
