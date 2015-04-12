# -*- coding: utf-8 -*-

"""
This class controls all the GUI for the player
menu screen.
"""
import sys
import pygame as pg
from . import setup, observer
from . import constants as c
from . import tools

#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    range = xrange


class SmallArrow(pg.sprite.Sprite):
    """
    Small arrow for menu.
    """
    def __init__(self, left_box):
        super(SmallArrow, self).__init__()
        self.image = setup.GFX['arrowright']
        self.rect = self.image.get_rect()
        self.state = 'selectmenu'
        self.state_dict = self.make_state_dict()
        self.slots = left_box.slots
        self.pos_list = []

    def make_state_dict(self):
        """
        Make state dictionary.
        """
        state_dict = {'selectmenu': self.navigate_select_menu,
                      'conductorsubmenu': self.navigate_conductor_submenu,
                      'monsterselect': self.navigate_monster_select,
                      'trainselect': self.navigate_monster_select,
                      'training': self.navigate_monster_training,
                      'itemtypeselect': self.navigate_item_type_select,
                      'monsterinfo': self.navigate_monster_info,
                      'itemsubmenu': self.navigate_item_submenu,
                      'magicsubmenu': self.navigate_magic_submenu}

        return state_dict

    def navigate_select_menu(self, pos_index):
        """
        Nav the select menu.
        """
        self.pos_list = self.make_select_menu_pos_list()
        self.rect = self.pos_list[pos_index]

    def navigate_conductor_submenu(self, pos_index):
        self.pos_list = self.make_conductor_menu_pos_list()
        self.rect = self.pos_list[pos_index]

    def navigate_monster_select(self, pos_index):
        self.pos_list = self.make_monster_select_pos_list()
        self.rect = self.pos_list[pos_index]

    def navigate_monster_training(self, pos_index):
        self.pos_list = self.make_monster_training_pos_list()
        self.rect = self.pos_list[pos_index]

    def navigate_item_type_select(self, pos_index):
        self.pos_list = self.make_item_type_select_pos_list()
        self.rect = self.pos_list[pos_index]
    
    def navigate_monster_info(self, pos_index):
        self.pos_list = self.make_monster_info_pos_list()
        if pos_index == 3:
            self.image = setup.GFX['doublearrow']
        else:
            self.image = setup.GFX['arrowleft']
        self.rect = self.pos_list[pos_index]

    def navigate_item_submenu(self, pos_index):
        """Nav the item submenu"""
        self.pos_list = self.make_item_menu_pos_list()
        self.rect = self.pos_list[pos_index]

    def navigate_magic_submenu(self, pos_index):
        """
        Nav the magic submenu.
        """
        self.pos_list = self.make_magic_menu_pos_list()
        self.rect = self.pos_list[pos_index]

    def make_magic_menu_pos_list(self):
        """
        Make the list of possible arrow positions for magic submenu.
        """
        pos_list = [(310, 119),
                    (310, 169)]

        return pos_list

    def make_select_menu_pos_list(self):
        """
        Make the list of possible arrow positions.
        """
        pos_list = []
        self.image = setup.GFX['arrowright']

        for i in range(6):
            pos = (615, 55 + (i * 40))
            pos_list.append(pos)

        return pos_list

    def make_monster_select_pos_list(self):
        pos_list = [(5,90), (5,150), (5,210),
		            (185,90), (185,150), (185,210),
                    (365,90), (365,150), (365,210)]
        self.image = setup.GFX['arrowright']

        return pos_list

    def make_monster_training_pos_list(self):
        pos_list = [(5,460), (5,500), (5,540),
                    (285,435), (285, 475), (285, 515), (285, 555),
                    (560,460), (560, 500), (560, 540)]
        self.image = setup.GFX['arrowright']

        return pos_list

    def make_monster_info_pos_list(self):
        pos_list = []

        for i in range(3):
            pos = (450, 440 + i*45)
            pos_list.append(pos)
        pos_list.append((520,440))
        pos_list.append((755,505))
        pos_list.append((755,555))

        return pos_list

    def make_conductor_menu_pos_list(self):
        pos_list = []
        self.image = setup.GFX['arrowleft']

        for i in range(3):
            pos = (570, 70 + (i*100))
            pos_list.append(pos)

        return pos_list

    def make_item_type_select_pos_list(self):
        pos_list = []
        self.image = setup.GFX['arrowright']
        
        for i in range(4):
            pos = (5, 75 + (i*60))
            pos_list.append(pos)

        return pos_list

    def make_item_menu_pos_list(self):
        """
        Make the list of arrow positions in the item submenu.
        """
        pos_list = []
        self.image = setup.GFX['arrowright']

        for i in range(5):
            pos = (5, 75 + (i*45))
            pos_list.append(pos)

        return pos_list

    def update(self, pos_index):
        """
        Update arrow position.
        """
        state_function = self.state_dict[self.state]
        state_function(pos_index)

    def draw(self, surface):
        """
        Draw to surface"""
        surface.blit(self.image, self.rect)


