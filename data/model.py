import pygame, sys, copy
from entityclasses import *
from compositeclasses import *
	

modelTamedMonsterList = {
	'Kobold': TamedMonster("Kobold", 1)
}
modelWildMonsterList = {
	'Swamp Thing': WildMonster("Swamp Thing", 1),
	'Slime': WildMonster("Slime", 1),
	'Wolf': WildMonster("Wolf", 1),
	'Husk': WildMonster("Husk", 1),
	'Orthrus': WildMonster("Orthrus", 1)
}

modelItemList = {
	'Potion': Consumable("Potion", 1)
}

modelInstrumentList = {
	'Flute': Instrument("Flute", 1)
}

modelSpellList = {
	'Black Aria': Spell("Black Aria", 1)
}

modelStatusList = {
	'Poison': Status("Poison", 1)
}