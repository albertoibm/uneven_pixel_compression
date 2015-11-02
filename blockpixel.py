from PIL import Image
from misc import *
init_globals()
import numpy
from sys import argv,exit,stdout
from visualizer import Pantalla
from math import log,ceil
from codec import *

if __name__=='__main__':
	treshold=500
        minsize = 4
	if len(argv)<2:
            print "Usage: blockpixel <OPTIONS> Image"
            print ""
            print "OPTIONS"
            print "-t threshold\tSet a threshold to divide the pixel (Default %d)"%treshold
            print "-m minsize\tSet the minimum size of a pixel (default %d)"%minsize
            print "-v\tVerbose mode"
            print "-V\tVisualize pixel division"
	    exit()
        ## ARGUMENTS
	if '-t' in argv:
		treshold = int(argv[argv.index('-t') + 1])
	if '-m' in argv:
		minsize = int(argv[argv.index('-m') + 1])
        visualize = '-V' in argv
        verbose = '-v' in argv
        debug = '-d' in argv

	imgfile=argv[-1]
	img=Image.open(imgfile)
        if visualize:
            screen = Pantalla(img.size[0],img.size[1])
	imgarray=numpy.array(img)
	
	bloques=[Bloque([0,0],img.size,numpy.array(img),\
		div='v' if img.size[1]>img.size[0] else 'h')]
	i=0
        if verbose:
            stdout.write("Creating pixels...")
            stdout.flush()
	while i<len(bloques):# and i < 10:
		if bloques[i].getVar() > treshold and bloques[i].area >= minsize:
			bloques.append(bloques[i].hijo())
			bloques[i].dividir()
		else:i+=1
        if verbose:
            print "done!"
        fname = imgfile.split('.')[0]+'.dpi'
        fopen = open(fname, 'w')
        for char in encode_file(img.size, bloques):
            fopen.write(char)
        fopen.close()
#	fopen=open(argv[1].split('.')[0]+'.dpi','w')
#	fopen.write('%d,%d,'%(img.size[0],img.size[1]))
        if verbose and visualize:
            stdout.write("Drawing image...")
            stdout.flush()
	imgarray-=imgarray
        for b in bloques:
                imgarray[b.y:b.y+len(b.imgarr),b.x:b.x+b.width]=b.colour
                if visualize:
                    screen.drawimg(Image.fromarray(imgarray))
#		fopen.write('%d,%d,%d,%d,%d,%d,%d,'%(b.x,b.y,b.width,b.height,\
#			b.colour[0],b.colour[1],b.colour[2]))
#	fopen.close()
        if verbose:
            if visualize:
                print "done!"
            print len(bloques),"bloques"
	img2=Image.fromarray(imgarray)
	img.show()
	img2.show()
