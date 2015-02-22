import pygame, environment, sys

def main(fps, scene):
	#you need this to use anything in pygame
	pygame.init()
	done = False
	clock = pygame.time.Clock()
	
	#game loop
	while not done:
		scene.process_input()
		scene.update()
		scene.render()
		pygame.display.flip()
		clock.tick(fps)
	
	#shuts down pygame... supposedly
	pygame.quit()
	
if __name__ == '__main__':
	main(60, environment.Environment())