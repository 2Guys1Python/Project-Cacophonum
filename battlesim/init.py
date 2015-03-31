import pygame, sys
from entityclasses import *
from compositeclasses import *

'''
Tamed Monster masterlist format:
	'Name': [maxHP, atk, def, mus, foc, cla, rhy, <- base (1-9999, combined max 50000?)
			maxHP, atk, def, mus, foc, cla, rhy] <- gain modifiers (1-10) 
'''

masterlist_tm = {
	'Kobold': [4500, 3000, 3000, 3000, 3000, 3000, 3000,
				5,4,3,5,5,5,6]
}

'''
Wild Monster masterlist format:
	'Name': [maxHP, atk, def, mus, foc, cla, rhy,				<- base, no max
			hits, proration,									<- attack stats
			[[command1, target1, condition1, conditionNum1, probability1] , [command2, target2, condition2, conditionNum2, probability2], ...]]
																^ possible AI actions, list by priority
																
	[!] Only generic command strings are attack, offspell, defspell, and debspell. [!]
	[!] All other names straight up call the word as a spell [!]

	
	[!] example AI: [!]
	Suicide to damage enemy party if self HP is <30% (prob 100)
	At turn 3, attack enemy with lowest hp (prob 100)
	Use Healing Howl to heal ally with lowest HP (prob 75)
	Use spell on random enemy, no condition (prob 60)
	Attack someone from enemy party, no condition (prob 100)
	
	[['suicide', 'enemy', 'selfcurHP<', '30', 100],
	['attack', 'enemy', 'turn=', 3, 100],
	['Healing Howl', 'ally', 'lowestcurHP', None, 60],
	['offspell', 'enemy', 'curHP>', 500, 60],
	['attack', 'enemy', None, None, 100]]
	
	again, an AI entry consists of this 5 tuple:
	[ACTION, TARGET, CONDITION, CONDITION COMPARATE (if applicable), PROBABILITY]
'''

masterlist_wm = {
	'Swamp Thing': [4500, 3000, 3000, 3000, 3000, 3000, 3000,
					4, 0.85,
					[['offspell', 'enemy', 'enemycurHP>', 500, 60],
					['attack', 'enemy', None, None, 100]]],
	'Slime': [2500, 1500, 1500, 1500, 1500, 3000, 3000,
					4, 0.85,
					[['offspell', 'enemy', 'enemycurHP>', 500, 60],
					['attack', 'enemy', None, None, 100]]],
	'Wolf': [5500, 3500, 4500, 3500, 3500, 3500, 3500,
					4, 0.85,
					[['offspell', 'enemy', 'enemycurHP>', 500, 60],
					['Healing Howl', 'ally','lowestcurHP' ,None, 95],
					['attack', 'enemy', None, None, 100]]],
	'Husk': [6500, 6000, 4000, 2500, 2500, 2500, 3000,
					4, 0.85,
					[['offspell', 'enemy', 'enemycurHP>', 500, 60],
					['Healing Howl', 'ally','lowestcurHP' ,None, 60],
					['attack', 'enemy', None, None, 100]]],
	'Orthrus': [7000, 7000, 3000, 7000, 7000, 7000, 7000,
					4, 0.85,
					[['offspell', 'enemy', 'enemycurHP>', 500, 60],
					['Healing Howl', 'self','curHP<' ,2500, 60],
					['suicide', 'enemy', 'selfcurHP<', '20', 100],
					['attack', 'enemy', None, None, 100]]]
}

'''
Item price masterlist format:
	'Name': [buy, sell]
'''

masterlist_price = {
	'Potion': [50, 25],
	'Flute': [600, 300]
}

'''
Item effect masterlist format:
	'Name': ['one/aoe/col/row', [['eff1', [arg1]], ['eff2', [arg1, arg2]], ...]]
'''

masterlist_item = {
	'Potion': ['one', [['rec_HP', [100]]]]
}

'''
Instrument masterlist format:
	'Name':[hits, bhp, batk, bdef, bmus, bfoc, bcla, brhy, bng,
				  php, patk, pdef, pmus, pfoc, pcla, prhy, png,
				  type, atk multiplier, crit chance, crit multiplier, proration per hit,
				  {effects}]
'''

masterlist_instrument = {
	'Flute': [8,0,60,0,30,0,0,0,0,
				0,0,0,0,0,0,0,0,
				'wind', 0.2, 15, 2.5, 0.9,
				None]
}

'''
Spell masterlist format:
	'Name': [cost, type, inst, target, [[eff1, [args]], [eff2, [args]], ...]]
	
	[!] type = off/def/buf/deb [!]
'''

masterlist_spell = {
	'Black Aria': [2, 'off', 'wind', 'aoe', 
					[['dmg_HP', [5, 'mus', 0.14]],
					['apply_debuff', ['Poison', 25, 2]]]]
}

'''
Status masterlist format:
	'Name': [type, [[eff1, [args]], [eff2, [args]], ...]]
	
	[!] type = off/def/buf/deb [!]
'''

masterlist_status = {
	'Poison': ['off', [['dmg_HP', [1, 'ecurHP', 0.05]]]],
	'Paralysis': ['off', [['set_Paralysis', [True]]]]
}

