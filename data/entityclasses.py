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
		
	def attack(self, target):
		atk = (self.stats['base']['atk'] + self.stats['bonus']['bonusatk'] - self.stats['penalty']['penaltyatk'])
		enemydefmod = (1.0-(0.30*(target.stats['base']['def'] + target.stats['bonus']['bonusdef'] - target.stats['penalty']['penaltydef'])/1000))
		hits = random.randint(1, 5)
		currentdamage = atk*0.25
		for x in range(0,self.stats['curr']['hits']):
			print "Hit %d:" %(x+1)
			target.damage(currentdamage*enemydefmod)
			currentdamage *= self.proration
	
	def damage(self, num):
		if num <= self.stats['curr']['curHP']:
			self.stats['curr']['curHP'] -= int(num)
		else:
			self.stats['curr']['curHP'] = 0
		print "%d dealt! %d HP left." %(num, self.stats['curr']['curHP'])
		if self.stats['curr']['curHP'] == 0:
			self.isDead = True
			self.canMove = False
			print "%s died" %self.name
	
	def heal(self, num):
		self.stats['curr']['curHP'] += int(num)
		if self.stats['curr']['curHP'] > (self.stats['base']['maxHP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP']):
			self.stats['curr']['curHP'] = (self.stats['base']['maxHP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP'])
			
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
	def __init__(self, name, index):
		super(TamedMonster, self).__init__(name, index)
		self.master = None
		self.stats = init.tamedMonster_Init(name)
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
				self.stats['tp'] += 1
				self.stats['totaltp'] += 1
				if (self.stats['tp']['totaltp'] >= 500):
					self.stats['tp']['nexttp'] *= 1.005
				elif (self.stats['tp']['totaltp'] >= 250):
					self.stats['tp']['nexttp'] *= 1.015
				elif (self.stats['tp']['totaltp'] >= 100):
					self.stats['tp']['nexttp'] *= 1.025
				else:
					self.stats['tp']['nexttp'] *= 1.035
		
		
	def setMaster(self, newmaster):
		self.master = newmaster
		
	def setInstrument(self, instrument):
		self.equipment['instrument'] = instrument
		self.stats['bonus']['bonusHP'] += instrument.stats['bonus']['bonusHP']
		self.stats['bonus']['bonusatk'] += instrument.stats['bonus']['bonusatk']
		self.stats['bonus']['bonusdef'] += instrument.stats['bonus']['bonusdef']
		self.stats['bonus']['bonusmus'] += instrument.stats['bonus']['bonusmus']
		self.stats['bonus']['bonusfoc'] += instrument.stats['bonus']['bonusfoc']
		self.stats['bonus']['bonuscla'] += instrument.stats['bonus']['bonuscla']
		self.stats['bonus']['bonusrhy'] += instrument.stats['bonus']['bonusrhy']
		self.stats['bonus']['bonusnotegain'] += instrument.stats['bonus']['bonusnotegain']
		self.stats['penalty']['penaltyHP'] += instrument.stats['penalty']['penaltyHP']
		self.stats['penalty']['penaltyatk'] += instrument.stats['penalty']['penaltyatk']
		self.stats['penalty']['penaltydef'] += instrument.stats['penalty']['penaltydef']
		self.stats['penalty']['penaltymus'] += instrument.stats['penalty']['penaltymus']
		self.stats['penalty']['penaltyfoc'] += instrument.stats['penalty']['penaltyfoc']
		self.stats['penalty']['penaltycla'] += instrument.stats['penalty']['penaltycla']
		self.stats['penalty']['penaltyrhy'] += instrument.stats['penalty']['penaltyrhy']
		self.stats['penalty']['penaltynotegain'] += instrument.stats['penalty']['penaltynotegain']
		
	def addSpell(self, spell):
		self.spells.append(spell)
	
	def damage(self, num):
		if num <= self.stats['curr']['curHP']:
			self.stats['curr']['curHP'] -= int(num)
		else:
			self.stats['curr']['curHP'] = 0
		print "%d dealt! %d HP left." %(num, self.stats['curr']['curHP'])
		if self.stats['curr']['curHP'] == 0:
			self.isDead = True
			print "%s died" %self.name
			
	def heal(self, num):
		self.stats['curr']['curHP'] += int(num)
		if self.stats['curr']['curHP'] > (self.stats['base']['maxHP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP']):
			self.stats['curr']['curHP'] = (self.stats['base']['maxHP'] + self.stats['bonus']['bonusHP'] - self.stats['penalty']['penaltyHP'])
	
	def attack(self, target):
		print "%s attacked %s!" %(self.name, target.name)
		self.stats['curr']['notes'] -= 2
		atk = (self.stats['base']['atk'] + self.stats['bonus']['bonusatk'] - self.stats['penalty']['penaltyatk'])
		equipmentmultiplier = self.equipment['instrument'].stats['base']['atkmult']
		enemydefmod = (1.0-(0.30*(target.stats['base']['def'] + target.stats['bonus']['bonusdef'] - target.stats['penalty']['penaltydef'])/1000))
		if self.equipment['instrument'] == None:
			hits = random.randint(1, 5)
			for x in range(0,hits):
				print "Hit %d:" %(x+1)
				target.damage(atk*0.25*enemydefmod)
		
				
		elif self.equipment['instrument'].stats['base']['type'] == 'wind':
		#Wind instruments ignore proration and some defense when critting
			currentDamage = atk * equipmentmultiplier * enemydefmod
			for x in range(0, self.equipment['instrument'].stats['base']['hits']):
				print "Hit %d:" %(x+1)
				if self.equipment['instrument'].stats['base']['critchance'] > random.randint(0, 100):
					print "Critical!"
					enemydefmod = (1.0-(0.30*(target.stats['base']['def'] + target.stats['bonus']['bonusdef'] - target.stats['penalty']['penaltydef'])/1200))
					target.damage(atk*equipmentmultiplier*enemydefmod*self.equipment['instrument'].stats['base']['critmult'])
				else:
					target.damage(currentDamage)
				currentDamage *= self.equipment['instrument'].stats['base']['proration']
				
		#String instruments have little if any proration		
		elif self.equipment['instrument'].stats['base']['type'] == 'string':
			currentDamage = atk * equipmentmultiplier * enemydefmod
			for x in range(0, self.equipment['instrument'].stats['base']['hits']):
				print "Hit %d:" %(x+1)
				if self.equipment['instrument'].stats['base']['critchance'] > random.randint(0, 100):
					print "Critical!"
					target.damage(currentDamage*self.equipment['instrument'].stats['base']['critmult'])
				else:
					target.damage(currentDamage)
				currentDamage *= self.equipment['instrument'].stats['base']['proration']
				
		#Percussion instruments have a few hits but always pierce defense		
		elif self.equipment['instrument'].stats['base']['type'] == 'percussion':
			currentDamage = atk * equipmentmultiplier
			for x in range(0, self.equipment['instrument'].stats['base']['hits']):
				print "Hit %d:" %(x+1)
				target.damage(currentDamage)
				currentDamage *= self.equipment['instrument'].stats['base']['proration']
				
	def useItem(self, index, target):
		item = self.master.removeItem(index)
		print "%s used %s on %s!" %(self.name, item.name, target.name)
		if item.itemType == "Consumable":
			if item.target == "one":
				itemhandler.useItem(item, target)
			else:
				itemhandler.useItemAoE(item, target)
		self.stats['curr']['notes'] -= 1
				
	def useSpell(self, index, target):
		spell = self.spells[index]
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
		self.stats['curr']['notes'] -= spell.cost
	
class Conductor:
	def __init__(self, name):
		self.name = name
		self.monsterLimit = 1
		self.monsters = []
		self.inventory = compositeclasses.Inventory()
		self.conductorskill = None
		self.aptitude = {
			'hp': 5, 'atk': 5, 'def': 5,
			'mus': 5,'foc': 5,'cla': 5,'rhy': 5,
			'string': 8,'wind': 5,'percussion': 2
		}
		
	def addMonster(self, monster):
		if self.monsterLimit > len(self.monsters):
			self.monsters.append(monster)
		
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
	'''	
	def useItem(self, itemIndex, target):
		self.items[itemIndex].use(target)
	'''
	
	'''
	def trainMonster(self, monster):
		
	'''