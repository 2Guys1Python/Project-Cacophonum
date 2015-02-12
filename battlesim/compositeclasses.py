import pygame, sys, init

class Item:
	def __init__(self, name, index, isKeyItem):
		self.name = name
		self.index = index
		self.isKeyItem = isKeyItem