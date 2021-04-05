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
	dim=4
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
	targetPos=(random.randrange(0,dim),random.randrange(0,dim))
	map[targetPos[0]][targetPos[1]].target=True
	map[targetPos[0]][targetPos[1]].terrain="-"
	return map,targetPos

def printMap(map):
	print("\n".join([" ".join([str(item) for item in row]) for row in map]))

def updateBelief(map, belief, observedPos):
	dim=len(map)
	terrainProbs=[0.1, 0.3, 0.7, 0.9]

	sum=0

	for row in range(0,dim):
		for col in range(0,dim):
			sum=sum+belief[row][col]
	print(sum)

	if map[observedPos[0]][observedPos[1]].terrain=='F':
			pTerrain=terrainProbs[0]
	elif map[observedPos[0]][observedPos[1]].terrain=='H':
			pTerrain=terrainProbs[1]
	elif map[observedPos[0]][observedPos[1]].terrain=='T':
			pTerrain=terrainProbs[2]
	else:
			pTerrain=terrainProbs[3]

	observedBel=belief[observedPos[0]][observedPos[1]]

	for row in range(0,dim):
		for col in range(0,dim):
			#Update unobserved spaces
				pFail=(((dim**2)-1)/(dim**2)+pTerrain*(1/dim**2))
				belief[row][col]=belief[row][col]/pFail
	
	#Update observed spaces
	belief[observedPos[0]][observedPos[1]]=observedBel*pTerrain


	return belief

def basicAgent1(map):
	dim=len(map)
	#t=increments by 1 each turn
	#Initial Beliefs at t=0

	beliefMap=[[1/dim**2 for i in range(dim)] for j in range(dim)]

	found=False
	while not found:
		observedPos=(random.randrange(0,dim),random.randrange(0,dim))
		if map[observedPos[0]][observedPos[1]].target:
			found=True
		else:
			beliefMap=updateBelief(map,beliefMap,observedPos)
		print(np.array(beliefMap))
		print("\n")
		
	printMap(map)


if __name__ == "__main__":
	main()
	map,targetPos=generateMap()
	printMap(map)
	basicAgent1(map)


