import pygame, sys, init

class WildMonster:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.stats = init.wildMonster_Init(name)
		self.itemDrops = []
		self.skills = []
		self.status = []
		self.AI = None
		
	

class TamedMonster:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.master = None
		self.stats = init.tamedMonster_Init(name)
		self.equipment = {
			'instrument': None,
			'accessory1': None,
			'accessory2': None,
		}
		self.skills = []
		self.status = []
	
	def printstats(self):
		print "Name: %s" % (self.name)
		print "Index: %s" % (self.index)
		print self.stats['base'].keys()
		print self.stats['base'].values()
		print self.stats['curr'].keys()
		print self.stats['curr'].values()
		print self.stats['bonus'].keys()
		print self.stats['bonus'].values()
		print self.stats['penalty'].keys()
		print self.stats['penalty'].values()
		
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
		
	
	
class Conductor:
	def __init__(self, name):
		self.name = name
		self.monsterLimit = 1
		self.monsters = []
		self.items = []
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
		if len(self.items) < 64:
			self.items.append(item)
			return True
		else:
			return False
	
	
	
	'''	
	def useItem(self, itemIndex, target):
		self.items[itemIndex].use(target)
	'''
	
	'''
	def trainMonster(self, monster):
		
	'''