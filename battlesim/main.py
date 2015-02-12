import pygame, sys, copy
from entityclasses import *
	

players = [Conductor("MC1")]
modelTamedMonsterList = {
	'Swamp Thing': TamedMonster("Swamp Thing", 1)
}
modelWildMonsterList = {
	'Little Bitch': WildMonster("Little Bitch", 1)
}

players[0].addMonster(copy.deepcopy(modelTamedMonsterList['Swamp Thing']))
players[0].monsters[0].setMaster(players[0])
players[0].monsters[0].printstats()
print players[0].monsters[0].name
print players[0].monsters[0].master.name