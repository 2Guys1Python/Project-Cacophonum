import pygame, sys, init

class Entity:
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
		self.monsters = []
		self.items = []
		self.conductorskill = None
		self.aptitude = {
			'hp': 5,
			'atk': 5,
			'def': 5,
			'mus': 5,
			'foc': 5,
			'cla': 5,
			'rhy': 5,
			'string': 8,
			'wind': 5,
			'percussion': 2
		}
		
	def setMonster(self, monster):
		self.monsters.append(monster)
		
	def addItem(self, item):
		if len(self.items) < 64:
			self.items.append(item)
		
	'''	
	def useItem(self, itemIndex, target):
		self.items[itemIndex].use(target)
	'''
	
	'''
	def trainMonster(self, monster):
		
	'''