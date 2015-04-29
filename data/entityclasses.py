import pygame, sys, init, random
import compositeclasses
import itemhandler, spellhandler

class Monster(object):
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.spells = []
		self.status = []
		self.isDead = False
		self.canMove = True

class WildMonster(Monster):
	def __init__(self, name, index):
		super(WildMonster, self).__init__(name, index)
		self.AI, self.stats = init.wildMonster_Init(name)
		self.itemDrops = []
		
	def calculate_attack_damage(self, target, currhits):
		atk = (self.stats['base']['atk'] + self.stats['bonus']['bonusatk'] - self.stats['penalty']['penaltyatk'])
		enemydefmod = (1.0-(0.30*(target.stats['base']['def'] + target.stats['bonus']['bonusdef'] - target.stats['penalty']['penaltydef'])/1000))
		currentdamage = atk*0.25 * enemydefmod * (self.stats['curr']['proration'] ** currhits)
		return currentdamage
	
	def damage(self, num):
		if num <= self.stats['curr']['HP']:
			self.stats['curr']['HP'] -= int(num)
		else:
			self.stats['curr']['HP'] = 0
		#print "%d dealt! %d HP left." %(num, self.stats['curr']['HP'])
		if self.stats['curr']['HP'] == 0:
			self.isDead = True
			self.canMove = False
			#print "%s died" %self.name
	
	def heal(self, num):
		self.stats['curr']['HP'] += int(num)
		if self.stats['curr']['HP'] > (self.stats['base']['HP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP']):
			self.stats['curr']['HP'] = (self.stats['base']['HP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP'])
			
	def addStatus(self, status):
		self.status.append(status)
		print "Applied %s on %s for %d turns!" %(status.name, self.name, status.duration)
	
	def processAI(self, turn, wildmonsters, tamedmonsters):
		act = []
		for action in self.AI:
			if action[4] > random.randint(0, 99):	# will the action occur at all by probability
				print ("%s passed probability test") %(action[0])
				if action[2] is not None:			# does the action have a specific condition
					if action[2].endswith(('<', '>', '=')):	# is it an absolute comparison action, thus using action[3]
						if action[1] == 'enemy':
							targetgroup = tamedmonsters
						elif action[1] == 'ally':
							targetgroup = wildmonsters
						elif action[1] == 'self':
							targetgroup = [self]
					
						if action[2] == 'turn>':
							comparison = (turn>action[3])
						elif action[2] == 'turn<':
							comparison = (turn<action[3])
						elif action[2] == 'turn=':
							comparison = (turn==action[3])
						elif action[2].startswith("self"):
							comparison, target = spellhandler.compareStat(action[2], action[3], self, [self])
						elif action[2].startswith("ally"):
							comparison, target = spellhandler.compareStat(action[2], action[3], self, wildmonsters)
						elif action[2].startswith("enemy"):
							comparison, target = spellhandler.compareStat(action[2], action[3], self, tamedmonsters)
						else:									# default, no prefix
							comparison, target = spellhandler.compareStat(action[2], action[3], self, targetgroup)
						
						if comparison:
							act = [action[0], target]
							break
					
					else:							# if finding extreme value rather than simple comparison
						if action[1] == "ally":
							targetgroup = wildmonsters
						elif action[1] == "enemy":
							targetgroup = tamedmonsters
						
						target = spellhandler.findExtreme(action[2], targetgroup)
						act = [action[0], target]
						break
							
						
						
				else:								# if the action has no specific condition
					act = [action[0], tamedmonsters[random.randint(0,len(tamedmonsters)-1)]]
					
		print ("%s will use %s on %s here") %(self.name, act[0], act[1].name)
		'''
		if act == 'attack':
			
		
		elif act == 'offspell':
			pass
		
		elif act == 'defspell':
			pass
		
		elif act == 'debspell':
			pass
			
		else
		'''