def tamedMonster_Init(indexName):
	
	tempdict = {}
	tempdict['base'] = {
			'maxHP': masterlist_tm[indexName][0], 'atk': masterlist_tm[indexName][1], 'def': masterlist_tm[indexName][2],
			'mus': masterlist_tm[indexName][3], 'foc': masterlist_tm[indexName][4], 'cla': masterlist_tm[indexName][5], 'rhy': masterlist_tm[indexName][6],
			'string': 1, 'wind': 1, 'percussion': 1
	}
	tempdict['curr'] = {
			'curHP': masterlist_tm[indexName][0], 'bond': 0,
			'notegain': 2, 'notes': 4
	}
	tempdict['bonus'] = {
			'bonusHP': 0, 'bonusatk': 0, 'bonusdef': 0,
			'bonusmus': 0, 'bonusfoc': 0, 'bonuscla': 0, 'bonusrhy': 0,
			'bonusnotegain': 0
	}
	tempdict['penalty'] = {
			'penaltyHP': 0,'penaltyatk': 0,'penaltydef': 0,
			'penaltymus': 0,'penaltyfoc': 0,'penaltycla': 0,'penaltyrhy': 0,
			'penaltynotegain': 0
	}
	tempdict['gains'] = {
			'maxHP': masterlist_tm[indexName][7],'atk': masterlist_tm[indexName][8],'def': masterlist_tm[indexName][9],
			'mus': masterlist_tm[indexName][10],'foc': masterlist_tm[indexName][11],'cla': masterlist_tm[indexName][12],'rhy': masterlist_tm[indexName][13]
	}
	tempdict['tp'] = {
			'tp': 0,'totaltp': 0,'tpprog': 0, 'nexttp': 100
	}
	
	return tempdict

def wildMonster_Init(indexName):
	tempdict = {}
	
	tempdict['base'] = {
			'maxHP': masterlist_wm[indexName][0], 'atk': masterlist_wm[indexName][1], 'def': masterlist_wm[indexName][2],
			'mus': masterlist_wm[indexName][3], 'foc': masterlist_wm[indexName][4], 'cla': masterlist_wm[indexName][5], 'rhy': masterlist_wm[indexName][6],
	}
	tempdict['curr'] = {
			'curHP': masterlist_wm[indexName][0], 'hits': masterlist_wm[indexName][7], 'proration': masterlist_wm[indexName][8]
	}
	tempdict['bonus'] = {
			'bonusHP': 0, 'bonusatk': 0, 'bonusdef': 0,
			'bonusmus': 0, 'bonusfoc': 0, 'bonuscla': 0, 'bonusrhy': 0
	}
	tempdict['penalty'] = {
			'penaltyHP': 0,'penaltyatk': 0,'penaltydef': 0,
			'penaltymus': 0,'penaltyfoc': 0,'penaltycla': 0,'penaltyrhy': 0
	}

	return masterlist_wm[indexName][9], tempdict

def itemPrice_Init(indexName):
	
	tempdict = {}
	tempdict['buy'] = masterlist_price[indexName][0]
	tempdict['sell'] = masterlist_price[indexName][1]
	return tempdict
	
def consumableEffect_Init(indexName):
	return masterlist_item[indexName][0], masterlist_item[indexName][1]
	
def instrument_Init(indexName):
	tempdict = {}
	tempdict['base'] = {
			'hits': masterlist_instrument[indexName][0], 'type': masterlist_instrument[indexName][17],
			'atkmult': masterlist_instrument[indexName][18],'critchance': masterlist_instrument[indexName][19], 'critmult': masterlist_instrument[indexName][20],
			'proration': masterlist_instrument[indexName][21],'effects': masterlist_instrument[indexName][22]
	}
	tempdict['bonus'] = {
			'bonusHP': masterlist_instrument[indexName][1], 'bonusatk': masterlist_instrument[indexName][2], 'bonusdef': masterlist_instrument[indexName][3],
			'bonusmus': masterlist_instrument[indexName][4], 'bonusfoc': masterlist_instrument[indexName][5], 'bonuscla': masterlist_instrument[indexName][6], 'bonusrhy': masterlist_instrument[indexName][7],
			'bonusnotegain': masterlist_instrument[indexName][8]
	}
	tempdict['penalty'] = {
			'penaltyHP': masterlist_instrument[indexName][9],'penaltyatk': masterlist_instrument[indexName][10],'penaltydef': masterlist_instrument[indexName][11],
			'penaltymus': masterlist_instrument[indexName][12],'penaltyfoc': masterlist_instrument[indexName][13],'penaltycla': masterlist_instrument[indexName][14],'penaltyrhy': masterlist_instrument[indexName][15],
			'penaltynotegain': masterlist_instrument[indexName][16]
	}
	return tempdict
	
def spell_Init(indexName):
	return masterlist_spell[indexName][0], masterlist_spell[indexName][1], masterlist_spell[indexName][2], masterlist_spell[indexName][3], masterlist_spell[indexName][4]
	
def status_Init(indexName):
	return masterlist_status[indexName][0], masterlist_status[indexName][1]