import pygame, sys, copy
from entityclasses import *
from compositeclasses import *
	

players = [Conductor("MC1")]
inventory = []
modelTamedMonsterList = {
	'Kobold': TamedMonster("Kobold", 1)
}
modelWildMonsterList = {
	'Swamp Thing': WildMonster("Swamp Thing", 1)
}

modelItemList = {
	'Potion': Consumable("Potion", 1)
}
'''
modelEquipmentList = {
	'Flute': Equipment(<tbd>)
}

modelSkillList = {
	'Black Aria': Skill(<tbd>)
}

modelStatusList = {
	'Poison': Status(<tbd>)
}
'''

players[0].addMonster(copy.deepcopy(modelTamedMonsterList['Kobold'])) #assigns a TamedMonster to a Conductor
players[0].monsters[0].setMaster(players[0]) #assigns the Conductor to the TamedMonster
players[0].monsters[0].printstats() #prints all stats of a given TamedMonster (NOT IN ORDER)
players[0].addItem(copy.deepcopy(modelItemList['Potion']))
print players[0].monsters[0].name #testing monster list reference in Conductor
print players[0].monsters[0].master.name #testing master reference in TamedMonster
print players[0].items[0].name
print players[0].items[0].itemEffect
print players[0].items[0].__class__.__name__