class BottomBox(pg.sprite.Sprite):
    def __init__(self, game_data):
        super(BottomBox, self).__init__()
        self.game_data = game_data
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 25)
        self.small_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 20)
        self.header_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 40)
        self.big_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 35)
        self.state = 'invisible'
        self.state_dict = self.make_state_dict()
        self.image, self.rect = self.make_blank_bottom_box()
        self.compstate = None
        self.conductorstate = None

    def make_state_dict(self):
        """Make the dictionary of state methods"""
        state_dict = {'conductorinfo': self.show_conductor_info,
                      'monsterinfo': self.show_monster_info,
                      'description': self.show_description,
                      'training': self.show_training,
                      'invisible': self.show_nothing}
		
        return state_dict

    def show_conductor_info(self):
        conductor = self.game_data['conductors'][self.compstate]
        default_text = ['Current Monsters:', 'Training Aptitudes:', 'HP: ', 'ATK: ', 'DEF: ', 'MUS: ', 'FOC: ', 'CLA: ', 'RHY: ', 'STR: ', 'WND: ', 'PRC: ']
        
        surface, rect = self.make_blank_bottom_box()
        
        for i in range(len(conductor.monsters)+1):
            if i == 0:
                text = default_text[i]
                text_image = self.header_font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=25, y=25+(45*i))
                surface.blit(text_image, text_rect)
            else:
                text = conductor.monsters[i-1].name
                text_image = self.big_font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=25, y=25+(45*i))
                surface.blit(text_image, text_rect)
                prevsize = self.big_font.size(text)
                text = "(" + conductor.monsters[i-1].species + ")"
                text_image = self.small_font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=prevsize[0]+35, y=35+(45*i))
                surface.blit(text_image, text_rect)
        
        text = default_text[1]
        
        text_image = self.header_font.render(text, True, c.WHITE)
        text_rect = text_image.get_rect(x=395, y=25)
        surface.blit(text_image, text_rect)
        
        for i in range(3):
            text = default_text[i+2]
            text += str(conductor.aptitude[text[:len(text)-2].lower()])
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=450+(i*85)+((i-1)*15), y = 75)
            surface.blit(text_image, text_rect)

        for i in range(4):
            text = default_text[i+5]
            text += str(conductor.aptitude[text[:len(text)-2].lower()])
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=400+(i*95), y = 105)
            surface.blit(text_image, text_rect)

        for i in range(3):
            text = default_text[i+9]
            if i == 0:
                text += str(conductor.aptitude['string'])
            elif i == 1:
                text += str(conductor.aptitude['wind'])
            elif i == 2:
                text += str(conductor.aptitude['percussion'])
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=450+(i*85)+((i-1)*15), y = 135)
            surface.blit(text_image, text_rect)
			
        self.image = surface
        self.rect = rect

    def show_monster_info(self):
        monster = self.game_data['conductors'][self.compstate[0]].monsters[self.compstate[1]]
        conductors = []
        for i in range(len(self.game_data['conductors'])):
            conductors.append(self.game_data['conductors'][i].name)

        default_text = ["Equipment:", "Instrument: ", "Accessory 1:", "Accessory 2:", "Master:", "Release?", "Yes", "No"]

        surface, rect = self.make_blank_bottom_box()

        for i in range(4):
            text = default_text[i]
            if i == 1:
                text += str(monster.equipment['instrument'])
            elif i == 2:
                text += str(monster.equipment['accessory1'])
            elif i == 3:
                text += str(monster.equipment['accessory2'])
            text_image = self.big_font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=30, y = 25 + (i*45))
            surface.blit(text_image, text_rect)

        text = default_text[4] + " " + str(monster.master.name)
        text_image = self.big_font.render(text, True, c.WHITE)
        text_rect = text_image.get_rect(x=500, y = 25)
        surface.blit(text_image, text_rect)
        
        text = conductors[self.conductorstate]
        text_image = self.big_font.render(text, True, c.WHITE)
        text_rect = text_image.get_rect(x=580, y=70)
        surface.blit(text_image, text_rect)

        text = default_text[5]
        text_image = self.big_font.render(text, True, c.WHITE)
        text_rect = text_image.get_rect(x=500, y=135)
        surface.blit(text_image, text_rect)

        for i in range(2):
            text = default_text[i+6]
            text_image = self.big_font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=650, y=135+(i*50))
            surface.blit(text_image, text_rect)

        self.image = surface
        self.rect = rect

    def show_training(self):
        conductor = self.game_data['conductors'][self.compstate[0]]
        monster = conductor.monsters[self.compstate[1]]
        default_text = ['TP remaining: ', 'To next TP: ', 'HP: ', 'ATK: ', 'DEF: ', 'MUS: ', 'FOC: ', 'CLA: ', 'RHY: ', 'STR: ', 'WND: ', 'PRC: ']

        surface, rect = self.make_blank_bottom_box()

        for i in range(2):
            text = default_text[i]
            if i == 0:
                text += str(monster.stats['tp']['tp'])
            else:
                text += str(monster.stats['tp']['tpprog']) + "/" + str(monster.stats['tp']['nexttp'])
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=25+(i*195), y=25)
            surface.blit(text_image, text_rect)

        for i in range(7):
            text = default_text[i+2]
            text_image = self.font.render(text, True, c.WHITE)
            if i < 3:
                text_rect = text_image.get_rect(x=50, y=95+(40*i))
            else:
                text_rect = text_image.get_rect(x=330, y=70+(40*(i-3)))
            surface.blit(text_image, text_rect)
            if i == 0:
                text = str(monster.stats['base'][text[:len(text)-2]])
            else:
                text = str(monster.stats['base'][text[:len(text)-2].lower()])
            text_image = self.font.render(text, True, c.WHITE)
            if i < 3:
                text_rect = text_image.get_rect(x=115, y=95+(40*i))
            else:
                text_rect = text_image.get_rect(x=395, y=70+(40*(i-3)))
            surface.blit(text_image, text_rect)

            text = default_text[i+2]
            if i == 0:
                text = "(" + str(conductor.aptitude[text[:len(text)-2].lower()] * monster.stats['gains'][text[:len(text)-2]]) + ")"
            else:
                text = "(" + str(conductor.aptitude[text[:len(text)-2].lower()] * monster.stats['gains'][text[:len(text)-2].lower()]) + ")"
            text_image = self.font.render(text, True, c.WHITE)
            if i < 3:
                text_rect = text_image.get_rect(x=175, y=95+(40*i))
            else:
                text_rect = text_image.get_rect(x=455, y=70+(40*(i-3)))
            surface.blit(text_image, text_rect)
			
        for i in range(3):
            text = default_text[i+9]
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=605, y=95+(40*i))
            surface.blit(text_image, text_rect)
            
            if i == 0:
                text = str(monster.stats['base']['string'])
            elif i == 1:
                text = str(monster.stats['base']['wind'])
            else:
                text = str(monster.stats['base']['percussion'])
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=670, y=95+(40*i))
            surface.blit(text_image, text_rect)

            text = default_text[i+9]
            if i == 0:
                text = "(" + str(conductor.aptitude['string']) + ")"
            elif i == 1:
                text = "(" + str(conductor.aptitude['wind']) + ")"
            elif i == 2:
                text = "(" + str(conductor.aptitude['percussion']) + ")"
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=740, y=95+(40*i))
            surface.blit(text_image, text_rect)

        self.image = surface
        self.rect = rect
            
    def show_description(self):
        pass
	
    def show_nothing(self):
        """
        Show nothing when the menu is opened from a level.
        """
        self.image, self.rect = self.make_blank_bottom_box()

    def make_blank_bottom_box(self):
        """Make an info box with title, otherwise blank"""
        image = setup.GFX['pmenu_box_bottom']
        rect = image.get_rect(left=25, top=375)
        centerx = rect.width / 2

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0,0))

        return surface, rect


    def update(self):
        state_function = self.state_dict[self.state]
        state_function()

    def draw(self, surface):
        """
        Draw to surface.
        """
        surface.blit(self.image, self.rect)


