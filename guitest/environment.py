import pygame
import graphics
import guiBase

class SceneBase():
	def __init__(self):
		self.next = self
	
	def process_input(self):
		pass
		
	def update(self):
		pass
	
	def render(self):
		pass
	
	def terminate(self):
		pygame.quit()

class Environment(SceneBase):
	
	def __init__(self):
		SceneBase.__init__(self)
		# creates a surface; this will be the first layer, at the very back
		self.surface = graphics.SCREEN
		self.mapgraphic = pygame.image.load("Bazaar.jpg").convert()
		# simply throw objects into a Group of sprites and they'll be drawn when you render them later
		self.gui_group = pygame.sprite.Group()
		self.spr1 = guiBase.OverworldSprite(0,0,"Ape.png")
		self.gui_group.add(self.spr1)
		
	def process_input(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.spr1.move(0,-32)
				elif event.key == pygame.K_DOWN:
					self.spr1.move(0,32)
				if event.key == pygame.K_LEFT:
					self.spr1.move(-32,0)
				elif event.key == pygame.K_RIGHT:
					self.spr1.move(32,0)
			if event.type == pygame.QUIT:
				self.terminate()
				
	def update(self):
		pass
		
	def render(self):
		#redraw map
		self.surface.blit(self.mapgraphic,(0,0))
		#draw objects in the group on the BG we created
		self.gui_group.draw(self.surface)
		
		#next frame ikuze!
		pygame.display.flip()
