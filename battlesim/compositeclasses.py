import pygame, sys, init

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
		
class Equipment(Item):
	def __init__(self, name, index):
		super(Equipment, self).__init__(name, index)
		self.itemType = "Equipment"
	
class Consumable(Item):
	def __init__(self, name, index):
		super(Consumable, self).__init__(name, index)
		self.itemEffect = init.consumableEffect_Init(name)
		self.itemType = "Consumable"