"""
This is the base class for all level states (i.e. states
where the player can move around the screen).  Levels are
differentiated by self.name and self.tmx_map.
This class inherits from the generic state class
found in the tools.py module.
"""
import copy, sys
import pygame as pg
from .. import tools, collision
from .. import constants as c
from .. components import person, textbox, portal
from . import player_menu
from .. import tilerender
from .. import setup


#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    range = xrange


class LevelState(tools._State):
    def __init__(self, name, battles=False):
        super(LevelState, self).__init__()
        self.name = name
        self.tmx_map = setup.TMX[name]
        self.allow_battles = battles
        self.music_title = None
        self.previous_music = None
        self.music = None
        self.volume = None
        self.portal = None

    def startup(self, current_time, game_data):
        """
        Call when the State object is flipped to.
        """
        self.game_data = game_data
        self.music, self.volume = self.set_music()
        self.current_time = current_time
        self.state = 'transition_in'
        self.reset_dialogue = ()
        self.switch_to_battle = False
        self.use_portal = False
        self.allow_input = False
        self.cut_off_bottom_map = ['castle', 'town', 'dungeon']
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_2x_map()

        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = self.make_level_surface(self.map_image)
        self.level_rect = self.level_surface.get_rect()
        self.portals = self.make_level_portals()
        self.player = self.make_player()
        self.blockers = self.make_blockers()
        self.sprites = self.make_sprites()
        self.triggers = self.make_triggers()
        self.encounters = self.make_encounterlist()

        self.collision_handler = collision.CollisionHandler(self.player,
                                                            self.blockers,
                                                            self.sprites,
                                                            self.portals,
                                                            self)
        self.dialogue_handler = textbox.TextHandler(self)
        self.state_dict = self.make_state_dict()
        self.menu_screen = player_menu.Player_Menu(game_data, self)
        self.transition_rect = setup.SCREEN.get_rect()
        self.transition_alpha = 255

    def set_music(self):
        """
        Set music based on name.
        """
        music_dict = {c.FAESLANDING: ('faeslanding', 2),
                      c.OVERWORLD: ('nikko', .8),
                      c.SOUTHFIELD: ('nikko', .8),
                      c.WESTFIELD: ('nikko', .8),
                      c.CASTLE: ('faeslanding', .8),
                      c.DUNGEON: ('dungeon_theme', .4),
                      c.DUNGEON2: ('dungeon_theme', .4),
                      c.DUNGEON3: ('dungeon_theme', .4),
                      c.DUNGEON4: ('dungeon_theme', .4),
                      c.DUNGEON5: ('dungeon_theme', .4),
                      c.HOUSE: ('pleasant_creek', .1),
                      c.BROTHER_HOUSE: ('pleasant_creek', .1)}
        
        """
        if self.game_data['crown quest'] and (self.name == c.TOWN or self.name == c.CASTLE):
            self.music_title = 'kings_theme'
            return setup.MUSIC['kings_theme'], .4
        """
        if self.name in music_dict:
            music = music_dict[self.name][0]
            volume = music_dict[self.name][1]
            self.music_title = music
            return setup.MUSIC[music], volume
        else:
            return None, None

    def make_viewport(self, map_image):
        """
        Create the viewport to view the level through.
        """
        map_rect = map_image.get_rect()
        return setup.SCREEN.get_rect(bottom=map_rect.bottom)

    def make_level_surface(self, map_image):
        """
        Create the surface all images are blitted to.
        """
        map_rect = map_image.get_rect()
        map_width = map_rect.width
        if self.name in self.cut_off_bottom_map:
            map_height = map_rect.height - 32
        else:
            map_height = map_rect.height
        size = map_width, map_height

        return pg.Surface(size).convert()

    def make_encounterlist(self):
        mon_list = []
        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'monster':
                mon_list.append(properties['monname'])
        #print mon_list
        return mon_list
    
    def make_player(self):
        """
        Make the player and sets location.
        """
        last_state = self.previous

        if last_state == 'battle':
            player = person.Player(self.game_data['last direction'], self.game_data)
            player.rect.x = self.game_data['last location'][0] * 32
            player.rect.y = self.game_data['last location'][1] * 32

        else:
            for object in self.renderer.tmx_data.getObjects():
                properties = object.__dict__
                if properties['name'] == 'start point':
                    #print "%s %s" %(last_state, properties['state'])
                    if last_state == properties['state']:
                        posx = properties['x'] * 2
                        posy = (properties['y'] * 2) - 32
                        player = person.Player(properties['direction'],
                                               self.game_data)
                        player.rect.x = posx
                        player.rect.y = posy

        return player

    def make_blockers(self):
        """
        Make the blockers for the level.
        """
        blockers = []

        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'blocker':
                left = properties['x'] * 2
                top = ((properties['y']) * 2) - 32
                blocker = pg.Rect(left, top, 32, 32)
                blockers.append(blocker)

        return blockers
    
    def make_triggers(self):
        """
        Make the cutscene triggers for the level.
        """
        triggers = pg.sprite.Group()
        
        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'trigger':
                left = properties['x'] * 2
                top = ((properties['y']) * 2) - 32
                trigger = person.Trigger(left,top)
                dialogue_list = []
                for i in range(int(properties['dialogue length'])):
                    dialogue_list.append(properties['dialogue'+str(i)])
                    trigger.dialogue = dialogue_list
                triggers.add(trigger)
        return triggers

    def make_sprites(self):
        """
        Make any sprites for the level as needed.
        """
        sprites = pg.sprite.Group()

        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'sprite':
                if 'direction' in properties:
                    direction = properties['direction']
                else:
                    direction = 'down'

                if properties['type'] == 'soldier' and direction == 'left':
                    index = 1
                else:
                    index = 0

                if 'item' in properties:
                    item = properties['item']
                else:
                    item = None

                if 'id' in properties:
                    id = properties['id']
                else:
                    id = None

                if 'battle' in properties:
                    battle = properties['battle']
                else:
                    battle = None

                if 'state' in properties:
                    sprite_state = properties['state']
                else:
                    sprite_state = None


                x = properties['x'] * 2
                y = ((properties['y']) * 2) - 32

                sprite_dict = {'oldman': person.Person('oldman',
                                                       x, y, direction),
                               'bluedressgirl': person.Person('femalevillager',
                                                              x, y, direction,
                                                              'resting', 1),
                               'femalewarrior': person.Person('femvillager2',
                                                              x, y, direction,
                                                              'autoresting'),
                               'devil': person.Person('devil', x, y,
                                                      'down', 'autoresting'),
                               'oldmanbrother': person.Person('oldmanbrother',
                                                              x, y, direction),
                               'soldier': person.Person('soldier',
                                                        x, y, direction,
                                                        'resting', index),
                               'king': person.Person('king', x, y, direction),
                               'evilwizard': person.Person('evilwizard', x, y, direction),
                               'treasurechest': person.Chest(x, y, id),
                               'Orthrus': person.Person('Orthrus', x, y, direction)}

                sprite = sprite_dict[properties['type']]
                if sprite_state:
                    sprite.state = sprite_state

                if sprite.name == 'oldman':
                    if self.game_data['old man gift'] and not self.game_data['elixir received']:
                        sprite.item = self.game_data['old man gift']
                    else:
                        sprite.item = item
                elif sprite.name == 'king':
                    if not self.game_data['talked to king']:
                        sprite.item = self.game_data['king item']
                else:
                    sprite.item = item
                sprite.battle = battle
                self.assign_dialogue(sprite, properties)
                self.check_for_opened_chest(sprite)
                if sprite.name == 'evilwizard' and self.game_data['crown quest']:
                    pass
                else:
                    sprites.add(sprite)

        return sprites

    def assign_dialogue(self, sprite, property_dict):
        """
        Assign dialogue from object property dictionaries in tmx maps to sprites.
        """
        dialogue_list = []
        item_list = []
        monster_list = []
        diaindex = 0
        
        #check each event flag set to pick which dialogue index to use
        
        for i in range(int(property_dict['dialogue_indices'])):
            bool = True
            diaindex = i
            for j in range(int(property_dict.get(('dialogue_'+str(i)+'_numflags'), 0))):
                temp = property_dict['dialogue_'+str(i)+'_flags_'+str(j)]
                if temp.startswith('not '):
                    temp = temp[4:]
                    bool &= not self.game_data['event flags'].get(temp, False)
                else:
                    bool &= self.game_data['event flags'].get(temp, False)
            if bool is True:
                break
                
        for i in range(int(property_dict.get(('dialogue_'+str(diaindex)+'_numitems'), 0))):
            item_list.append(property_dict['dialogue_'+str(diaindex)+'_item_'+str(i)])
            sprite.item = item_list
            
        for i in range(int(property_dict.get(('dialogue_'+str(diaindex)+'_battlemonnum'), 0))):
            monster_list.append(property_dict['dialogue_'+str(diaindex)+'_battle_'+str(i)])
            sprite.battle = monster_list
            
        for i in range(int(property_dict.get(('dialogue_'+str(diaindex)+'_numaddflags'), 0))):
            temp = property_dict['dialogue_'+str(diaindex)+'_addflags_'+str(i)]
            if temp in self.game_data['event flags']:
                if temp.startswith("false_"):
                    temp = temp[6:]
                    self.game_data['event flags'][temp] = False
                else:
                    self.game_data['event flags'][temp] = True

        for i in range(int(property_dict['dialogue_'+str(diaindex)+'_length'])):
            dialogue_list.append(property_dict['dialogue_'+str(diaindex)+'_'+str(i)])
            sprite.dialogue = dialogue_list
        
        """
        TODO: add code to read the ff:
        [x] dialogue_indices = how many dialogue options there are
        [x] dialogue_#_numflags = how many flags there are to activate this dialogue branch (add "not " prefix to check for falseness)
        [x] dialogue_#_flags_# = name of each event flag to check, e.g. "killed the boss"
        [x] dialogue_#_length = length of dialogue branch
        [x] dialogue_#_numitems = how many items the NPC/event trigger will give you when the dialogue is finished
        [x] dialogue_#_item_# = name of each item, e.g. "Potion"
        [x] dialogue_#_numaddflags = how many event flags will be tripped at the end of the dialogue
        [x] dialogue_#_addflags_# = name of each event (add "false_" prefix to make it false instead)
        [x] dialogue_#_battlemonnum = number of monsters to be battled at the end of this dialogue
        [x] dialogue_#_battle_# = name of each monster, e.g. "Slime"
        [x] dialogue_#_# = each line in the dialogue branch
        """


    def check_for_opened_chest(self, sprite):
        if sprite.name == 'treasurechest':
            if not self.game_data['treasure{}'.format(sprite.id)]:
                sprite.dialogue = ['Empty.']
                sprite.item = None
                sprite.index = 1

    def make_state_dict(self):
        """
        Make a dictionary of states the level can be in.
        """
        state_dict = {'normal': self.running_normally,
                      'dialogue': self.handling_dialogue,
                      'menu': self.goto_menu,
                      'transition_in': self.transition_in,
                      'transition_out': self.transition_out,
                      'slow transition out': self.slow_fade_out}

        return state_dict

    def make_level_portals(self):
        """
        Make the portals to switch state.
        """
        portal_group = pg.sprite.Group()

        for object in self.renderer.tmx_data.getObjects():
            properties = object.__dict__
            if properties['name'] == 'portal':
                posx = properties['x'] * 2
                posy = (properties['y'] * 2) - 32
                new_state = properties['type']
                portal_group.add(portal.Portal(posx, posy, new_state))


        return portal_group

    def running_normally(self, surface, keys, current_time):
        """
        Update level normally.
        """
        self.check_for_dialogue()
        self.player.update(keys, current_time)
        self.sprites.update(current_time)
        self.collision_handler.update(keys, current_time)
        self.check_for_battle()
        self.check_for_portals()
        self.check_for_end_of_game()
        self.dialogue_handler.update(keys, current_time)
        self.check_for_menu(keys)
        self.viewport_update()
        self.draw_level(surface)

    def check_for_portals(self):
        """
        Check if the player walks into a door, requiring a level change.
        """
        if self.use_portal and not self.done:
            self.player.location = self.player.get_tile_location()
            self.update_game_data()
            self.next = self.portal
            self.state = 'transition_out'

    def check_for_battle(self):
        """
        Check if the flag has been made true, indicating
        to switch state to a battle.
        """
        if self.switch_to_battle and self.allow_battles and not self.done:
            self.player.location = self.player.get_tile_location()
            self.update_game_data()
            self.next = 'battle'
            self.state = 'transition_out'

    def check_for_menu(self, keys):
        """
        Check if player hits enter to go to menu.
        """
        if keys[pg.K_RETURN] and self.allow_input:
            if self.player.state == 'resting':
                self.state = 'menu'
                self.allow_input = False

        if not keys[pg.K_RETURN]:
            self.allow_input = True


    def update_game_data(self):
        """
        Update the persistant game data dictionary.
        """
        self.game_data['last location'] = self.player.location
        self.game_data['last direction'] = self.player.direction
        self.game_data['last state'] = self.name
        self.set_new_start_pos()

    def check_for_end_of_game(self):
        """
        Switch scene to credits if main quest is complete.
        """
        """
        if self.game_data['delivered crown']:
            self.next = c.CREDITS
            self.state = 'slow transition out'
        """
        pass

    def set_new_start_pos(self):
        """
        Set new start position based on previous state.
        """
        location = copy.deepcopy(self.game_data['last location'])
        direction = self.game_data['last direction']

        if self.next == 'player menu':
            pass
        elif direction == 'up':
            location[1] += 1
        elif direction == 'down':
            location[1] -= 1
        elif direction == 'left':
            location[0] += 1
        elif direction == 'right':
            location[0] -= 1

    def handling_dialogue(self, surface, keys, current_time):
        """
        Update only dialogue boxes.
        """
        self.dialogue_handler.update(keys, current_time)
        self.draw_level(surface)

    def goto_menu(self, surface, keys, *args):
        """
        Go to menu screen.
        """
        self.menu_screen.update(surface, keys)
        self.menu_screen.draw(surface)

    def check_for_dialogue(self):
        """
        Check if the level needs to freeze.
        """
        if self.dialogue_handler.textbox:
            self.state = 'dialogue'

    def transition_out(self, surface, *args):
        """
        Transition level to new scene.
        """
        transition_image = pg.Surface(self.transition_rect.size)
        transition_image.fill(c.TRANSITION_COLOR)
        transition_image.set_alpha(self.transition_alpha)
        self.draw_level(surface)
        surface.blit(transition_image, self.transition_rect)
        self.transition_alpha += c.TRANSITION_SPEED
        if self.transition_alpha >= 255:
            self.transition_alpha = 255
            self.done = True

    def slow_fade_out(self, surface, *args):
        """
        Transition level to new scene.
        """
        transition_image = pg.Surface(self.transition_rect.size)
        transition_image.fill(c.TRANSITION_COLOR)
        transition_image.set_alpha(self.transition_alpha)
        self.draw_level(surface)
        surface.blit(transition_image, self.transition_rect)
        self.transition_alpha += 2
        if self.transition_alpha >= 255:
            self.transition_alpha = 255
            self.done = True

    def transition_in(self, surface, *args):
        """
        Transition into level.
        """
        self.viewport_update()
        transition_image = pg.Surface(self.transition_rect.size)
        transition_image.fill(c.TRANSITION_COLOR)
        transition_image.set_alpha(self.transition_alpha)
        self.draw_level(surface)
        surface.blit(transition_image, self.transition_rect)
        self.transition_alpha -= c.TRANSITION_SPEED 
        if self.transition_alpha <= 0:
            self.state = 'normal'
            self.transition_alpha = 0

    def update(self, surface, keys, current_time):
        """
        Update state.
        """
        state_function = self.state_dict[self.state]
        state_function(surface, keys, current_time)

    def viewport_update(self):
        """
        Update viewport so it stays centered on character,
        unless at edge of map.
        """
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)

    def draw_level(self, surface):
        """
        Blit all images to screen.
        """
        self.level_surface.blit(self.map_image, self.viewport, self.viewport)
        self.level_surface.blit(self.player.image, self.player.rect)
        self.sprites.draw(self.level_surface)

        surface.blit(self.level_surface, (0, 0), self.viewport)
        self.dialogue_handler.draw(surface)
















