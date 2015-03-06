import pygame, sys, copy
from entityclasses import *
from compositeclasses import *
from spellhandler import *

class BattleInstance:
	def __init__(self, composers, tamedmonsters, wildmonsters):
		self.turn = 1
		self.over = False
		self.composers = composers
		self.tamedmonsters = tamedmonsters
		self.wildmonsters = wildmonsters
		for t in tamedmonsters:
			t.stats['curr']['notes'] = 4
		print "initialized"
		
	def loop(self):
		print "Controls: [A]ttack, [S]pell, [I]tem, [W]ait"
		
		while not self.over:
			#tamed monsters go first
			for t in self.tamedmonsters:
				action = raw_input("Input action: ")
				if (action == "a" or action == "A") and t.stats['curr']['notes'] >= 2:
					c = 0
					for w in self.wildmonsters:
						print "%d: %s" %(c, w.name)
						c += 1
					targetnum = input("Input number of desired target: ")
					t.attack(self.wildmonsters[targetnum])
				elif action == "s" or action == "S":
					c = 0
					for s in t.spells:
						print "%d: %s" %(c, s.name)
						c += 1
					spellnum = input("Input number of desired spell: ")
					if t.stats['curr']['notes'] >= t.spells[spellnum].cost:
						if t.spells[spellnum].target == "one":
							c = 0
							for w in self.wildmonsters:
								print "%d: %s" %(c, w.name)
								c += 1
							targetnum = input("Input number of desired target: ")
							t.useSpell(spellnum, self.wildmonsters[targetnum])
						else:
							t.useSpell(spellnum, self.wildmonsters)
					else:
						print "Not enough notes"
				elif (action == "i" or action == "I") and t.stats['curr']['notes'] >= 1:
					c = 0
					for i in t.master.inventory.items:
						print "%d: %s" %(c,i.name)
						c += 1
					itemnum = input("Input number of desired item: ")
					c = 0
					for a in self.tamedmonsters:
						print "%d: %s" %(c, a.name)
						c += 1
					targetnum = input("Input number of desired target: ")
					target = self.tamedmonsters[targetnum]
					t.useItem(itemnum, target)
				
				elif action == "w" or action == "W":
					pass
				
				t.stats['curr']['notes'] += t.stats['curr']['notegain'] + t.stats['bonus']['bonusnotegain'] -t.stats['penalty']['penaltynotegain']
				
			self.over = True