__author__ = 'justinarmstrong'

import os, random, copy
import pygame as pg
from . import constants as c
from entityclasses import *
from compositeclasses import *

class Control(object):
    """
    Control class for entire project.  Contains the game loop, and contains
    the event_loop which passes events to States as needed.  Logic for flipping
    states is also found here.
    """
    def __init__(self, caption):
        self.screen = pg.display.get_surface()
        self.done = False
        self.clock = pg.time.Clock()
        self.caption = caption
        self.fps = 60
        self.show_fps = False
        self.current_time = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.set_music()

    def update(self):
        self.current_time = pg.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        previous_music = self.state.music_title
        persist = self.state.cleanup()
        if self.state_name == 'battle':
            monlist = self.state.encounters
            self.state = self.state_dict[self.state_name](monlist)
        else:
            self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.previous_music = previous_music
        self.state.startup(self.current_time, persist)
        self.set_music()

    def set_music(self):
        """
        Set music for the new state.
        """
        if self.state.music_title == self.state.previous_music:
            pass
        elif self.state.music:
            pg.mixer.music.load(self.state.music)
            pg.mixer.music.set_volume(self.state.volume)
            pg.mixer.music.play(-1)

    def event_loop(self):
        self.events = pg.event.get()

        for event in self.events:
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
                self.state.get_event(event)
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
                self.state.get_event(event)

    def toggle_show_fps(self, key):
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(self.caption)

    def main(self):
        """Main loop for entire program"""
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pg.display.set_caption(with_fps)


class _State(object):
    """Base class for all game states"""
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.game_data = {}
        self.music = None
        self.music_title = None
        self.previous_music = None

    def get_event(self, event):
        pass

    def startup(self, current_time, game_data):
        self.game_data = game_data
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.game_data

    def update(self, surface, keys, current_time):
        pass


def load_all_gfx(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp')):
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pg.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name] = img
    return graphics


def load_all_music(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    songs = {}
    for song in os.listdir(directory):
        name, ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_fonts(directory, accept=('.ttf')):
    return load_all_music(directory, accept)


def load_all_tmx(directory, accept=('.tmx')):
    return load_all_music(directory, accept)


def load_all_sfx(directory, accept=('.wav','.mp3','.ogg','.mdi')):
    effects = {}
    for fx in os.listdir(directory):
        name, ext = os.path.splitext(fx)
        if ext.lower() in accept:
            effects[name] = pg.mixer.Sound(os.path.join(directory, fx))
    return effects


def get_image(x, y, width, height, sprite_sheet):
    """Extracts image from sprite sheet"""
    image = pg.Surface([width, height])
    rect = image.get_rect()

    image.blit(sprite_sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(c.BLACK)

    return image

def get_tile(x, y, tileset, width=16, height=16, scale=1):
    """Gets the surface and rect for a tile"""
    surface = get_image(x, y, width, height, tileset)
    surface = pg.transform.scale(surface, (int(width*scale), int(height*scale)))
    rect = surface.get_rect()

    tile_dict = {'surface': surface,
                 'rect': rect}

    return tile_dict

def notify_observers(self, event):
    """
    Notify all observers of events.
    """
    for each_observer in self.observers:
        each_observer.on_notify(event)

def create_game_data_dict():
    """Create a dictionary of persistant values the player
    carries between states"""
    
    players = [Conductor("Hanami Otozono")]
    monsters = [copy.deepcopy(TamedMonster("Ichiro", "Kobold", 1))]
    players[0].addMonster(monsters[0])
    monsters[0].setMaster(players[0]) 
    monsters[0].addSpell(copy.deepcopy(Spell("Black Aria", 1)))
    players[0].addItem(copy.deepcopy(Consumable("Potion", 1)))
    players[0].addItem(copy.deepcopy(Instrument("Flute", 1)))
    monsters[0].equip(copy.deepcopy(Instrument("Flute", 1)),"instrument")
    
    '''
    players.append(Conductor("Gir-Nas"))
    monsters.append(copy.deepcopy(TamedMonster("Naraka", "Kobold", 1)))
    players[1].addMonster(monsters[1])
    monsters[1].setMaster(players[1]) 
    monsters[1].addSpell(copy.deepcopy(Spell("Black Aria", 1)))
    players[1].addItem(copy.deepcopy(Consumable("Potion", 1)))
    players[1].addItem(copy.deepcopy(Instrument("Flute", 1)))
    monsters.append(copy.deepcopy(TamedMonster("Kyouki", "Kobold", 1)))
    players[0].addMonster(monsters[2])
    monsters[2].setMaster(players[0])

    players[0].addItem(copy.deepcopy(Instrument("Gria Auliet", 1)))
    players[0].addItem(copy.deepcopy(Instrument("Gria Auliet", 1)))
    players[0].addItem(copy.deepcopy(Instrument("Gria Auliet", 1)))
    players[0].addItem(copy.deepcopy(Instrument("Flute", 1)))
    players[0].addItem(copy.deepcopy(Instrument("Gria Auliet", 1)))
    players[0].addItem(copy.deepcopy(Instrument("Flute", 1)))
    '''
    

    player_items = []
    for x in range(7):
        player_items.append(copy.deepcopy(Consumable("Potion", 1)))
    
    treasure_flags = {'FL1': False}
    
    event_flags = {'start of game': True}


    data_dict = {'last location': None,
                 'last state': None,
                 'last direction': 'down',
                 'player inventory': player_items,
                 'conductors': players,
                 'gold': 400,
                 'battle counter': 50,
                 'start of game': True,
                 'treasure flags': treasure_flags,
                 'event flags': event_flags
    }

    return data_dict







