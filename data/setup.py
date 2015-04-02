import os
import pygame
from . import tools
from . import constants as c

GAME = 'BEGIN GAME'

ORIGINAL_CAPTION = 'Project Cacophonum'

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
pygame.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pygame.display.set_mode((960, 640))
SCREEN_RECT = SCREEN.get_rect()

FONTS = tools.load_all_fonts(os.path.join('resources', 'fonts'))
MUSIC = tools.load_all_music(os.path.join('resources', 'music'))
GFX = tools.load_all_gfx(os.path.join('resources', 'graphics'))
SFX = tools.load_all_sfx(os.path.join('resources', 'sound'))
TMX = tools.load_all_tmx(os.path.join('resources', 'tmx'))

FONT = pygame.font.Font(FONTS['Fixedsys500c'], 20)



