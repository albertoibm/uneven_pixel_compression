import numpy
def init_globals():
    global verbose
    global debug
    verbose = False
    debug = False
class Bloque:
	def __init__(self,xy,size,imgarr=[],div='h',colour=0):
		self.div=div
		self.x=xy[0]
		self.y=xy[1]
		self.width=size[0]
		self.height=size[1]
		self.area=self.getArea()
		self.imgarr=imgarr
                if not colour:
                    self.colour = self.getColour()
                else:
                    self.colour = colour
		self.hijo
	def getArea(self):
		return self.width*self.height
	def hijo(self):
		if self.div=='h':
			return Bloque((self.x+int(round(self.width/2.)),self.y),\
				(self.width/2,self.height),div='v',\
				imgarr=self.imgarr[:,int(round(self.width/2.)):])
		elif self.div=='v':
			return Bloque((self.x,self.y+int(round(self.height/2.))),\
				(self.width,self.height/2),div='h',\
				imgarr=self.imgarr[int(round(self.height/2.)):,:])
	def dividir(self):
		if self.div=='h':
			self.width=int(round(self.width/2.))
			self.imgarr=self.imgarr[:,:self.width]
			self.div='v'
		elif self.div=='v':
			self.height=int(round(self.height/2.))
			self.imgarr=self.imgarr[:self.height,:]
			self.div='h'
                ### They were inverted. Bug solved
		self.area=self.getArea()
		self.colour=self.getColour()
		
	def getColour(self):
                if self.area != 0:
       		    return self.imgarr.sum(axis=1).sum(axis=0)/(self.area)
                else:
                    return self.imgarr
	def getVar(self):
		return numpy.sum((self.imgarr-self.colour)**2)/self.area
	def getPix(self):
		return self.imgarr-self.imgarr+self.getColour()
