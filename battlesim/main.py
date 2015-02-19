import pygame, sys, copy
from entityclasses import *
from compositeclasses import *
	

modelTamedMonsterList = {
	'Kobold': TamedMonster("Kobold", 1)
}
modelWildMonsterList = {
	'Swamp Thing': WildMonster("Swamp Thing", 1)
}

modelItemList = {
	'Potion': Consumable("Potion", 1)
}

modelInstrumentList = {
	'Flute': Instrument("Flute", 1)
}
'''
modelSkillList = {
	'Black Aria': Skill("Black Aria", 1)
}

modelStatusList = {
	'Poison': Status("Poison", 1)
}
'''	
	
players = [Conductor("MC1")]
wildmon = [copy.deepcopy(modelWildMonsterList['Swamp Thing'])]


players[0].addMonster(copy.deepcopy(modelTamedMonsterList['Kobold'])) 
players[0].monsters[0].setMaster(players[0]) 
players[0].addItem(copy.deepcopy(modelItemList['Potion']))
players[0].addItem(copy.deepcopy(modelInstrumentList['Flute']))
players[0].monsters[0].printstats()
print "%s's conductor is %s" %(players[0].monsters[0].name, players[0].monsters[0].master.name)
print players[0].getItem(0).name
print "%s's effects are: %s" %(players[0].getItem(0).name, str(players[0].getItem(0).itemEffect))
print players[0].getItem(0).__class__.__name__
print "Equipping %s" %(players[0].getItem(1).name)
players[0].monsters[0].setInstrument(players[0].removeItem(1))
players[0].monsters[0].printstats()
print players[0].monsters[0].equipment['instrument'].name
players[0].monsters[0].attack(wildmon[0])