class TamedMonster(Monster):
	def __init__(self, name, species, index):
		super(TamedMonster, self).__init__(name, index)
		self.master = None
		self.species = species
		self.stats = init.tamedMonster_Init(species)
		self.equipment = {
			'instrument': None,
			'accessory1': None,
			'accessory2': None
		}
	
	def printstats(self):
		print "Name: %s" % (self.name)
		print "Index: %s" % (self.index)
		print sorted(self.stats['base'].iteritems())
		print sorted(self.stats['curr'].iteritems())
		print sorted(self.stats['bonus'].iteritems())
		print sorted(self.stats['penalty'].iteritems())
		
	def gainTP(self, gainedprog):
		storedprog = 0
		while(gainedprog != 0):
			if (gainedprog > (self.stats['tp']['nexttp'] - self.stats['tp']['tpprog'])):
				storedprog = self.stats['tp']['nexttp'] - self.stats['tp']['tpprog']
				gainedprog -= storedprog
			else:
				storedprog = gainedprog
				gainedprog = 0
		
			self.stats['tp']['tpprog'] += storedprog
			
			#when leveling up
			if self.stats['tp']['tpprog'] ==  self.stats['tp']['nexttp']:
				self.stats['tp']['tp'] += 1
				self.stats['tp']['totaltp'] += 1
				if (self.stats['tp']['totaltp'] >= 500):
					self.stats['tp']['nexttp'] *= 1.005
				elif (self.stats['tp']['totaltp'] >= 250):
					self.stats['tp']['nexttp'] *= 1.015
				elif (self.stats['tp']['totaltp'] >= 100):
					self.stats['tp']['nexttp'] *= 1.025
				elif (self.stats['tp']['totaltp'] >= 50):
					self.stats['tp']['nexttp'] *= 1.75
				elif (self.stats['tp']['totaltp'] >= 20):
					self.stats['tp']['nexttp'] *= 1.8
				else:
					self.stats['tp']['nexttp'] *= 2
			
			self.stats['tp']['nexttp'] = int(self.stats['tp']['nexttp'])

	def setMaster(self, newmaster):
		self.master = newmaster

	def regenNotes(self):
		self.stats['curr']['notes'] += self.stats['curr']['notegain'] + self.stats['bonus']['bonusnotegain'] - self.stats['penalty']['penaltynotegain']
		if self.stats['curr']['notes'] >=10:
			self.stats['curr']['notes'] = 10
		
	def equip(self, equipment, slot):
		self.equipment[slot] = equipment
		self.stats['bonus']['bonusHP'] += equipment.stats['bonus']['bonusHP']
		self.stats['bonus']['bonusatk'] += equipment.stats['bonus']['bonusatk']
		self.stats['bonus']['bonusdef'] += equipment.stats['bonus']['bonusdef']
		self.stats['bonus']['bonusmus'] += equipment.stats['bonus']['bonusmus']
		self.stats['bonus']['bonusfoc'] += equipment.stats['bonus']['bonusfoc']
		self.stats['bonus']['bonuscla'] += equipment.stats['bonus']['bonuscla']
		self.stats['bonus']['bonusrhy'] += equipment.stats['bonus']['bonusrhy']
		self.stats['bonus']['bonusnotegain'] += equipment.stats['bonus']['bonusnotegain']
		self.stats['penalty']['penaltyHP'] += equipment.stats['penalty']['penaltyHP']
		self.stats['penalty']['penaltyatk'] += equipment.stats['penalty']['penaltyatk']
		self.stats['penalty']['penaltydef'] += equipment.stats['penalty']['penaltydef']
		self.stats['penalty']['penaltymus'] += equipment.stats['penalty']['penaltymus']
		self.stats['penalty']['penaltyfoc'] += equipment.stats['penalty']['penaltyfoc']
		self.stats['penalty']['penaltycla'] += equipment.stats['penalty']['penaltycla']
		self.stats['penalty']['penaltyrhy'] += equipment.stats['penalty']['penaltyrhy']
		self.stats['penalty']['penaltynotegain'] += equipment.stats['penalty']['penaltynotegain']
    
	def unequip(self, slot):
		equipment = self.equipment[slot]
		self.stats['bonus']['bonusHP'] -= equipment.stats['bonus']['bonusHP']
		self.stats['bonus']['bonusatk'] -= equipment.stats['bonus']['bonusatk']
		self.stats['bonus']['bonusdef'] -= equipment.stats['bonus']['bonusdef']
		self.stats['bonus']['bonusmus'] -= equipment.stats['bonus']['bonusmus']
		self.stats['bonus']['bonusfoc'] -= equipment.stats['bonus']['bonusfoc']
		self.stats['bonus']['bonuscla'] -= equipment.stats['bonus']['bonuscla']
		self.stats['bonus']['bonusrhy'] -= equipment.stats['bonus']['bonusrhy']
		self.stats['bonus']['bonusnotegain'] -= equipment.stats['bonus']['bonusnotegain']
		self.stats['penalty']['penaltyHP'] -= equipment.stats['penalty']['penaltyHP']
		self.stats['penalty']['penaltyatk'] -= equipment.stats['penalty']['penaltyatk']
		self.stats['penalty']['penaltydef'] -= equipment.stats['penalty']['penaltydef']
		self.stats['penalty']['penaltymus'] -= equipment.stats['penalty']['penaltymus']
		self.stats['penalty']['penaltyfoc'] -= equipment.stats['penalty']['penaltyfoc']
		self.stats['penalty']['penaltycla'] -= equipment.stats['penalty']['penaltycla']
		self.stats['penalty']['penaltyrhy'] -= equipment.stats['penalty']['penaltyrhy']
		self.stats['penalty']['penaltynotegain'] -= equipment.stats['penalty']['penaltynotegain']
		self.equipment[slot] = None
		self.master.addItem(equipment)
        
		
	def addSpell(self, spell):
		self.spells.append(spell)
	
	def damage(self, num):
		if num <= self.stats['curr']['HP']:
			self.stats['curr']['HP'] -= int(num)
		else:
			self.stats['curr']['HP'] = 0
		#print "%d dealt! %d HP left." %(num, self.stats['curr']['HP'])
		if self.stats['curr']['HP'] == 0:
			self.isDead = True
			
	def heal(self, num):
		self.stats['curr']['HP'] += int(num)
		if self.stats['curr']['HP'] > (self.stats['base']['HP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP']):
			self.stats['curr']['HP'] = (self.stats['base']['HP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP'])
	
	def calculate_attack_damage(self, target, currhits):
		atk = (self.stats['base']['atk'] + self.stats['bonus']['bonusatk'] - self.stats['penalty']['penaltyatk'])
		enemydefmod = (1.0-(0.30*(target.stats['base']['def'] + target.stats['bonus']['bonusdef'] - target.stats['penalty']['penaltydef'])/1000))
		
		if self.equipment['instrument'] == None:
			return (atk*0.1*enemydefmod)
		
		elif self.equipment['instrument'].stats['base']['type'] == 'wind':
		#Wind instruments ignore proration and some defense when critting
			equipmentmultiplier = self.equipment['instrument'].stats['base']['atkmult']
			enemydefmod = (1.0-(0.30*(target.stats['base']['def'] + target.stats['bonus']['bonusdef'] - target.stats['penalty']['penaltydef'])/1200))
			currentDamage = atk * equipmentmultiplier * enemydefmod * (self.equipment['instrument'].stats['base']['proration'] ** currhits)
			if self.equipment['instrument'].stats['base']['critchance'] > random.randint(0, 100):
				#print "Critical!"
				enemydefmod = (1.0-(0.30*(target.stats['base']['def'] + target.stats['bonus']['bonusdef'] - target.stats['penalty']['penaltydef'])/1200))
				return (atk*equipmentmultiplier*enemydefmod*self.equipment['instrument'].stats['base']['critmult'])
			else:
				return (currentDamage)
		
		elif self.equipment['instrument'].stats['base']['type'] == 'string':
			currentDamage = atk * equipmentmultiplier * enemydefmod * (self.equipment['instrument'].stats['base']['proration'] ** currhits)
			if self.equipment['instrument'].stats['base']['critchance'] > random.randint(0, 100):
				#print "Critical!"
				return (currentDamage*self.equipment['instrument'].stats['base']['critmult'])
			else:
				return (currentDamage)
		
		elif self.equipment['instrument'].stats['base']['type'] == 'percussion':
			currentDamage = atk * equipmentmultiplier * (self.equipment['instrument'].stats['base']['proration'] ** currhits)
			return (currentDamage)
				
	def useItem(self, index, target):
		item = self.master.removeItem(index)
		for i, eff in enumerate(item.effectsList):
			if eff[0] == 'rec_HP':
				args = eff[1]
		'''
		print "%s used %s on %s!" %(self.name, item.name, target.name)
		if item.itemType == "Consumable":
			if item.target == "one":
				itemhandler.useItem(item, target)
			else:
				itemhandler.useItemAoE(item, target)
		'''
		return itemhandler.rec_HP(args, target)
				
	def useSpell(self, index, target):
		spell = self.spells[index]
		for i, eff in enumerate(spell.effectsList):
			if eff[0] == 'dmg_HP':
				args = eff[1]
		'''
		if spell.target == "one":
			print "%s used %s on %s!" %(self.name, spell.name, target.name)
			spellhandler.useSpell(spell, self, target)
		
		else:
			namecoll = []
			for x in range(0,len(target)):
				namecoll.append(target[x].name)
			print "%s used %s on " %(self.name, spell.name)
			print namecoll
			spellhandler.useSpellAoE(spell, self, target)
		'''
		return spellhandler.dmg_HP(args, self, target)
	
