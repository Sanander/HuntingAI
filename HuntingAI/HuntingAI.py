import random
import numpy as np

def main():
	print("Hello")
	generateMap()

#Flat='F'
#Hilly='H'
#Forrest='T'
#Caves='C'
class Space():
	def __init__(self, terrain, target=False):
		self.terrain=terrain
		self.target=target
	def __str__(self):
		return self.terrain

def generateMap():
	dim=50
	map=[[Space("X") for i in range(dim)] for j in range(dim)]
	for row in map:
		for item in row:
			rand=random.randrange(1,5)
			if(rand==1):
				ter="F"
			elif(rand==2):
				ter="H"
			elif(rand==3):
				ter="T"
			elif(rand==4):
				ter="C"
			item.terrain=ter
	targetPos=(random.randrange(0,49),random.randrange(0,49))
	map[targetPos[0]][targetPos[1]].terrain="4"
	return map,targetPos

def printMap(map):
	print("\n".join([" ".join([str(item) for item in row]) for row in map]))

if __name__ == "__main__":
	main()
	map,targetPos=generateMap()
	printMap(map)


