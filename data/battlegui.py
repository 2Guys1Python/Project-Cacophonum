"""
GUI components for battle states.
"""
import sys
import pygame as pg
from . import setup, observer
from . import constants as c

#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    range = xrange

class InfoBox(object):
    """
    Info box that describes attack damage and other battle
    related information.
    """
    def __init__(self, game_data, experience, gold, playerentities, monsterentities, enemyentities):
        self.game_data = game_data
        self.enemy_damage = 0
        self.player_damage = 0
        self.index = 0
        self.state = c.ATTACK
        self.big_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 38)
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.title_font.set_underline(True)
        self.med_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 28)
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 18)
        self.experience_points = experience
        self.gold_earned = gold
        self.playerentities = playerentities
        self.monsterentities = monsterentities
        self.enemyentities = enemyentities
        self.currentmonster = 0
        self.enemyindex = 0
        self.playerindex = 0
        self.state_dict = self.make_state_dict()
        self.noteoff = [setup.GFX['8thnoteempty'], setup.GFX['wholenoteempty'], setup.GFX['gclefempty']]
        self.noteon = [setup.GFX['8thnotefilled'], setup.GFX['wholenotefilled'], setup.GFX['gcleffilled']]
        self.notecount = monsterentities[self.currentmonster].stats['curr']['notes']
        self.image = self.make_image()
        self.rect = self.image.get_rect(bottom=640)
        self.item_text_list = self.make_item_text()[1:]
        self.magic_text_list = self.make_magic_text()[1:]
        self.command_list = [c.ATTACK, c.SPELL, c.ITEM, c.SYMPHONY, c.WAIT, c.RUN_AWAY]
        self.itemindex = 0
        self.allow_input = True

    def make_state_dict(self):
        """
        Make dictionary of states Battle info can be in.
        """
        state_dict   = {c.ATTACK: 'ATTACK',
                        c.SPELL: 'SPELL',
                        c.ITEM: 'ITEM',
                        c.SYMPHONY: 'SYMPHONY',
                        c.WAIT: 'WAIT',
                        c.RUN_AWAY: 'RUN',
                        c.SELECT_ENEMY_ATTACK: 'ATTACK',
                        c.SELECT_ENEMY_SPELL: '',
                        c.ENEMY_ATTACK: self.player_hit(),
                        c.PLAYER_ATTACK: self.enemy_damaged(),
                        c.ENEMY_DAMAGED: self.enemy_damaged(),
                        c.ENEMY_DEAD: 'Enemy killed.',
                        c.PLAYER_DAMAGED: self.player_hit(),
                        c.DRINK_HEALING_POTION: 'Player healed.',
                        c.DRINK_ETHER_POTION: 'Magic Points Increased.',
                        c.OFF_SPELL: 'FIRE BLAST!',
                        c.BATTLE_WON: 'Battle won!',
                        c.SHOW_EXPERIENCE: self.show_experience(),
                        c.SHOW_GOLD: self.show_gold()}

        return state_dict
    
    def last_option(self):
        return self.state

    def check_input(self, keys):
        if self.allow_input:
            if keys[pg.K_RIGHT]:
                if self.state in self.command_list:
                    #self.notify(c.CLICK)
                    self.index += 1
                    if self.index > len(self.command_list)-1:
                        self.index = 0
                    self.state = self.command_list[self.index]
                    self.allow_input = False
            elif keys[pg.K_LEFT]:
                if self.state in self.command_list:
                    #self.notify(c.CLICK)
                    self.index -= 1
                    if self.index < 0:
                        self.index = len(self.command_list)-1
                    self.state = self.command_list[self.index]
                    self.allow_input = False


        if keys[pg.K_DOWN] == False and keys[pg.K_UP] == False \
                and keys[pg.K_RIGHT] == False and keys[pg.K_LEFT] == False:
            self.allow_input = True

    def enemy_damaged(self):
        """
        Return text of enemy being hit using calculated damage.
        """
        return "{} hit with {} damage. {}/{}".format(self.enemyentities[self.enemyindex].name,self.enemy_damage, self.enemyentities[self.enemyindex].stats['curr']['HP'] - self.enemy_damage, self.enemyentities[self.enemyindex].stats['base']['HP'] + self.enemyentities[self.enemyindex].stats['bonus']['bonusHP'] - self.enemyentities[self.enemyindex].stats['penalty']['penaltyHP'])

    def make_item_text(self):
        """
        Make the text for when the player selects items.
        """
        consum_list = []
        inventory = self.monsterentities[self.currentmonster].master.inventory
        
        for x in range(inventory.getSize()):
            if inventory.getItem(x).itemType is "Consumable":
                consum_list.append(inventory.getItem(x).name)

        return consum_list

    def make_magic_text(self):
        """
        Make the text for when the player selects magic.
        """
        inventory = self.game_data['player inventory']
        allowed_item_list = ['Fire Blast', 'Cure']
        title = 'SELECT MAGIC SPELL'
        magic_text_list = [title]
        spell_list = [item for item in inventory if item in allowed_item_list]
        magic_text_list.extend(spell_list)
        magic_text_list.append('BACK')
        
        magic_text_list = []
        for m in self.monsterentities[self.currentmonster].spells:
            magic_text_list.append(m.name)

        return magic_text_list

    def make_text_sprites(self, text_list):
        """
        Make sprites out of text.
        """
        sprite_group = pg.sprite.Group()

        for i, text in enumerate(text_list):
            sprite = pg.sprite.Sprite()

            if len(text_list)-(self.itemindex*4)>4:
                for x in range(4):
                    text = text_list[x+(self.itemindex*4)]
                    posx = 65
                    posy = 30 + (x*35)
                
            else:
                for x in range(len(text_list) - self.itemindex*4):
                    text = text_list[x+(self.itemindex*4)]
                    posx = 65
                    posy = 30 + (x*35)
            sprite.image = self.med_font.render(text, True, c.WHITE)
            sprite.rect = sprite.image.get_rect(x=posx, y=posy)
            sprite_group.add(sprite)
        
        
        return sprite_group
        
        

    def make_image(self):
        """
        Make image out of box and message.
        """
        image = setup.GFX['battlebox']
        rect = image.get_rect(bottom=640)
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))
        
        if self.state == c.SELECT_ITEM:
            text_sprites = self.make_text_sprites(self.make_item_text())
            text_sprites.draw(surface)
        elif self.state == c.SELECT_MAGIC:
            text_sprites = self.make_text_sprites(self.make_magic_text())
            text_sprites.draw(surface)
        elif self.state in (c.SHOW_EXPERIENCE, c.SHOW_GOLD, c.ENEMY_DAMAGED, c.PLAYER_DAMAGED, c.ENEMY_ATTACK, c.PLAYER_ATTACK, c.BATTLE_WON):
            text_surface = self.med_font.render(self.state_dict[self.state], True, c.WHITE)
            text_rect = text_surface.get_rect(x=300, y=75)
            text_rect.centerx = rect.centerx-10
            surface.blit(text_surface, text_rect)
        else:
            text_surface = self.big_font.render(self.state_dict[self.state], True, c.WHITE)
            text_rect = text_surface.get_rect(x=470, y=75)
            text_rect.centerx = rect.centerx+230
            surface.blit(text_surface, text_rect)
            text_surface = self.big_font.render(self.monsterentities[self.currentmonster].name, True, c.WHITE)
            text_rect = text_surface.get_rect(x=20,y=15)
            surface.blit(text_surface, text_rect)
            text_surface = self.font.render('(' + self.monsterentities[self.currentmonster].species + ')', True, c.WHITE)
            text_rect = text_surface.get_rect(x=text_rect.right+10, y=text_rect.centery-6)
            surface.blit(text_surface, text_rect)
            text_surface = self.med_font.render('Health: ' + str(self.monsterentities[self.currentmonster].stats['curr']['HP']) + '/' + str(self.monsterentities[self.currentmonster].stats['base']['HP'] + self.monsterentities[self.currentmonster].stats['bonus']['bonusHP'] - self.monsterentities[self.currentmonster].stats['penalty']['penaltyHP']), True, c.WHITE)
            text_rect = text_surface.get_rect(x=20,y=55)
            surface.blit(text_surface, text_rect)
            text_surface = self.med_font.render('Status: ' + str(self.monsterentities[self.currentmonster].stats['curr']['notes']) + " notes", True, c.WHITE)
            text_rect = text_surface.get_rect(x=20, y=90)
            surface.blit(text_surface, text_rect)

            for i in range(10):
                temppos = [(345, 33), (440,33), (440,98), (345,98), (394,23), (470, 78), (430, 143), (355,143), (315,78), (390,55)]
                if i < 4:
                    if i < self.notecount:
                        tempnote = self.noteon[0]
                    else:
                        tempnote = self.noteoff[0]
                elif i < 9:
                    if i < self.notecount:
                        tempnote = self.noteon[1]
                    else:
                        tempnote = self.noteoff[1]
                        
                else:
                    if i < self.notecount:
                        tempnote = self.noteon[2]
                    else:
                        tempnote = self.noteoff[2]
                
                temprect = tempnote.get_rect(x=temppos[i][0],y=temppos[i][1])
                
                surface.blit(tempnote, temprect)
            
        return surface

    def set_enemy_damage(self, enemy_damage):
        """
        Set enemy damage in state dictionary.
        """
        self.enemy_damage = enemy_damage
        self.state_dict[c.ENEMY_DAMAGED] = self.enemy_damaged()
    
    def set_enemy_index(self, enemy_index):
        self.enemyindex = enemy_index
        
    def set_player_damage(self, player_damage):
        """
        Set player damage in state dictionary.
        """
        self.player_damage = player_damage
        self.state_dict[c.PLAYER_DAMAGED] = self.player_hit()
    
    def set_player_index(self, player_index):
        self.playerindex = player_index

    def player_hit(self):
        if self.player_damage:
            return "{} hit with {} damage. {}/{}".format(self.monsterentities[self.playerindex].name, self.player_damage, self.monsterentities[self.playerindex].stats['curr']['HP'] - self.player_damage, self.monsterentities[self.playerindex].stats['base']['HP'] + self.monsterentities[self.playerindex].stats['bonus']['bonusHP'] - self.monsterentities[self.playerindex].stats['penalty']['penaltyHP'])

    def update(self, keys, currentmonster):
        """Updates info box"""
        self.check_input(keys)
        self.currentmonster = currentmonster
        self.image = self.make_image()

    def show_experience(self):
        """
        Show how much experience the player earned.
        """
        return "You earned {} experience points this battle!".format(self.experience_points)

    def show_gold(self):
        """
        Show how much gold the player earned.
        """
        return "You found {} gold.".format(self.gold_earned)

    def reset_level_up_message(self):
        self.state_dict[c.LEVEL_UP] = self.level_up()


