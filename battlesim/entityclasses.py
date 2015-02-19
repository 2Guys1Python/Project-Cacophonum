import pygame, sys, init, random
import compositeclasses

class WildMonster:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.stats = init.wildMonster_Init(name)
		self.itemDrops = []
		self.skills = []
		self.status = []
		self.AI = None
	
	def damage(self, num):
		self.stats['curr']['curHP'] -= num
		print "%d dealt! %d HP left." %(num, self.stats['curr']['curHP'])
	

class TamedMonster:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.master = None
		self.stats = init.tamedMonster_Init(name)
		self.equipment = {
			'instrument': None,
			'accessory1': None,
			'accessory2': None
		}
		self.skills = []
		self.status = []
	
	def printstats(self):
		print "Name: %s" % (self.name)
		print "Index: %s" % (self.index)
		print sorted(self.stats['base'].iteritems())
		print sorted(self.stats['curr'].iteritems())
		print sorted(self.stats['bonus'].iteritems())
		print sorted(self.stats['penalty'].iteritems())
		
	def gainTP(self, gainedtp):
		storedtp = 0;
		self.stats['tp'].totaltp += 1;
		if (gainedtp > (nexttp - tp)):
			storedtp = gainedtp - (nexttp - tp)
			gainedtp -= storedtp
		self.stats['tp'].tp += gainedtp
		if (self.stats['tp'].totaltp >= 500):
			self.stats['tp'].mult = 1.005
		elif (self.stats['tp'].totaltp >= 250):
			self.stats['tp'].mult = 1.015
		elif (self.stats['tp'].totaltp >= 100):
			self.stats['tp'].mult = 1.025
		nexttp *= mult
		self.stats['tp'].tp += storedtp
		
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
	
	def damage(self, num):
		self.stats['curr']['curHP'] -= num
		print "%d dealt! %d HP left." %(num, self.stats['curr']['curHP'])
	
	def attack(self, target):
		print "%s attacked %s!" %(self.name, target.name)
		currentDamage = (self.stats['base']['atk'] + self.stats['bonus']['bonusatk'] - self.stats['penalty']['penaltyatk']) * self.equipment['instrument'].stats['base']['atkmult']
		for x in range(0, self.equipment['instrument'].stats['base']['hits']):
			print "Hit %d:" %(x+1)
			if self.equipment['instrument'].stats['base']['critchance'] > random.randint(0, 100):
				print "Critical!"
				target.damage(currentDamage*self.equipment['instrument'].stats['base']['critmult'])
			else:
				target.damage(currentDamage)
			currentDamage *= self.equipment['instrument'].stats['base']['proration']
	
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