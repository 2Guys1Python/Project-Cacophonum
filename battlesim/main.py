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

players[0].addMonster(copy.deepcopy(modelTamedMonsterList['Kobold'])) 
players[0].monsters[0].setMaster(players[0]) 
players[0].addItem(copy.deepcopy(modelItemList['Potion']))
players[0].monsters[0].printstats() 
print "%s's conductor is %s" %(players[0].monsters[0].name, players[0].monsters[0].master.name)
print players[0].items[0].name
print "%s's effects are: %s" %(players[0].items[0].name, str(players[0].items[0].itemEffect))
print players[0].items[0].__class__.__name__