'''
class SelectBox(object):
    """
    Box to select whether to attack, use item, use magic or run away.
    """
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.slots = self.make_slots()
        self.image = self.make_image()
        self.rect = self.image.get_rect(bottom=640,
                                        right=960)

    def make_image(self):
        """
        Make the box image for
        """
        image = setup.GFX['goldbox']
        rect = image.get_rect(bottom=640)
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for text in self.slots:
            text_surface = self.font.render(text, True, c.NEAR_BLACK)
            text_rect = text_surface.get_rect(x=self.slots[text]['x'],
                                              y=self.slots[text]['y'])
            surface.blit(text_surface, text_rect)

        return surface

    def make_slots(self):
        """
        Make the slots that hold the text selections, and locations.
        """
        slot_dict = {}
        selections = ['Attack', 'Items', 'Magic', 'Run']

        for i, text in enumerate(selections):
            slot_dict[text] = {'x': 150,
                               'y': (i*34)+10}

        return slot_dict
'''


class SelectArrow(object):
    """Small arrow for menu"""
    def __init__(self, enemy_pos_list, info_box):
        self.info_box = info_box
        self.image = setup.GFX['doublearrow']
        self.rect = self.image.get_rect()
        self.state = 'select action'
        self.state_dict = self.make_state_dict()
        self.pos_list = self.make_select_action_pos_list()
        self.index = 0
        self.rect.topleft = self.pos_list[self.index]
        self.allow_input = False
        self.enemy_pos_list = enemy_pos_list
        self.observers = [observer.SoundEffects()]

    def notify(self, event):
        """
        Notify all observers of events.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def make_state_dict(self):
        """Make state dictionary"""
        state_dict = {c.SELECT_ACTION: self.select_action,
                      c.SELECT_ENEMY_ATTACK: self.select_enemy_attack,
                      c.SELECT_ENEMY_SPELL: self.select_enemy_spell,
                      c.SELECT_ITEM: self.select_item,
                      c.SELECT_MAGIC: self.select_magic,
                      'invisible': self.become_invisible_surface}

        return state_dict

    def select_action(self, keys):
        """
        Select what action the player should take.
        """
        self.pos_list = self.make_select_action_pos_list()
        if self.index > (len(self.pos_list) - 1):
            print self.pos_list, self.index
        self.rect.topleft = self.pos_list[self.index]

        self.check_input(keys)

    def make_select_action_pos_list(self):
        """
        Make the list of positions the arrow can be in.
        """
        self.image = setup.GFX['doublearrow']
        pos_list = [(510,525)]

        return pos_list

    def select_enemy_attack(self, keys):
        """
        Select what enemy you want to take action on.
        """
        self.pos_list = self.enemy_pos_list
        self.image = setup.GFX['arrowright']

        if self.pos_list:
            pos = self.pos_list[self.index]
            self.rect.x = pos[0] - 60
            self.rect.y = pos[1] + 20

        self.check_input(keys)
    
    def select_enemy_spell(self, keys):
        """
        Select what enemy you want to take action on.
        """
        self.pos_list = self.enemy_pos_list
        self.image = setup.GFX['arrowright']

        if self.pos_list:
            pos = self.pos_list[self.index]
            self.rect.x = pos[0] - 60
            self.rect.y = pos[1] + 20

        self.check_input(keys)

    def check_input(self, keys):
        if self.allow_input:
            if keys[pg.K_DOWN] and self.index < (len(self.pos_list) - 1):
                self.notify(c.CLICK)
                self.index += 1
                self.allow_input = False
            elif keys[pg.K_UP] and self.index > 0:
                self.notify(c.CLICK)
                self.index -= 1
                self.allow_input = False
            elif keys[pg.K_RIGHT]:
                if self.state in (c.SELECT_ENEMY_ATTACK, c.SELECT_ENEMY_SPELL):
                    if self.index+3 < len(self.pos_list):
                        self.notify(c.CLICK)
                        self.index += 3
                self.allow_input = False
            elif keys[pg.K_LEFT]:
                if self.state in (c.SELECT_ENEMY_ATTACK, c.SELECT_ENEMY_SPELL):
                    if self.index-3 > -1:
                        self.notify(c.CLICK)
                        self.index -=3
                self.allow_input = False
                        


        if keys[pg.K_DOWN] == False and keys[pg.K_UP] == False \
                and keys[pg.K_RIGHT] == False and keys[pg.K_LEFT] == False:
            self.allow_input = True

    def select_item(self, keys):
        """
        Select item to use.
        """
        self.pos_list = self.make_select_item_pos_list()
        self.image = setup.GFX['arrowright']

        pos = self.pos_list[self.index]
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.check_input(keys)

    def make_select_item_pos_list(self):
        """
        Make the coordinates for the arrow for the item select screen.
        """
        pos_list = []
        text_list = self.info_box.make_item_text()

        for i in range(len(text_list)):
            left = 3
            top = (i * 35) + 475
            pos_list.append((left, top))

        return pos_list

    def select_magic(self, keys):
        """
        Select magic to use.
        """
        self.pos_list = self.make_select_magic_pos_list()
        self.image = setup.GFX['arrowright']

        pos = self.pos_list[self.index]
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.check_input(keys)

    def make_select_magic_pos_list(self):
        """
        Make the coordinates for the arrow for the magic select screen.
        """
        pos_list = []
        text_list = self.info_box.make_magic_text()

        for i in range(len(text_list)):
            left = 3
            top = (i * 35) + 475
            pos_list.append((left, top))

        return pos_list


    def become_invisible_surface(self, *args):
        """
        Make image attribute an invisible surface.
        """
        self.image = pg.Surface(self.rect.size)
        self.image.set_colorkey(c.BLACK)

    def become_select_item_state(self):
        self.index = 0
        self.state = c.SELECT_ITEM

    def become_select_magic_state(self):
        self.index = 0
        self.state = c.SELECT_MAGIC

    def update(self, keys):
        """
        Update arrow position.
        """
        state_function = self.state_dict[self.state]
        state_function(keys)

    def draw(self, surface):
        """
        Draw to surface.
        """
        surface.blit(self.image, self.rect)

    def remove_pos(self, i):
        self.enemy_pos_list.pop(i)

'''
class PlayerHealth(object):
    """
    Basic health meter for player.
    """
    def __init__(self, select_box_rect, game_data):
        self.stats = game_data['conductors'][0].monsters[0].stats
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.posx = select_box_rect.centerx
        self.posy = select_box_rect.y - 5

    @property
    def image(self):
        """
        Make the image surface for the player
        """
        current_health = str(self.stats['curr']['HP'])
        max_health = str(self.stats['base']['HP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP'])
        if len(current_health) == 2:
            buffer = '  '
        elif len(current_health) == 1:
            buffer = '    '
        else:
            buffer = ''
        health_string = "Health: {}{}/{}".format(buffer, current_health, max_health)
        health_surface =  self.title_font.render(health_string, True, c.NEAR_BLACK)
        health_rect = health_surface.get_rect(x=20, y=9)

        """
        current_magic = str(self.magic_stats['current'])
        if len(current_magic) == 2:
            buffer = '  '
        elif len(current_magic) == 1:
            buffer = '    '
        else:
            buffer = ''
        max_magic = str(self.magic_stats['maximum'])
        magic_string = "Magic:  {}{}/{}".format(buffer, current_magic, max_magic)
        magic_surface = self.title_font.render(magic_string, True, c.NEAR_BLACK)
        magic_rect = magic_surface.get_rect(x=20, top=health_rect.bottom)
        """
        
        box_surface = setup.GFX['battlestatbox']
        box_rect = box_surface.get_rect()

        parent_surface = pg.Surface(box_rect.size)
        parent_surface.blit(box_surface, box_rect)
        parent_surface.blit(health_surface, health_rect)
        #parent_surface.blit(magic_surface, magic_rect)

        return parent_surface

    @property
    def rect(self):
        """
        Make the rect object for image surface.
        """
        return self.image.get_rect(centerx=self.posx, bottom=self.posy)

    def draw(self, surface):
        """
        Draw health to surface.
        """
        surface.blit(self.image, self.rect)
'''