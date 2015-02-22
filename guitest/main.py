import pygame, environment, sys

def main(fps, scene):
	pygame.init()
	done = False
	clock = pygame.time.Clock()
	
	while not done:
		scene.process_input()
		scene.update()
		scene.render()
		pygame.display.flip()
		clock.tick(fps)
	pygame.quit()
	
if __name__ == '__main__':
	main(60, environment.Environment())