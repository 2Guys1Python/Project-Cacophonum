import pygame, sys

class Entity:
	def __init__(self, name, index):
		tempdict = {}
		tempdict['base'] = {
			'maxHP': 4500,
			'curHP': 4500,
			'atk': 3000,
			'def': 3000,
			'mus': 3000,
			'foc': 3000,
			'cla': 3000,
			'rhy': 3000,
			'notegain': 2,
			'maxnotes': 10,
			'notes': 4
		}
		tempdict['bonus'] = {
			'bonusHP': 0,
			'bonusatk': 0,
			'bonusdef': 0,
			'bonusmus': 0,
			'bonusfoc': 0,
			'bonuscla': 0,
			'bonusrhy': 0,
			'bonusnotegain': 0
		}
		tempdict['penalty'] = {
			'penaltyHP': 0,
			'penaltyatk': 0,
			'penaltydef': 0,
			'penaltymus': 0,
			'penaltyfoc': 0,
			'penaltycla': 0,
			'penaltyrhy': 0,
			'penaltynotegain': 0
		}
		tempdict['gains'] = {
			'maxHP': 5,
			'atk': 4,
			'def': 3,
			'mus': 5,
			'foc': 5,
			'cla': 5,
			'rhy': 6
		}
		tempdict['tp'] = {
			'tp': 0,
			'totaltp': 0,
			'nexttp': 100,
			'mult': 1.035
		}
		tempdict['equipment'] = {
			'instrument': None,
			'accessory1': None,
			'accessory2': None,
		}
		tempdict['skills'] = {}
		tempdict['status'] = {}
		self.name = name
		self.index = index
		self.master = None
		self.stats = tempdict
	
	def printstats(self):
		print "Name: %s" % (self.name)
		print "Index: %s" % (self.index)
		print self.stats['base'].keys()
		print self.stats['base'].values()
		print self.stats['bonus'].keys()
		print self.stats['bonus'].values()
		print self.stats['penalty'].keys()
		print self.stats['penalty'].values()
		
	def gainTP(self, gainedtp):
		storedtp = 0;
		self.stats['tp'].totaltp += 1;
		if (gainedtp > (nexttp - tp)):
			storedtp = gainedtp - (nexttp - tp)
			gainedtp -= storedtp
		self.stats['tp'].tp += gainedtp
		if (self.stats['tp'].totaltp >= 500):
			self.stats['tp'].mult = 1.005
		elif (self.stats['tp'].totaltp >= 250):
			self.stats['tp'].mult = 1.015
		elif (self.stats['tp'].totaltp >= 100):
			self.stats['tp'].mult = 1.025
		nexttp *= mult
		self.stats['tp'].tp += storedtp
		
	def setMaster(self, newmaster):
		self.master = newmaster
		
	
	
class Conductor:
	def __init__(self, name):
		self.name = name
		self.monsters = []
		
	def setMonster(self, monster):
		self.monsters.append(monster)