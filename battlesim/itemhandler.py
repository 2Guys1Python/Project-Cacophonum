import pygame, sys, copy
from entityclasses import *
from compositeclasses import *

def useItem(item, target):
	for func in item.effectsList:
		funcdict[func[0]](func[1], target)

def useItemAoE(item, target):
	for ent in target:
		for func in item.effectsList:
			funcdict[func[0]](args, target[ent])
	
def rec_HP(args, target):
	target.heal(args[0])

	
# Function dictionary should be at the bottom because Python will think the functions haven't been defined otherwise
funcdict = {
	'rec_HP': rec_HP
}
