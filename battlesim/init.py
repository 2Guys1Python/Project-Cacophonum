import pygame, sys
from entityclasses import *
from compositeclasses import *

def tamedMonster_Init(indexName):
	'''
	masterlist format:
	'Name': [maxHP, atk, def, mus, foc, cla, rhy <- base (1-9999, combined max 50000?)
			maxHP, atk, def, mus, foc, cla, rhy] <- gain modifiers (1-10) 
	'''
	masterlist = {
		'Kobold': [4500, 3000, 3000, 3000, 3000, 3000, 3000,
					5,4,3,5,5,5,6]
	}
	
	tempdict = {}
	tempdict['base'] = {
			'maxHP': masterlist[indexName][0], 'atk': masterlist[indexName][1], 'def': masterlist[indexName][2],
			'mus': masterlist[indexName][3], 'foc': masterlist[indexName][4], 'cla': masterlist[indexName][5], 'rhy': masterlist[indexName][6],
			'string': 1, 'wind': 1, 'percussion': 1
	}
	tempdict['curr'] = {
			'curHP': masterlist[indexName][0], 'bond': 0,
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
			'maxHP': masterlist[indexName][7],'atk': masterlist[indexName][8],'def': masterlist[indexName][9],
			'mus': masterlist[indexName][10],'foc': masterlist[indexName][11],'cla': masterlist[indexName][12],'rhy': masterlist[indexName][13]
	}
	tempdict['tp'] = {
			'tp': 0,'totaltp': 0,'nexttp': 100,
			'mult': 1.035
	}
	
	return tempdict

def wildMonster_Init(indexName):
	tempdict = {}
	masterlist = {
		'Swamp Thing': [4500, 3000, 3000, 3000, 3000, 3000, 3000]
	}
	tempdict['base'] = {
			'maxHP': masterlist[indexName][0], 'atk': masterlist[indexName][1], 'def': masterlist[indexName][2],
			'mus': masterlist[indexName][3], 'foc': masterlist[indexName][4], 'cla': masterlist[indexName][5], 'rhy': masterlist[indexName][6],
	}
	tempdict['curr'] = {
			'curHP': masterlist[indexName][0]
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