class Conductor:
	def __init__(self, name):
		self.name = name
		self.monsterLimit = 3
		self.monsters = []
		self.inventory = compositeclasses.Inventory()
		self.conductorskill = None
		self.aptitude = init.conductor_Init(name)
		
	def addMonster(self, monster):
		if self.monsterLimit > len(self.monsters):
			self.monsters.append(monster)
			monster.setMaster(self)
			return True
		else:
			return False
		
	def addMonsterLimit(self):
		if self.monsterLimit < 3:
			monsterLimit += 1
			return True
		else:
			return False
		
	def subtractMonsterLimit(self):
		if self.monsterLimit > 1:
			monsterLimit -= 1
			return True
		else:
			return False
			
	
	def addItem(self, item):
		if self.inventory.getSize() < 64:
			self.inventory.addItem(item)
			return True
		else:
			return False
			
	def getItem(self, index):
		if self.inventory.getSize() > 0:
			return self.inventory.getItem(index)
	
	def removeItem(self, index):
		if self.inventory.getSize() > 0:
			return self.inventory.removeItem(index)

	def inventorySize(self):
		return self.inventory.getSize()
		
	def useItem(self, itemIndex, target):
		self.items[itemIndex].use(target)
	

	def trainMonster(self, monsterindex, statindex):
		basearr = ['HP', 'atk', 'def', 'mus', 'foc', 'cla', 'rhy', 'string', 'wind', 'percussion']
		
		if self.monsters[monsterindex].stats['tp']['tp'] > 0:
			self.monsters[monsterindex].stats['tp']['tp'] -= 1
			if statindex < 7:
				self.monsters[monsterindex].stats['base'][basearr[statindex]] += (self.monsters[monsterindex].stats['gains'][basearr[statindex]] * self.aptitude[basearr[statindex]])
			else:
				self.monsters[monsterindex].stats['base'][basearr[statindex]] += self.aptitude[basearr[statindex]]