class LeftBox(pg.sprite.Sprite):
    def __init__(self, game_data):
        super(LeftBox, self).__init__()
        self.game_data = game_data
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.big_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 35)
        self.cond_font = pg.font.Font(setup.FONTS[c.SPEC_FONT1], 40)
        self.cond_font.set_italic(True)
        self.title_font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 28)
        self.title_font.set_underline(True)
        self.get_tile = tools.get_tile
        self.slots = {}
        self.state = 'invisible'
        self.state_dict = self.make_state_dict()
        self.print_slots = True
        self.itemindex = 0
        self.selectedmonster = None

    def make_state_dict(self):
        """Make the dictionary of state methods"""
        state_dict = {'conductors': self.show_conductors,
                      'monsters': self.show_monsters,
                      'trainselect': self.show_monsters,
                      'itemtypes': self.show_itemtypes,
                      'consumables': self.show_consumables,
                      'equipment': self.show_equipment,
                      'keyitems': self.show_keyitems,
                      'loot': self.show_loot,
                      'instruments': self.show_instruments,
                      'accessories': self.show_accessories,
                      'invisible': self.show_nothing}
		
        return state_dict

    def show_conductors(self):
        conductor_list = []
        for conduc in self.game_data['conductors']:
            conductor_list.append(conduc.name)
        
        surface, rect = self.make_blank_left_box()
        
        for i in range(len(conductor_list)):
            text = conductor_list[i]
            text_image = self.cond_font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=250, y=55+(100*i))
            surface.blit(text_image, text_rect)
            
        self.image = surface
        self.rect = rect

    def show_monsters(self):
        monster_list = [[],[],[]]
        for i, conduc in enumerate(self.game_data['conductors']):
            for m in conduc.monsters:
                monster_list[i].append(m.name)
                
        self.slots = {}
        
        for i, l in enumerate(monster_list):
            for j, m in enumerate(l):
                posx = 65 + (i*180)
                posy = 85 + (j*60)
                self.slots[(posx,posy)] = m
        
        surface, rect = self.make_blank_left_box()
        
        for coord in self.slots:
            text = self.slots[coord]
            text_image = self.big_font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(topleft=coord)
            surface.blit(text_image, text_rect)
            
        self.image = surface
        self.rect = rect

    def show_itemtypes(self):
        itemtype_list = ['Loot', 'Consumables', 'Equipment', 'Key Items']

        surface, rect = self.make_blank_left_box()

        for i in range(len(itemtype_list)):
            text = itemtype_list[i]
            text_image = self.big_font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=65, y=65+(i*60))
            surface.blit(text_image, text_rect)
        
        self.image = surface
        self.rect = rect
        
    def show_consumables(self):
        self.consum_list = []
        
        for item in self.game_data['player inventory']:
            if item.itemType is "Consumable":
                self.consum_list.append(item.name)

        self.slots = {}

        surface, rect = self.make_blank_left_box()
        if len(self.consum_list)-(self.itemindex*5)>5:
            for x in range(5):
                text = self.consum_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        else:
            for x in range(len(self.consum_list) - self.itemindex*5):
                text = self.consum_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        
        self.image = surface
        self.rect = rect

    def show_loot(self):
        self.loot_list = []
        
        for item in self.game_data['player inventory']:
            if item.itemType is "Loot":
                self.loot_list.append(item.name)

        self.slots = {}

        surface, rect = self.make_blank_left_box()
        if len(self.loot_list)-(self.itemindex*5)>5:
            for x in range(5):
                text = self.loot_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        else:
            for x in range(len(self.loot_list) - self.itemindex*5):
                text = self.loot_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        
        self.image = surface
        self.rect = rect

    def show_equipment(self):
        self.eq_list = []
		
        for item in self.game_data['player inventory']:
            if item.itemType is "Instrument" or item.itemType is "Accessory":
                self.eq_list.append(item.name)

        self.slots = {}

        surface, rect = self.make_blank_left_box()
        if len(self.eq_list)-(self.itemindex*5)>5:
            for x in range(5):
                text = self.eq_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        else:
            for x in range(len(self.eq_list) - self.itemindex*5):
                text = self.eq_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        
        self.image = surface
        self.rect = rect

    def show_keyitems(self):
        self.ki_list = []
		
        for item in self.game_data['player inventory']:
            if item.itemType is "Key Item":
                self.ki_list.append(item.name)

        self.slots = {}

        surface, rect = self.make_blank_left_box()
        if len(self.ki_list)-(self.itemindex*5)>5:
            for x in range(5):
                text = self.ki_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        else:
            for x in range(len(self.ki_list) - self.itemindex*5):
                text = self.ki_list[x+(self.itemindex*5)]
                posx = 65
                posy = 70 + (x*45)
                self.slots[(posx,posy)] = text
                text_image = self.font.render(text, True, c.WHITE)
                text_rect = text_image.get_rect(x=posx, y=posy)
                surface.blit(text_image, text_rect)
        
        self.image = surface
        self.rect = rect

    def show_instruments(self):
        self.inst_list = []
		
        inventory = self.selectedmonster.master.inventory
        for x in inventory:
            if x.itemType is "Instrument":
                self.inst_list.append(x.name)

        self.slots = {}

        surface, rect = self.make_blank_left_box()
        for x in range(5):
            text = self.inst_list[x+(self.itemindex*5)]
            posx = 65
            posy = 70 + (x*45)
            self.slots[(posx,posy)] = text
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=posx, y=posy)
            surface.blit(text_image, text_rect)
        
        self.image = surface
        self.rect = rect

    def show_accessories(self):
        self.acc_list = []
		
        inventory = self.selectedmonster.master.inventory
        for x in inventory:
            if x.itemType is "Accessory":
                acc_list.append(x.name)

        self.slots = {}

        surface, rect = self.make_blank_left_box()
        for x in range(5):
            text = self.acc_list[x+(self.itemindex*5)]
            posx = 65
            posy = 70 + (x*45)
            self.slots[(posx,posy)] = text
            text_image = self.font.render(text, True, c.WHITE)
            text_rect = text_image.get_rect(x=posx, y=posy)
            surface.blit(text_image, text_rect)
        
        self.image = surface
        self.rect = rect


    def show_nothing(self):
        """
        Show nothing when the menu is opened from a level.
        """
        self.image, self.rect = self.make_blank_left_box()

    def make_blank_left_box(self):
        """Make an info box with title, otherwise blank"""
        image = setup.GFX['pmenu_box_left']
        rect = image.get_rect(left=25, top=15)
        centerx = rect.width / 2

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0,0))

        return surface, rect


    def update(self):
        state_function = self.state_dict[self.state]
        state_function()


    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)


