import pygame

class Pantalla:
	def __init__(self,width,height):
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width,self.height))
		self.img = None
	def drawimg(self,img):
		self.img = pygame.image.fromstring(img.tobytes(),img.size,img.mode)
		self.screen.blit(self.img, (0,0))
		pygame.display.update()
