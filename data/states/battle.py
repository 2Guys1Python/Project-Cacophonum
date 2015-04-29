"""This is the state that handles battles against
monsters"""
import random, sys, copy
from itertools import izip
import pygame as pg
from .. import tools, battlegui, observer, setup, entityclasses, compositeclasses, spellhandler, itemhandler
from .. components import person, attack, attackitems
from .. import constants as c


#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    range = xrange


class Battle(tools._State):
    def __init__(self, monlist):
        super(Battle, self).__init__()
        self.name = 'battle'
        self.music = setup.MUSIC['precarious']
        self.volume = 0.4
        self.monlist = monlist

    def startup(self, current_time, game_data):
        """
        Initialize state attributes.
        """
        self.current_time = current_time
        self.timer = current_time
        self.allow_input = False
        self.game_data = game_data
        self.state = 'transition in'
        self.next = game_data['last state']
        self.run_away = False

        self.players, self.playerentities = self.make_player()
        self.monsters, self.monsterentities = self.make_monster()
        self.currentmonster = 0
        self.enemy_index = 0
        self.inventory = self.monsterentities[self.currentmonster].master.inventory
        self.currhits = 0
        self.maxhits = 1
        for p in self.players:
            p.attacked_enemy = None
        self.attack_animations = pg.sprite.Group()
        self.enemy_group, self.enemy_pos_list, self.enemy_list, self.enemyentities = self.make_enemies()
        self.experience_points = self.get_experience_points()
        self.new_gold = self.get_new_gold()
        self.background = self.make_background()
        self.info_box = battlegui.InfoBox(game_data, 
                                          self.experience_points, 
                                          self.new_gold,
                                          self.playerentities,
                                          self.monsterentities,
                                          self.enemyentities)
        self.arrow = battlegui.SelectArrow(self.enemy_pos_list,
                                           self.info_box)
        '''
        self.select_box = battlegui.SelectBox()
        self.player_health_box = battlegui.PlayerHealth(self.select_box.rect,
                                                        self.game_data)
        '''

        self.select_action_state_dict = self.make_selection_state_dict()
        self.observers = [observer.Battle(self),
                          observer.MusicChange()]
        for p in self.players:
            p.observers.extend(self.observers)
        self.observers.append(observer.SoundEffects())
        self.damage_points = pg.sprite.Group()
        self.player_actions = []
        self.enemy_actions = []
        self.player_action_dict = self.make_player_action_dict()
        self.enemy_action_dict = self.make_enemy_action_dict()
        self.enemies_to_attack = []
        self.monsters_to_attack = []
        self.action_selected = False
        self.just_leveled_up = False
        self.transition_rect = setup.SCREEN.get_rect()
        self.transition_alpha = 255
        

    def make_player_action_dict(self):
        """
        Make the dict to execute player actions.
        """
        action_dict = {c.PLAYER_ATTACK: self.enter_player_attack_state,
                       c.OFF_SPELL: self.cast_cure,
                       c.DEF_SPELL: self.cast_fire_blast,
                       c.DRINK_HEALING_POTION: self.enter_drink_healing_potion_state,
                       c.DRINK_ETHER_POTION: self.enter_drink_ether_potion_state}

        return action_dict
        
    def make_enemy_action_dict(self):
        action_dict = {c.ENEMY_ATTACK: self.enter_enemy_attack_state}
        
        return action_dict

    def get_experience_points(self):
        """
        Calculate experience points based on number of enemies
        and their levels.
        """
        experience_total = 0

        for enemy in self.enemyentities:
            experience_total += enemy.stats['curr']['TP']

        return experience_total

    def get_new_gold(self):
        """
        Calculate the gold collected at the end of the battle.
        """
        gold = 0

        for enemy in self.enemy_list:
            max_gold = enemy.level * 20
            gold += (random.randint(1, max_gold))

        return gold

    def make_background(self):
        """
        Make the blue/black background.
        """
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()
        background_group = pg.sprite.Group(background)

        return background_group

    def make_enemies(self):
        """
        Make the enemies for the battle. Return sprite group.
        """
        pos_list = []
        ent_list = []
        enemy_list = []

        for column in range(3):
            for row in range(3):
                x = (column * 110) + 40
                y = (row * 130) + 70
                pos_list.append([x, y])

        enemy_group = pg.sprite.OrderedUpdates()

        if self.game_data['battle type']:
            enemy_list.append(person.Enemy('Orthrus', 0, 0,
                                  'down', 'battle resting'))
            ent_list.append(copy.deepcopy(entityclasses.WildMonster('Orthrus', 1)))
        else:
            if self.game_data['start of game']:
                for enemy in range(3):
                    ran = random.randint(0,len(self.monlist)-1)
                    enemy_list.append(person.Enemy(self.monlist[ran], 0, 0,
                                                 'down', 'battle resting'))
                    ent_list.append(copy.deepcopy(entityclasses.WildMonster(self.monlist[ran], 1)))
                self.game_data['start of game'] = False
            else:
                for enemy in range(random.randint(1, 4)):
                    ran = random.randint(0,len(self.monlist)-1)
                    enemy_list.append(person.Enemy(self.monlist[ran], 0, 0,
                                                 'down', 'battle resting'))
                    ent_list.append(copy.deepcopy(entityclasses.WildMonster(self.monlist[ran], 1)))
        enemy_group.add(enemy_list.__iter__())
        for i, enemy in enumerate(enemy_group):
            enemy.rect.topleft = pos_list[i]
            enemy.image = pg.transform.scale2x(enemy.image)
            enemy.index = i
        
        
        #print [e.name for e in enemy_list]
        #print [x.name for x in ent_list]
        #print [g.name for g in enemy_group.sprites()]
        

        return enemy_group, pos_list[0:len(enemy_group)], enemy_list, ent_list

    def make_player(self):
        """
        Make the lists of sprites and data for the conductors
        """
        players = []
        playerentities = []
        for i, p in enumerate(self.game_data['conductors']):
            if i == 0:
                players.append(person.Player('left', self.game_data, 758, 69, 'battle resting', 1, p.name))
            elif i == 1:
                players.append(person.Player('left', self.game_data, 575, 220, 'battle resting', 1, p.name))
            elif i == 2:
                players.append(person.Player('left', self.game_data, 777, 317, 'battle resting', 1, p.name))
            playerentities.append(p)
            players[i].image = pg.transform.scale2x(players[i].image)
        return players, playerentities
        
    def make_monster(self):
        """
        Make the lists of sprites and data for the monsters
        """
        monsters = []
        monsterentities = []
        k = 0
        temppos = [(840,30), (660, 30), (810, 135), (655,160), (500, 195), (640, 270), (700,370), (850, 380), (815,245)]
        for i, c in enumerate(self.game_data['conductors']):
            for j, m in enumerate(c.monsters):
                monsters.append(person.Player('left', self.game_data, temppos[i*3+j][0], temppos[i*3+j][1], 'battle resting', 1, m.species))
                monsterentities.append(m)
                monsters[k].image = pg.transform.scale2x(monsters[k].image)
                k+=1
        return monsters, monsterentities

    def make_selection_state_dict(self):
        """
        Make a dictionary of states with arrow coordinates as keys.
        """
        index_list = range(6)
        state_list = [self.enter_select_enemy_attack_state, self.enter_select_magic_state,
                      self.enter_select_item_state, self.enter_select_symphony_state,
                      self.next_turn, self.try_to_run_away]
        return dict(izip(index_list, state_list))

    def update(self, surface, keys, current_time):
        """
        Update the battle state.
        """
        self.current_time = current_time
        self.check_input(keys)
        self.check_timed_events()
        self.check_if_battle_won()
        self.enemy_group.update(current_time)
        for p in self.players:
            p.update(keys, current_time)
        for m in self.monsters:
            m.update(keys, current_time)
        self.attack_animations.update()
        self.info_box.update(keys, self.currentmonster)
        self.arrow.update(keys)
        self.damage_points.update()
        self.execute_player_actions()

        self.draw_battle(surface)

    def check_input(self, keys):
        """
        Check user input to navigate GUI.
        """
        if self.allow_input:
            if keys[pg.K_z]:
                if self.state == c.SELECT_ACTION:
                    self.notify(c.CLICK2)
                    enter_state_function = self.select_action_state_dict[self.info_box.index]
                    enter_state_function()

                elif self.state == c.SELECT_ENEMY_ATTACK:
                    self.notify(c.CLICK2)
                    if self.monsterentities[self.currentmonster].stats['curr']['notes'] > 1:
                        if self.monsterentities[self.currentmonster].equipment['instrument']:
                            self.maxhits = self.monsterentities[self.currentmonster].equipment['instrument'].stats['base']['hits']
                        else:
                            self.maxhits = 5
                        self.monsterentities[self.currentmonster].stats['curr']['notes'] -= 2
                        for x in range(self.maxhits):
                            self.player_actions.append(c.PLAYER_ATTACK)
                            self.enemies_to_attack.append(self.enemy_list[self.arrow.index])
                        self.action_selected = True
                
                elif self.state == c.SELECT_MAGIC:
                    self.notify(c.CLICK2)
                    trueindex = self.arrow.index + self.info_box.itemindex
                    print trueindex
                    self.enter_select_action_state()
                
                elif self.state == c.SELECT_ENEMY_SPELL:
                    self.notify(c.CLICK2)
                    if self.info_box.state == c.ATTACK:
                        if self.monsterentities[self.currentmonster].equipment['instrument']:
                            self.maxhits = self.monsterentities[self.currentmonster].equipment['instrument'].stats['base']['hits']
                        else:
                            self.maxhits = 5
                        for x in range(maxhits):
                            self.player_actions.append(c.PLAYER_ATTACK)
                            self.enemies_to_attack.append(self.get_enemy_to_attack())
                    self.action_selected = True

                elif self.state == c.SELECT_ITEM:
                    self.notify(c.CLICK2)
                    if self.arrow.index == (len(self.arrow.pos_list) - 1):
                        self.enter_select_action_state()
                    elif self.info_box.item_text_list[self.arrow.index][:14] == 'Healing Potion':
                        if 'Healing Potion' in self.game_data['player inventory']:
                            self.player_actions.append(c.DRINK_HEALING_POTION)
                            self.action_selected = True
                    elif self.info_box.item_text_list[self.arrow.index][:5] == 'Ether':
                        if 'Ether Potion' in self.game_data['player inventory']:
                            self.player_actions.append(c.DRINK_ETHER_POTION)
                            self.action_selected = True
                elif self.state == c.SELECT_MAGIC:
                    self.notify(c.CLICK2)
                    if self.arrow.index == (len(self.arrow.pos_list) - 1):
                        self.enter_select_action_state()
                    elif self.info_box.magic_text_list[self.arrow.index] == 'Cure':
                        magic_points = self.game_data['player inventory']['Cure']['magic points']
                        if self.temp_magic >= magic_points:
                            self.temp_magic -= magic_points
                            self.player_actions.append(c.DEF_SPELL)
                            self.action_selected = True
                    elif self.info_box.magic_text_list[self.arrow.index] == 'Fire Blast':
                        magic_points = self.game_data['player inventory']['Fire Blast']['magic points']
                        if self.temp_magic >= magic_points:
                            self.temp_magic -= magic_points
                            self.player_actions.append(c.OFF_SPELL)
                            self.action_selected = True

            elif keys[pg.K_x]:
                if self.state == c.SELECT_ENEMY_ATTACK:
                    self.state = self.arrow.state = c.SELECT_ACTION
                    self.info_box.state = c.ATTACK
                    self.arrow.index = 0
                elif self.state == c.SELECT_ENEMY_SPELL:
                    self.state = self.arrow.state = c.SELECT_ACTION
                    self.info_box.state = c.SPELL
                    self.arrow.index = 0
                elif self.state == c.SELECT_ITEM:
                    self.notify(c.CLICK2)
                    self.enter_select_action_state()
                    self.info_box.state = c.ITEM
                    self.info_box.itemindex = 0
                elif self.state == c.SELECT_MAGIC:
                    self.notify(c.CLICK2)
                    self.enter_select_action_state()
                    self.info_box.state = c.SPELL
                    self.info_box.itemindex = 0
                    
            self.allow_input = False
        


        if keys[pg.K_RETURN] == False and keys[pg.K_z] == False and keys[pg.K_x] == False:
            self.allow_input = True

    def check_timed_events(self):
        """
        Check if amount of time has passed for timed events.
        """
        timed_states = [c.PLAYER_DAMAGED,
                        c.ENEMY_DAMAGED,
                        c.ENEMY_DEAD,
                        c.DRINK_HEALING_POTION,
                        c.DRINK_ETHER_POTION]
        long_delay = timed_states
        if self.state in long_delay:
            if (self.current_time - self.timer) > 300:
                if self.state == c.ENEMY_DAMAGED:
                    if self.player_actions:
                        self.player_action_dict[self.player_actions[0]]()
                        self.player_actions.pop(0)
                        self.currhits += 1
                    else:
                        if not len(self.enemy_list):
                            self.enter_battle_won_state()
                        elif self.currentmonster < len(self.monsters)-1:
                            self.monsterentities[self.currentmonster].stats['curr']['notes'] += self.monsterentities[self.currentmonster].stats['curr']['notegain'] + self.monsterentities[self.currentmonster].stats['bonus']['bonusnotegain'] - self.monsterentities[self.currentmonster].stats['penalty']['penaltynotegain']
                            self.currentmonster+=1
                            self.info_box.currentmonster+=1
                            self.enter_select_action_state()
                            self.currhits = 0
                        elif len(self.enemy_list):
                            self.monsterentities[self.currentmonster].stats['curr']['notes'] += self.monsterentities[self.currentmonster].stats['curr']['notegain'] + self.monsterentities[self.currentmonster].stats['bonus']['bonusnotegain'] - self.monsterentities[self.currentmonster].stats['penalty']['penaltynotegain']
                            self.enemy_index = 0
                            self.currhits = 0
                            self.enter_enemy_AI_state()
                
                elif self.state == c.PLAYER_DAMAGED:
                    if self.enemy_actions:
                        self.enemy_action_dict[self.enemy_actions.pop(0)]()
                        self.currhits+=1
                    elif self.enemy_index == (len(self.enemy_list) - 1):
                        self.currhits = 0
                        self.currentmonster = 0
                        if self.run_away:
                            self.enter_run_away_state()
                        else:
                            self.enter_select_action_state()
                    else:
                        self.currhits = 0
                        self.switch_enemy()
                        
                elif (self.state == c.DRINK_HEALING_POTION or
                      self.state == c.DEF_SPELL or
                      self.state == c.DRINK_ETHER_POTION):
                    if self.player_actions:
                        self.player_action_dict[self.player_actions[0]]()
                        self.player_actions.pop(0)
                    else:
                        if len(self.enemy_list):
                            self.enter_enemy_AI_state()
                        else:
                            self.enter_battle_won_state()
                self.timer = self.current_time

        elif self.state == c.OFF_SPELL or self.state == c.DEF_SPELL:
            if (self.current_time - self.timer) > 1500:
                if self.player_actions:
                    if not len(self.enemy_list):
                        self.enter_battle_won_state()
                    else:
                        self.player_action_dict[self.player_actions[0]]()
                        self.player_actions.pop(0)
                else:
                    if len(self.enemy_list):
                        self.enter_enemy_AI_state()
                    else:
                        self.enter_battle_won_state()
                self.timer = self.current_time

        elif self.state == c.RUN_AWAY:
            if (self.current_time - self.timer) > 1500:
                self.end_battle()

        elif self.state == c.BATTLE_WON:
            if (self.current_time - self.timer) > 1960:
                self.enter_show_gold_state()

        elif self.state == c.SHOW_GOLD:
            if (self.current_time - self.timer) > 1960:
                self.enter_show_experience_state()

        
        #elif self.state == c.LEVEL_UP:
        #    if (self.current_time - self.timer) > 2200:
        #        if self.game_data['player stats']['Level'] == 3:
        #            self.enter_two_actions_per_turn_state()
        #        else:
        #            self.end_battle()

        elif self.state == c.SHOW_EXPERIENCE:
            if (self.current_time - self.timer) > 2200:
                for m in self.monsterentities:
                    m.gainTP(self.experience_points)
                else:
                    self.end_battle()


    def check_if_battle_won(self):
        """
        Check if state is SELECT_ACTION and there are no enemies left.
        """
        if self.state in self.info_box.command_list:
            if len(self.enemy_group) == 0:
                self.enter_battle_won_state()

    def notify(self, event):
        """
        Notify observer of event.
        """
        for new_observer in self.observers:
            new_observer.on_notify(event)

    def end_battle(self):
        """
        End battle and flip back to previous state.
        """
        if self.game_data['battle type'] == 'evilwizard':
            self.game_data['crown quest'] = True
            self.game_data['talked to king'] = True
        self.game_data['last state'] = self.name
        self.game_data['battle counter'] = random.randint(50, 255)
        self.game_data['battle type'] = None
        for co in self.game_data['conductors']:
            for m in co.monsters:
                m.stats['curr']['notes'] = 4
        self.state = 'transition out'

    def attack_enemy(self, enemy_damage):
        enemy = self.monsters[self.currentmonster].attacked_enemy
        enemyindex = self.enemy_list.index(enemy)
        self.enemyentities[enemyindex].damage(enemy_damage)
        self.set_enemy_indices()

        if enemy:
            enemy.enter_knock_back_state()
            if self.enemyentities[enemyindex].stats['curr']['HP'] <= 0 and len(self.player_actions) == 1:
                self.enemy_list.pop(enemy.index)
                self.enemyentities.pop(enemyindex)
                enemy.state = c.FADE_DEATH
                self.arrow.remove_pos(enemyindex)
            self.enemy_index = 0

    def set_enemy_indices(self):
        for i, enemy in enumerate(self.enemy_list):
            enemy.index = i

    def draw_battle(self, surface):
        """Draw all elements of battle state"""
        self.background.draw(surface)
        self.enemy_group.draw(surface)
        self.attack_animations.draw(surface)
        for p in self.players:
            surface.blit(p.image, p.rect)
        for m in self.monsters:
            surface.blit(m.image, m.rect)
        surface.blit(self.info_box.image, self.info_box.rect)
        #surface.blit(self.select_box.image, self.select_box.rect)
        #surface.blit(self.arrow.image, self.arrow.rect)
        self.arrow.draw(surface)
        #self.player_health_box.draw(surface)
        self.damage_points.draw(surface)
        self.draw_transition(surface)

    def draw_transition(self, surface):
        """
        Fade in and out of state.
        """
        if self.state == 'transition in':

            transition_image = pg.Surface(self.transition_rect.size)
            transition_image.fill(c.TRANSITION_COLOR)
            transition_image.set_alpha(self.transition_alpha)
            surface.blit(transition_image, self.transition_rect)
            self.transition_alpha -= c.TRANSITION_SPEED 
            if self.transition_alpha <= 0:
                self.state = c.SELECT_ACTION
                self.transition_alpha = 0

        elif self.state == 'transition out':
            transition_image = pg.Surface(self.transition_rect.size)
            transition_image.fill(c.TRANSITION_COLOR)
            transition_image.set_alpha(self.transition_alpha)
            surface.blit(transition_image, self.transition_rect)
            self.transition_alpha += c.TRANSITION_SPEED 
            if self.transition_alpha >= 255:
                self.done = True

        elif self.state == c.DEATH_FADE:
            transition_image = pg.Surface(self.transition_rect.size)
            transition_image.fill(c.TRANSITION_COLOR)
            transition_image.set_alpha(self.transition_alpha)
            surface.blit(transition_image, self.transition_rect)
            self.transition_alpha += c.DEATH_TRANSITION_SPEED
            if self.transition_alpha >= 255:
                self.done = True
                self.next = c.DEATH_SCENE

    def player_damaged(self, monster, damage):
        monster.damage(damage)
        if monster.isDead:
            monster.stats['curr']['HP'] = 0
            self.state = c.DEATH_FADE

    def player_healed(self, heal, magic_points=0):
        """
        Add health from potion to game data.
        """
        health = self.game_data['player stats']['health']

        health['current'] += heal
        if health['current'] > health['maximum']:
            health['current'] = health['maximum']

        if self.state == c.DRINK_HEALING_POTION:
            self.game_data['player inventory']['Healing Potion']['quantity'] -= 1
            if self.game_data['player inventory']['Healing Potion']['quantity'] == 0:
                del self.game_data['player inventory']['Healing Potion']
        elif self.state == c.DEF_SPELL:
            self.game_data['player stats']['magic']['current'] -= magic_points

    def magic_boost(self, magic_points):
        """
        Add magic from ether to game data.
        """
        magic = self.game_data['player stats']['magic']
        magic['current'] += magic_points
        self.temp_magic += magic_points
        if magic['current'] > magic['maximum']:
            magic['current'] = magic['maximum']

        self.game_data['player inventory']['Ether Potion']['quantity'] -= 1
        if not self.game_data['player inventory']['Ether Potion']['quantity']:
            del self.game_data['player inventory']['Ether Potion']

    def set_timer_to_current_time(self):
        """Set the timer to the current time."""
        self.timer = self.current_time

    def cast_fire_blast(self):
        """
        Cast fire blast on all enemies.
        """
        self.notify(c.FIRE)
        self.state = self.info_box.state = c.OFF_SPELL
        POWER = self.inventory['Fire Blast']['power']
        MAGIC_POINTS = self.inventory['Fire Blast']['magic points']
        self.game_data['player stats']['magic']['current'] -= MAGIC_POINTS
        for enemy in self.enemy_list:
            DAMAGE = random.randint(POWER//2, POWER)
            self.damage_points.add(
                attackitems.HealthPoints(DAMAGE, enemy.rect.topright))
            enemy.health -= DAMAGE
            posx = enemy.rect.x - 32
            posy = enemy.rect.y - 64
            fire_sprite = attack.Fire(posx, posy)
            self.attack_animations.add(fire_sprite)
            if enemy.health <= 0:
                enemy.kill()
                self.arrow.remove_pos(enemy)
            else:
                enemy.enter_knock_back_state()
        self.enemy_list = [enemy for enemy in self.enemy_list if enemy.health > 0]
        self.enemy_index = 0
        self.arrow.index = 0
        self.arrow.state = 'invisible'
        self.set_timer_to_current_time()

    def cast_cure(self):
        """
        Cast cure spell on player.
        """
        self.state = c.DEF_SPELL
        HEAL_AMOUNT = self.inventory['Cure']['power']
        MAGIC_POINTS = self.inventory['Cure']['magic points']
        self.player.healing = True
        self.set_timer_to_current_time()
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(HEAL_AMOUNT, self.player.rect.topright, False))
        self.player_healed(HEAL_AMOUNT, MAGIC_POINTS)
        self.info_box.state = c.DRINK_HEALING_POTION
        self.notify(c.POWERUP)
    
    def enter_select_enemy_attack_state(self):
        """
        Transition battle into the select enemy state.
        """
        self.state = self.arrow.state = self.info_box.state = c.SELECT_ENEMY_ATTACK
        self.arrow.index = 0
        
    def enter_select_symphony_state(self):
        pass
    
    def next_turn(self):
        self.monsterentities[self.currentmonster].stats['curr']['notes'] += self.monsterentities[self.currentmonster].stats['curr']['notegain'] + self.monsterentities[self.currentmonster].stats['bonus']['bonusnotegain'] - self.monsterentities[self.currentmonster].stats['penalty']['penaltynotegain']
        self.action_selected = False
        if self.currentmonster < len(self.monsters)-1:
            self.enter_select_action_state()
            self.currhits = 0
            self.currentmonster+=1
            self.info_box.currentmonster+=1
        elif len(self.enemy_list):
            self.arrow.index = 0
            self.currhits = 0
            self.enemy_index = 0
            self.arrow.state = 'invisible'
            self.enter_enemy_AI_state()

    def enter_select_item_state(self):
        """
        Transition battle into the select item state.
        """
        self.state = self.info_box.state = c.SELECT_ITEM
        self.arrow.become_select_item_state()

    def enter_select_magic_state(self):
        """
        Transition battle into the select magic state.
        """
        self.state = self.info_box.state = c.SELECT_MAGIC
        self.arrow.become_select_magic_state()

    def try_to_run_away(self):
        """
        Transition battle into the run away state.
        """
        self.run_away = True
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.currentmonster = len(self.monsterentities)
        self.enter_enemy_AI_state()

    def enter_enemy_AI_state(self):
        enemy = self.enemy_list[self.enemy_index]
        enemyent = self.enemyentities[self.enemy_index]
        for action in enemyent.AI:
            if action[4] > random.randint(0, 99):    # will the action occur at all by probability
                #print ("%s passed probability test") %(action[0])
                if action[2] is not None:            # does the action have a specific condition
                    if action[2].endswith(('<', '>', '=')):    # is it an absolute comparison action, thus using action[3]
                        if action[1] == 'enemy':
                            targetgroup = self.monsterentities
                        elif action[1] == 'ally':
                            targetgroup = self.enemyentities
                        elif action[1] == 'self':
                            targetgroup = [enemyent]
                        
                        if action[2] == 'turn>':
                            comparison = (turn>action[3])
                        elif action[2] == 'turn<':
                            comparison = (turn<action[3])
                        elif action[2] == 'turn=':
                            comparison = (turn==action[3])
                        elif action[2].startswith("self"):
                            comparison, target = spellhandler.compareStat(action[2], action[3], self, [enemyent])
                        elif action[2].startswith("ally"):
                            comparison, target = spellhandler.compareStat(action[2], action[3], self, self.enemyentities)
                        elif action[2].startswith("enemy"):
                            comparison, target = spellhandler.compareStat(action[2], action[3], self, self.monsterentities)
                        else:                                    # default, no prefix
                            comparison, target = spellhandler.compareStat(action[2], action[3], self, targetgroup)
                        
                        if comparison:
                            act = [action[0], target]
                            break
                    
                    else:                            # if finding extreme value rather than simple comparison
                        if action[1] == "ally":
                            targetgroup = self.enemyentities
                        elif action[1] == "enemy":
                            targetgroup = self.monsterentities
                            
                        target = spellhandler.findExtreme(action[2], targetgroup)
                        act = [action[0], target]
                        break
                            
                        
                        
                else:                                # if the action has no specific condition
                    act = [action[0], self.monsterentities[random.randint(0,len(self.monsterentities)-1)]]
                        
        #print ("%s will use %s on %s here") %(enemyent.name, act[0], act[1].name)

        '''
        if act[0] == 'attack':
            self.maxhits = random.randint(1,3)
            for x in range(self.maxhits):
                self.enemy_actions.append(c.ENEMY_ATTACK)
                self.monsters_to_attack.append(self.monsters[self.monsterentities.index(act[1])])
            self.enemy_action_dict[self.enemy_actions.pop(0)]()
        '''
        self.maxhits = random.randint(1,3)
        for x in range(self.maxhits):
            self.enemy_actions.append(c.ENEMY_ATTACK)
            self.monsters_to_attack.append(self.monsters[self.monsterentities.index(act[1])])
        self.enemy_action_dict[self.enemy_actions.pop(0)]()
        
        
    def enter_enemy_attack_state(self):
        """
        Transition battle into the Enemy attack state.
        """
        self.state = self.info_box.state = c.ENEMY_ATTACK
        monster_to_attack = self.monsters_to_attack.pop(0)
        enemy = self.enemy_list[self.enemy_index]
        enemy.enter_enemy_attack_state(monster_to_attack)

    def enter_player_attack_state(self):
        """
        Transition battle into the Player attack state.
        """
        self.state = self.info_box.state = c.PLAYER_ATTACK
        enemy_to_attack = self.enemies_to_attack.pop(0)
        if enemy_to_attack in self.enemy_list:
            self.monsters[self.currentmonster].enter_attack_state(enemy_to_attack)
        else:
            if self.enemy_list:
                self.monsters[self.currentmonster].enter_attack_state(self.enemy_list[0])
            else:
                self.enter_battle_won_state()
        self.arrow.state = 'invisible'
        self.notify(c.ENEMY_DAMAGED)



    def enter_drink_healing_potion_state(self):
        """
        Transition battle into the Drink Healing Potion state.
        """
        self.state = self.info_box.state = c.DRINK_HEALING_POTION
        self.player.healing = True
        self.set_timer_to_current_time()
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(30,
                                     self.player.rect.topright,
                                     False))
        self.player_healed(30)
        self.notify(c.POWERUP)

    def enter_drink_ether_potion_state(self):
        """
        Transition battle into the Drink Ether Potion state.
        """
        self.state = self.info_box.state = c.DRINK_ETHER_POTION
        self.player.healing = True
        self.arrow.state = 'invisible'
        self.enemy_index = 0
        self.damage_points.add(
            attackitems.HealthPoints(30,
                                     self.player.rect.topright,
                                     False,
                                     True))
        self.magic_boost(30)
        self.set_timer_to_current_time()
        self.notify(c.POWERUP)

    def enter_select_action_state(self):
        """
        Transition battle into the select action state
        """
        self.state = c.SELECT_ACTION
        self.info_box.state = c.ATTACK
        self.info_box.index = 0
        self.info_box.itemindex = 0
        self.arrow.index = 0
        self.arrow.state = c.SELECT_ACTION

    def enter_player_damaged_state(self):
        """
        Transition battle into the player damaged state.
        """
        self.state = self.info_box.state = c.PLAYER_DAMAGED
        if self.enemy_index > len(self.enemy_list) - 1:
            self.enemy_index = 0
        enemy = self.enemy_list[self.enemy_index]
        target = enemy.attacked_monster
        targetindex = self.monsters.index(target)
        player_damage = int(self.enemyentities[self.enemy_index].calculate_attack_damage(self.monsterentities[targetindex], self.currhits))

        self.damage_points.add(
            attackitems.HealthPoints(player_damage,
                                     target.rect.topright))
        self.info_box.set_player_damage(player_damage)
        self.info_box.set_player_index(targetindex)
        self.set_timer_to_current_time()
        self.player_damaged(self.monsterentities[targetindex], player_damage)
        if player_damage:
            sfx_num = random.randint(1,3)
            self.notify('punch{}'.format(sfx_num))
            target.damaged = True
            target.enter_knock_back_state()
        else:
            self.notify(c.MISS)

    def enter_enemy_damaged_state(self):
        """
        Transition battle into the enemy damaged state.
        """
        self.state = self.info_box.state = c.ENEMY_DAMAGED
        enemy = self.monsters[self.currentmonster].attacked_enemy
        enemyindex = self.enemy_list.index(enemy)
        enemy_damage = int(self.monsterentities[self.currentmonster].calculate_attack_damage(self.enemyentities[enemyindex], self.currhits))
        self.damage_points.add(
            attackitems.HealthPoints(enemy_damage,
                                     self.monsters[self.currentmonster].attacked_enemy.rect.topright))
        self.info_box.set_enemy_index(enemyindex)
        self.info_box.set_enemy_damage(enemy_damage)
        
        #print "%s %s %d %d" %(enemy.name, self.enemyentities[enemyindex].name, enemyindex, self.info_box.enemyindex)
        #print [e.name for e in self.enemy_list]
        #print [x.name for x in self.enemyentities]
        #print [i.name for i in self.info_box.enemyentities]
        #print [g.name for g in self.enemy_group.sprites()]

        self.arrow.index = 0
        self.attack_enemy(enemy_damage)
        self.set_timer_to_current_time()

    def switch_enemy(self):
        """
        Switch which enemy the player is attacking.
        """
        if self.enemy_index < len(self.enemy_list) - 1:
            self.enemy_index += 1
            self.enter_enemy_AI_state()

    def enter_run_away_state(self):
        """
        Transition battle into the run away state.
        """
        self.state = self.info_box.state = c.RUN_AWAY
        self.arrow.state = 'invisible'
        for p in self.players:
            p.state = c.RUN_AWAY
        for m in self.monsters:
            m.state = c.RUN_AWAY
        self.set_timer_to_current_time()
        self.notify(c.RUN_AWAY)

    def enter_battle_won_state(self):
        """
        Transition battle into the battle won state.
        """
        self.notify(c.BATTLE_WON)
        self.state = self.info_box.state = c.BATTLE_WON
        for p in self.players:
            p.state = c.VICTORY_DANCE
        self.set_timer_to_current_time()

    def enter_show_gold_state(self):
        """
        Transition battle into the show gold state.
        """
        self.game_data['gold'] += self.new_gold
        self.state = self.info_box.state = c.SHOW_GOLD
        self.set_timer_to_current_time()

    def enter_show_experience_state(self):
        """
        Transition battle into the show experience state.
        """
        self.state = self.info_box.state = c.SHOW_EXPERIENCE
        self.set_timer_to_current_time()

    def enter_level_up_state(self):
        """
        Transition battle into the LEVEL UP state.
        """
        self.state = self.info_box.state = c.LEVEL_UP
        self.info_box.reset_level_up_message()
        self.set_timer_to_current_time()

    def enter_two_actions_per_turn_state(self):
        self.state = self.info_box.state = c.TWO_ACTIONS
        self.set_timer_to_current_time()

    def execute_player_actions(self):
        """
        Execute the player actions.
        """
        if len(self.player_actions) >= self.maxhits:
            enter_state = self.player_action_dict[self.player_actions[0]]
            enter_state()
            self.player_actions.pop(0)
            self.currhits += 1
            self.action_selected = False
			
        else:
            if self.action_selected:
                self.currhits = 0
                self.enter_select_action_state()
                self.action_selected = False








