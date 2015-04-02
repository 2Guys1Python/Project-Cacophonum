import sys
import pygame
from data import setup
from data.main import main

if __name__ =='__main__':
    setup.GAME
    main()
    pygame.quit()
    sys.exit()
