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
			
class OverworldSprite(guiElement):
	def __init__(self,x,y,imagename):
		guiElement.__init__(self)
		self.image = pygame.image.load(imagename)
		self.width, self.height = self.image.get_size()
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		
	def sprite_sheet(self,size,file,pos=(0,0)):

		#Initial Values
		len_sprt_x,len_sprt_y = size #sprite size
		sprt_rect_x,sprt_rect_y = pos #where to find first sprite on sheet
		print "%d %d" %(len_sprt_x, len_sprt_y)
		sheet = pygame.image.load(file).convert_alpha() #Load the sheet
		sheet_rect = sheet.get_rect()
		sprites = []
		print sheet_rect.height, sheet_rect.width
		for i in range(0,sheet_rect.height-len_sprt_y,41):#rows
			print "row"
			for j in range(0,sheet_rect.width-len_sprt_x,71):#columns
				print "column"
				print sprt_rect_x, sprt_rect_y
				sheet.set_clip(pygame.Rect(sprt_rect_x, sprt_rect_y, len_sprt_x, len_sprt_y)) #find sprite you want
				sprite = sheet.subsurface(sheet.get_clip()) #grab the sprite you want
				sprites.append(sprite)
				sprt_rect_x += 71

			sprt_rect_y += 41
			sprt_rect_x = 0
		self.sprites = sprites
		
	def move(self,x,y):
		self.rect.x += x
		#left
		if x < 0:
			self.image = self.sprites[8]
		#right
		elif x > 0:
			self.image = self.sprites[24]
		#screen border collision
		if self.rect.x < 0:
			self.rect.x = 0
		elif self.rect.x >= (graphics.SCWIDTH-self.width):
			self.rect.x = (graphics.SCWIDTH-self.width)
		self.rect.y += y
		#down
		if y > 0:
			self.image = self.sprites[16]
		#up
		elif y < 0:
			self.image = self.sprites[0]
		if self.rect.y < 0:
			self.rect.y = 0
		elif self.rect.y >= (graphics.SCHEIGHT-self.height):
			self.rect.y = (graphics.SCHEIGHT-self.height)
