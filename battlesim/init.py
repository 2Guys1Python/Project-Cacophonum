import pygame, sys
from entityclasses import *
from compositeclasses import *

'''
Tamed Monster masterlist format:
	'Name': [maxHP, atk, def, mus, foc, cla, rhy <- base (1-9999, combined max 50000?)
			maxHP, atk, def, mus, foc, cla, rhy] <- gain modifiers (1-10) 
'''

masterlist_tm = {
	'Kobold': [4500, 3000, 3000, 3000, 3000, 3000, 3000,
				5,4,3,5,5,5,6]
}

'''
Wild Monster masterlist format:
	'Name': [maxHP, atk, def, mus, foc, cla, rhy] <- base, no max
'''

masterlist_wm = {
	'Swamp Thing': [4500, 3000, 3000, 3000, 3000, 3000, 3000]
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
	'Name':{
		'effect_name': <whatever>
	}
'''

masterlist_item = {
	'Potion': {
		'rec_HP': 100
	}
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
			'tp': 0,'totaltp': 0,'nexttp': 100,
			'mult': 1.035
	}
	
	return tempdict

def wildMonster_Init(indexName):
	tempdict = {}
	
	tempdict['base'] = {
			'maxHP': masterlist_wm[indexName][0], 'atk': masterlist_wm[indexName][1], 'def': masterlist_wm[indexName][2],
			'mus': masterlist_wm[indexName][3], 'foc': masterlist_wm[indexName][4], 'cla': masterlist_wm[indexName][5], 'rhy': masterlist_wm[indexName][6],
	}
	tempdict['curr'] = {
			'curHP': masterlist_wm[indexName][0]
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

	return tempdict

def itemPrice_Init(indexName):
	
	tempdict = {}
	tempdict['buy'] = masterlist_price[indexName][0]
	tempdict['sell'] = masterlist_price[indexName][1]
	return tempdict
	
def consumableEffect_Init(indexName):
	return masterlist_item[indexName]
	
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