class RightBox(pg.sprite.Sprite):
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 40)
        self.image, self.rect = self.make_image()

    def make_image(self):
        choices = ['Conductors', 'Monsters', 'Items', 'Training', 'Quests', 'Save']
        image = setup.GFX['pmenu_box_right']
        rect = image.get_rect(left=675, top=15)

        for x in choices:
            x.center(20)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        for i, choice in enumerate(choices):
            choice_image = self.font.render(choice, True, c.WHITE)
            choice_rect = choice_image.get_rect(x=15, y=(45 + (i * 40)))
            choice_rect.centerx = rect.centerx - 675
            surface.blit(choice_image, choice_rect)

        return surface, rect

    def draw(self, surface):
        """Draw to surface"""
        surface.blit(self.image, self.rect)


class MenuGui(object):
    def __init__(self, level, inventory, conductors):
        self.level = level
        self.game_data = self.level.game_data
        self.monsters = self.make_monster_list()
        self.sfx_observer = observer.SoundEffects()
        self.observers = [self.sfx_observer]
        self.inventory = inventory
        self.conductors = conductors
        self.left_box = LeftBox(self.game_data)
        self.bottom_box = BottomBox(self.game_data)
        self.right_box = RightBox()
        self.arrow = SmallArrow(self.left_box)
        self.arrow_index = 0
        self.allow_input = False

    def make_monster_list(self):
        monster_list = [[],[],[]]
        self.monposlist = []
        for i, conduc in enumerate(self.game_data['conductors']):
            for j, m in enumerate(conduc.monsters):
                monster_list[i].append(m.name)
                self.monposlist.append(j + (i*3))

        return monster_list
        

    def check_for_input(self, keys):
        """Check for input"""
        if self.allow_input:
            if keys[pg.K_DOWN]:
                if self.arrow_index < len(self.arrow.pos_list) - 1:

                    if self.arrow.state == 'conductorsubmenu':
                        if len(self.game_data['conductors']) > self.arrow_index+1:
                            self.arrow_index += 1
                            self.bottom_box.compstate += 1
                            self.notify(c.CLICK)


                    elif self.arrow.state in ('monsterselect', 'trainselect'):
                        if len(self.monsters) > self.arrow_index+1:
                            self.arrow_index = self.monposlist[self.monposlist.index(self.arrow_index) + 1]
                            self.notify(c.CLICK)

                    elif self.arrow.state == 'itemsubmenu':
                        if self.left_box.state == 'loot':
                            if len(self.left_box.loot_list) > (self.arrow_index + self.left_box.itemindex*5) + 1:
                                self.arrow_index += 1
                                self.notify(c.CLICK)
                        elif self.left_box.state == 'consumables':
                            if len(self.left_box.consum_list) > (self.arrow_index + self.left_box.itemindex*5) + 1:
                                self.arrow_index += 1
                                self.notify(c.CLICK)
                        elif self.left_box.state == 'equipment':
                            if len(self.left_box.eq_list) > (self.arrow_index + self.left_box.itemindex*5) + 1:
                                self.arrow_index += 1
                                self.notify(c.CLICK)
                        elif self.left_box.state == 'keyitems':
                            if len(self.left_box.ki_list) > (self.arrow_index + self.left_box.itemindex*5) + 1:
                                self.arrow_index += 1
                                self.notify(c.CLICK)

                    else:
                        self.arrow_index += 1
                        self.notify(c.CLICK)

                else:
                    if self.arrow.state == 'itemsubmenu':
                        if self.arrow_index > 3:
                            self.arrow_index = 0
                            self.left_box.itemindex += 1
                self.allow_input = False

            elif keys[pg.K_UP]:
                if self.arrow_index > 0:
                    if self.arrow.state == 'conductorsubmenu':
                        self.notify(c.CLICK)
                        self.arrow_index -= 1
                        self.bottom_box.compstate -= 1

                    elif self.arrow.state in ('monsterselect', 'trainselect'):
                        self.notify(c.CLICK)
                        self.arrow_index = self.monposlist[self.monposlist.index(self.arrow_index) - 1]

                    elif self.arrow.state == 'itemsubmenu':
                        if self.left_box.itemindex >= 0:
                            self.notify(c.CLICK)
                            self.arrow_index -= 1

                    else:
                        self.notify(c.CLICK)
                        self.arrow_index -= 1

                else:
                    if self.arrow.state == 'itemsubmenu':
                        if self.left_box.itemindex > 0:
                                self.left_box.itemindex -= 1
                                self.arrow_index = 4
                        else:
                                self.arrow_index = 0
                    
                self.allow_input = False

            elif keys[pg.K_LEFT]:
                if self.arrow.state == 'monsterinfo':
                    if self.arrow_index == 3:
                        if self.bottom_box.conductorstate > 0:
                            self.notify(c.CLICK)
                            self.bottom_box.conductorstate -= 1

                self.allow_input = False

            elif keys[pg.K_RIGHT]:
                if self.arrow.state == 'monsterinfo':
                   if self.arrow_index == 3:
                       if self.bottom_box.conductorstate+1 < len(self.game_data['conductors']):
                            self.bottom_box.conductorstate += 1
                            self.notify(c.CLICK)
                self.allow_input = False

            elif keys[pg.K_z]:
                if self.arrow.state == 'selectmenu':
                    if self.arrow_index == 0:
                        self.notify(c.CLICK2)
                        self.left_box.state = 'conductors'
                        self.bottom_box.state = 'conductorinfo'
                        self.bottom_box.compstate = 0
                        self.arrow.state = 'conductorsubmenu'
                        self.arrow_index = 0
                    elif self.arrow_index == 1:
                        self.notify(c.CLICK2)
                        self.arrow_index = 0
                        self.left_box.state = 'monsters'
                        self.arrow.state = 'monsterselect'
                    elif self.arrow_index == 2:
                        self.notify(c.CLICK2)
                        self.arrow_index = 0
                        self.left_box.state = 'itemtypes'
                        self.arrow.state = 'itemtypeselect'
                    elif self.arrow_index == 3:
                        self.notify(c.CLICK2)
                        self.arrow_index = 0
                        self.left_box.state = 'trainselect'
                        self.arrow.state = 'trainselect'
                
                elif self.arrow.state == 'monsterselect':
                    self.notify(c.CLICK2)
                    self.arrow.state = 'monsterinfo'
                    self.bottom_box.compstate = ((self.arrow_index/3), self.arrow_index%3)
                    self.bottom_box.conductorstate = 0
                    self.arrow_index = 0
                    self.bottom_box.state = 'monsterinfo'

                elif self.arrow.state == 'trainselect':
                    self.notify(c.CLICK2)
                    self.arrow.state = 'training'
                    self.bottom_box.compstate = ((self.arrow_index/3), self.arrow_index%3)
                    self.arrow_index = 0
                    self.bottom_box.state = 'training'

                elif self.arrow.state == 'itemtypeselect':
                    self.notify(c.CLICK2)
                    if self.arrow_index == 0:
                        self.left_box.state = 'loot'
                    elif self.arrow_index == 1:
                        self.left_box.state = 'consumables'
                    elif self.arrow_index == 2:
                        self.left_box.state = 'equipment'
                    elif self.arrow_index == 3:
                        self.left_box.state = 'keyitems'
                    self.arrow_index = 0
                    self.arrow.state = 'itemsubmenu'
                self.allow_input = False

            elif keys[pg.K_x]:
                if self.arrow.state in ('conductorsubmenu', 'monsterselect','itemtypeselect', 'trainselect'):
                    self.notify(c.CLOSE)
                    self.left_box.state = 'invisible'
                    self.bottom_box.state = 'invisible'
                    self.arrow.state = 'selectmenu'
                    self.arrow_index = 0

                elif self.arrow.state == 'monsterinfo':
                    self.notify(c.CLOSE)
                    self.bottom_box.state = 'invisible'
                    self.bottom_box.compstate = 0
                    self.arrow.state = 'monsterselect'
                    self.arrow_index = 0

                elif self.arrow.state == 'training':
                    self.notify(c.CLOSE)
                    self.bottom_box.state = 'invisible'
                    self.bottom_box.compstate = 0
                    self.arrow.state = 'trainselect'
                    self.arrow_index = 0

                elif self.arrow.state == 'itemsubmenu':
                    self.notify(c.CLOSE)
                    self.left_box.state = 'itemtypes'
                    self.arrow.state = 'itemtypeselect'
                    self.arrow_index = 0

                self.allow_input = False

            elif keys[pg.K_RETURN]:
                self.level.state = 'normal'
                self.left_box.state = 'invisible'
                self.arrow_index = 0
                self.arrow.state = 'selectmenu'
                self.allow_input = False

        if (not keys[pg.K_DOWN]
                and not keys[pg.K_UP]
                and not keys[pg.K_RETURN]
                and not keys[pg.K_SPACE]
                and not keys[pg.K_RIGHT]
                and not keys[pg.K_LEFT]
                and not keys[pg.K_z]
                and not keys[pg.K_x]):
            self.allow_input = True

    def notify(self, event):
        """
        Notify all observers of event.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def select_item(self):
        """
        Select item from item menu.
        """
        health = self.game_data['player stats']['health']
        posx = self.arrow.rect.x - 220
        posy = self.arrow.rect.y - 38

        if (posx, posy) in self.left_box.slots:
            if self.left_box.slots[(posx, posy)][:7] == 'Healing':
                potion = 'Healing Potion'
                value = 30
                self.drink_potion(potion, health, value)
            elif self.left_box.slots[(posx, posy)][:5] == 'Ether':
                potion = 'Ether Potion'
                stat = self.game_data['player stats']['magic']
                value = 30
                self.drink_potion(potion, stat, value)
            elif self.left_box.slots[(posx, posy)][:10] == 'Long Sword':
                self.inventory['equipped weapon'] = 'Long Sword'
            elif self.left_box.slots[(posx, posy)][:6] == 'Rapier':
                self.inventory['equipped weapon'] = 'Rapier'
            elif self.left_box.slots[(posx, posy)][:13] == 'Wooden Shield':
                if 'Wooden Shield' in self.inventory['equipped armor']:
                    self.inventory['equipped armor'].remove('Wooden Shield')
                else:
                    self.inventory['equipped armor'].append('Wooden Shield')
            elif self.left_box.slots[(posx, posy)][:10] == 'Chain Mail':
                if 'Chain Mail' in self.inventory['equipped armor']:
                    self.inventory['equipped armor'].remove('Chain Mail')
                else:
                    self.inventory['equipped armor'].append('Chain Mail')

    def select_magic(self):
        """
        Select spell from magic menu.
        """
        health = self.game_data['player stats']['health']
        magic = self.game_data['player stats']['magic']
        posx = self.arrow.rect.x - 190
        posy = self.arrow.rect.y - 39

        if (posx, posy) in self.left_box.slots:
            if self.left_box.slots[(posx, posy)][:4] == 'Cure':
               self.use_cure_spell()

    def use_cure_spell(self):
        """
        Use cure spell to heal player.
        """
        health = self.game_data['player stats']['health']
        magic = self.game_data['player stats']['magic']
        inventory = self.game_data['player inventory']

        if health['current'] != health['maximum']:
            if magic['current'] >= inventory['Cure']['magic points']:
                self.notify(c.POWERUP)
                magic['current'] -= inventory['Cure']['magic points']
                health['current'] += inventory['Cure']['power']
                if health['current'] > health['maximum']:
                    health['current'] = health['maximum']

    def drink_potion(self, potion, stat, value):
        """
        Drink potion and change player stats.
        """
        if stat['current'] != stat['maximum']:
            self.notify(c.POWERUP)
            self.inventory[potion]['quantity'] -= 1
            stat['current'] += value
            if stat['current'] > stat['maximum']:
                stat['current'] = stat['maximum']
            if not self.inventory[potion]['quantity']:
                del self.inventory[potion]

    def update(self, keys):
        self.left_box.update()
        self.right_box.update()
        self.bottom_box.update()
        self.arrow.update(self.arrow_index)
        self.check_for_input(keys)


    def draw(self, surface):
        self.right_box.draw(surface)
        self.left_box.draw(surface)
        self.bottom_box.draw(surface)
        self.arrow.draw(surface)