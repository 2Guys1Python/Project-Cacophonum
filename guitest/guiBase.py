import pygame
import graphics

class guiElement(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		

class Square(guiElement):
	def __init__(self, x, y, width, height, color):
		guiElement.__init__(self)
		self.width = width
		self.height = height
		self.color = color
		
		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def move(self,x,y):
		self.rect.x += x
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x >= (graphics.SCWIDTH-self.width):
			self.rect.x = (graphics.SCWIDTH-self.width)
		self.rect.y += y
		if self.rect.y < 0:
			self.rect.y = 0
		elif self.rect.y >= (graphics.SCHEIGHT-self.height):
			self.rect.y = (graphics.SCHEIGHT-self.height)