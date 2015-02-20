import pygame, sys, copy
from entityclasses import *
from compositeclasses import *

def useSpell(spell, source, target):
	for func in spell.effectsList:
		funcdict[func[0]](func[1], source, target)

def useSpellAoE(spell, source, target):
	for x in range(0, len(target)):
		for func in spell.effectsList:
			funcdict[func[0]](func[1], source, target[x])


			
def getStat(str, s, t):
	if str == 'maxHP':
		return s['base']['maxHP'] + s['bonus']['bonusHP'] - s['penalty']['penaltyHP']
	elif str == 'atk':
		return s['base']['atk'] + s['bonus']['bonusatk'] - s['penalty']['penaltyatk']
	elif str == 'def':
		return s['base']['def'] + s['bonus']['bonusdef'] - s['penalty']['penaltydef']
	elif str == 'mus':
		return s['base']['mus'] + s['bonus']['bonusmus'] - s['penalty']['penaltymus']
	elif str == 'foc':
		return s['base']['foc'] + s['bonus']['bonusfoc'] - s['penalty']['penaltyfoc']
	elif str == 'cla':
		return s['base']['cla'] + s['bonus']['bonuscla'] - s['penalty']['penaltycla']
	elif str == 'rhy':
		return s['base']['rhy'] + s['bonus']['bonusrhy'] - s['penalty']['penaltyrhy']
		
# args: [hits, scaling stat, scalar]
def dmg_HP(args, source, target):
	scalingstat = getStat(args[1], source.stats, target.stats)
	for x in range(0, args[0]):
		print "Hit %d" %(x+1)
		target.damage(scalingstat*args[2])


# Function dictionary should be at the bottom because Python will think the functions haven't been defined otherwise
funcdict = {
	'dmg_HP': dmg_HP
}
