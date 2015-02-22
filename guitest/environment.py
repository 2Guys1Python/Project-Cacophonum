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
		self.surface.fill((0,0,250))
		# simply throw objects into a Group of sprites and they'll be drawn when you render them later
		self.gui_group = pygame.sprite.Group()
		self.square = guiBase.Square(40,40,40,40,(0,0,0))
		self.gui_group.add(self.square)
		
	def process_input(self):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.square.move(0,-40)
				elif event.key == pygame.K_DOWN:
					self.square.move(0,40)
				if event.key == pygame.K_LEFT:
					self.square.move(-40,0)
				elif event.key == pygame.K_RIGHT:
					self.square.move(40,0)
			if event.type == pygame.QUIT:
				self.terminate()
				
	def update(self):
		pass
		
	def render(self):
		#redraw BG
		self.surface.fill((0,0,250))
		#self.surface.blit(self.square.image, (self.square.rect.x, self.square.rect.y)) <<< idk what this does so I took it out until further notice
		
		#draw objects in the group on the BG we created
		self.gui_group.draw(self.surface)
		
		#next frame ikuze!
		pygame.display.flip()
