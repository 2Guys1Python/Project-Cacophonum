import pygame, sys
from entityclasses import *
	

x = Entity("Swamp Thing", 1)
y = Conductor("MC1")
y.setMonster(x)
x.setMaster(y)
x.printstats()
print y.monsters[0].name
print x.master.name