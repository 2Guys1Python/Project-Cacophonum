import pygame, sys, copy, random, operator
from entityclasses import *
from compositeclasses import *
#from statushandler import *

def useSpell(spell, source, target):
	for func in spell.effectsList:
		funcdict[func[0]](func[1], source, target)

def useSpellAoE(spell, source, target):
	for x in range(0, len(target)):
		for func in spell.effectsList:
			funcdict[func[0]](func[1], source, target[x])

def statusTick(status):
	for e in status.effects:
		funcdict[e[0]](e[1], status.source, status.target)
			
def getStat(str, s, t):
	if str == 'maxHP':
		return s['base']['maxHP'] + s['bonus']['bonusHP'] - s['penalty']['penaltyHP']
	elif str == 'curHP':
		return s['curr']['curHP']
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
	elif str == 'emaxHP':
		return t['base']['maxHP'] + t['bonus']['bonusHP'] - t['penalty']['penaltyHP']
	elif str == 'ecurHP':
		return t['curr']['curHP']
	elif str == 'eatk':
		return t['base']['atk'] + t['bonus']['bonusatk'] - t['penalty']['penaltyatk']
	elif str == 'edef':
		return t['base']['def'] + t['bonus']['bonusdef'] - t['penalty']['penaltydef']
	elif str == 'emus':
		return t['base']['mus'] + t['bonus']['bonusmus'] - t['penalty']['penaltymus']
	elif str == 'efoc':
		return t['base']['foc'] + t['bonus']['bonusfoc'] - t['penalty']['penaltyfoc']
	elif str == 'ecla':
		return t['base']['cla'] + t['bonus']['bonuscla'] - t['penalty']['penaltycla']
	elif str == 'erhy':
		return t['base']['rhy'] + t['bonus']['bonusrhy'] - t['penalty']['penaltyrhy']
		
def compareStat(str, comparate, source, targetgroup):
	bool = False
	if str.startswith("self"):
		if "cur" in str:
			mode = "curr"
		elif "bonus" in str:
			mode = "bonus"
		elif "penalty" in str:
			mode = "penalty"
		else:
			mode = "base"
		bool = ops[str[len(str)-1]](source.stats[mode][str[4:len(str)-1]], comparate)
		return bool, targetgroup
		
	elif str.startswith("ally") or str.startswith("enemy"):						#ally or enemy
		if "cur" in str:
			mode = "curr"
		elif "bonus" in str:
			mode = "bonus"
		elif "penalty" in str:
			mode = "penalty"
		else:
			mode = "base"
		
		num = random.randint(0, len(targetgroup)-1)
		
		for c in range(0, len(targetgroup)):
			target = targetgroup[num]
			bool = ops[str[len(str)-1]](targetgroup[c].stats[mode][str[str.find('y')+1:len(str)-1]], comparate)
			num += 1
			if num > (len(targetgroup)-1):
				num = 0
			if bool:
				return bool, target
		return bool, target

def findExtreme(str, targetgroup):
	if "cur" in str:
		mode = "curr"
	elif "bonus" in str:
		mode = "bonus"
	elif "penalty" in str:
		mode = "penalty"
	else:
		mode = "base"
		
	print str
			
	ex = targetgroup[0].stats[mode][str[str.find('t')+1:len(str)]]
	mon = targetgroup[0]
	
	for t in targetgroup:
		if str.startswith("highest"):
			if t.stats[mode][str[str.find('t')+1:len(str)]] > ex:
				ex = t.stats[mode][str[str.find('t')+1:len(str)]]
				mon = t
		elif str.startswith("lowest"):
			if t.stats[mode][str[str.find('t')+1:len(str)]] < ex:
				ex = t.stats[mode][str[str.find('t')+1:len(str)]]
				mon = t
	
	return mon
		
# args: [hits, scaling stat, scalar]
def dmg_HP(args, source, target):
	scalingstat = getStat(args[1], source.stats, target.stats)
	for x in range(0, args[0]):
		print "Hit %d" %(x+1)
		target.damage(scalingstat*args[2])

# args: [scaling stat, scalar]		
def rec_HP(args, source, target):
	scalingstat = getStat(args[0], source.stats, target.stats)
	target.heal(scalingstat*args[1])

# args: [status name, base proc chance, base duration]		
def apply_debuff(args, source, target):
	status = copy.deepcopy(Status(args[0], 1))
	status.source = source
	status.target = target
	duration = args[2]
	ratio = getStat('cla', source.stats, target.stats) / getStat('erhy', source.stats, target.stats)
	procchance = args[1] * ratio
	if ratio > 1:
		if ratio >= 2:
			# 1% to add 2 duration at 2x, 10% at 3x
			chance = 9*ratio - 17
			if random.randint(0,100) < chance:
				duration += 2
			else:
				duration += 1
		else:
			duration += 1
	status.duration = duration
	if procchance > random.randint(0,100):
		target.addStatus(status)
	
# args: [bool]
def set_Paralysis(args, source, target):
	target.canMove = (not bool)

# Function dictionary should be at the bottom because Python will think the functions haven't been defined otherwise
funcdict = {
	'dmg_HP': dmg_HP,
	'apply_debuff': apply_debuff,
	'set_Paralysis': set_Paralysis
}

ops = {
	'+' : operator.add,
	'-' : operator.sub,
	'*' : operator.mul,
	'/' : operator.div,
	'%' : operator.mod,
	'^' : operator.xor,
	'>' : operator.gt,
	'<' : operator.lt,
	'=' : operator.eq
}
