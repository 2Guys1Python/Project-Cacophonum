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
		
	def loop(self):
		print "Controls: [A]ttack, [S]pell, [I]tem"
		while not self.over:
			#tamed monsters go first
			for t in self.tamedmonsters:
				action = raw_input("Input action: ")
				if action == "a" or action == "A":
					c = 0
					for w in self.wildmonsters:
						print "%d: %s" %(c, w.name)
					targetnum = input("Input number of desired target: ")
					t.attack(self.wildmonsters[targetnum])
				elif action == "s" or action == "S":
					c = 0
					for s in t.spells:
						print "%d: %s" %(c, s.name)
					spellnum = input("Input number of desired spell: ")
					if t.spells[spellnum].target == "one":
						c = 0
						for w in self.wildmonsters:
							print "%d: %s" %(c, w.name)
						targetnum = input("Input number of desired target: ")
						t.useSpell(spellnum, self.wildmonsters[targetnum])
					else:
						t.useSpell(spellnum, self.wildmonsters)
						
				self.over = True