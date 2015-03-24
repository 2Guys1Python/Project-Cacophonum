import pygame, sys, copy
from entityclasses import *
from compositeclasses import *
from battle import *
from model import *

players = [Conductor("MC1")]
wildmon = [copy.deepcopy(modelWildMonsterList['Swamp Thing']), copy.deepcopy(modelWildMonsterList['Wolf'])]


players[0].addMonster(copy.deepcopy(modelTamedMonsterList['Kobold'])) 
players[0].monsters[0].setMaster(players[0]) 
players[0].monsters[0].addSpell(copy.deepcopy(modelSpellList['Black Aria']))
players[0].addItem(copy.deepcopy(modelItemList['Potion']))
players[0].addItem(copy.deepcopy(modelInstrumentList['Flute']))
#players[0].monsters[0].printstats()
#print "%s's conductor is %s" %(players[0].monsters[0].name, players[0].monsters[0].master.name)
#print players[0].getItem(0).name
#print "%s's effects are: %s" %(players[0].getItem(0).name, str(players[0].getItem(0).effectsList))
#print players[0].getItem(0).__class__.__name__
#print "Equipping %s" %(players[0].getItem(1).name)
players[0].monsters[0].setInstrument(players[0].removeItem(1))
#players[0].monsters[0].printstats()
#print players[0].monsters[0].equipment['instrument'].name
b = BattleInstance(players, players[0].monsters, wildmon)
b.nameDiff()
b.loop()
