import pygame, sys, init

class Spell:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.cost, self.type, self.inst, self.target, self.effectsList = init.spell_Init(name)

class Status:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.type, self.effects = init.status_Init(name)
		
#Item related stuff
class KeyItem(object):
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.itemType = "Key Item"
		'''
		self.description = init.itemDescription_Init(name)
		'''
		
class Item(KeyItem):
	def __init__(self, name, index):
		super(Item, self).__init__(name, index)
		self.itemType = "Loot"
		self.prices = init.itemPrice_Init(name)
		
class Instrument(Item):
	def __init__(self, name, index):
		super(Instrument, self).__init__(name, index)
		self.itemType = "Instrument"
		self.stats = init.instrument_Init(name)
	
class Consumable(Item):
	def __init__(self, name, index):
		super(Consumable, self).__init__(name, index)
		self.target, self.effectsList = init.consumableEffect_Init(name)
		self.itemType = "Consumable"

	
class Inventory(object):
	def __init__(self):
		self.items = []
	
	def getSize(self):
		return len(self.items)
	
	def addItem(self, item):
		self.items.append(item)
		
	def getItem(self, index):
		return self.items[index]
	
	def removeItem(self, index):
		return self.items.pop(index)
		
