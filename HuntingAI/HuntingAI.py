import random
import numpy as np

def main():
	dim=4
	map,targetPos=generateMap(dim)
	printMap(map)
	basicAgent1(map)

#Flat='F', Hilly='H', Forrest='T', Caves='C'
class Space():
	def __init__(self, terrain, target=False):
		self.terrain=terrain
		self.target=target
	def __str__(self):
		return self.terrain

def generateMap(dim):
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
	return map,targetPos

def printMap(map):
	print("\n".join([" ".join([str(item) for item in row]) for row in map]))

def updateBelief(map, belief, observedPos):
	dim=len(map)
	terrainProbs=[0.1, 0.3, 0.7, 0.9]

	#sum=0

	#for row in range(0,dim):
	#	for col in range(0,dim):
	#		sum=sum+belief[row][col]
	#print(sum)

	#print(str(observedPos[0])+" "+str(observedPos[1]))

	if map[observedPos[0]][observedPos[1]].terrain=='F':
			pTerrain=terrainProbs[0]
	elif map[observedPos[0]][observedPos[1]].terrain=='H':
			pTerrain=terrainProbs[1]
	elif map[observedPos[0]][observedPos[1]].terrain=='T':
			pTerrain=terrainProbs[2]
	else:
			pTerrain=terrainProbs[3]

	observedBel=belief[observedPos[0]][observedPos[1]]
	pFail=(((dim**2)-1)/(dim**2)+pTerrain*(1/dim**2))

	for row in range(0,dim):
		for col in range(0,dim):
			#Update unobserved spaces
				belief[row][col]=belief[row][col]/pFail
	
	#Update observed spaces
	belief[observedPos[0]][observedPos[1]]=observedBel*(1-pTerrain)


	return belief

def getBestSpace1(map,belief,currentPos):
	max=belief[currentPos[0]][currentPos[1]]
	moveToPos=currentPos
	spaces=[currentPos]
	dim=len(map)
	for row in range(0,dim):
		for col in range(0,dim):
			#Target space has highest belief. Reset list of spaces
			if belief[row][col]>max:
				moveToPos=(row,col)
				max=belief[row][col]
				spaces=[(row,col)]
			#Same belief, pick closest by Manhattan distance. Store both if equally far
			elif belief[row][col]==max:
				dist1=abs(currentPos[0]-moveToPos[0])+abs(currentPos[1]-moveToPos[1])
				dist2=abs(currentPos[0]-row)+abs(currentPos[1]-col)
				if dist2<dist1:
					moveToPos=(row,col)
					spaces=[(row,col)]
				elif dist1==dist2:
					spaces.append((row,col))
	#Pick random of equidistant points
	moveToPos=spaces[random.randrange(0,len(spaces))]
	dist=abs(currentPos[0]-moveToPos[0])+abs(currentPos[1]-moveToPos[1])
	return moveToPos,dist

def basicAgent1(map):
	dim=len(map)

	#Initial Beliefs at t=0
	beliefMap=[[1/dim**2 for i in range(dim)] for j in range(dim)]

	found=False
	currentPos=(random.randrange(0,dim),random.randrange(0,dim))

	turns=0
	terrainProbs=[0.1, 0.3, 0.7, 0.9]


	while not found:
		print(np.array(beliefMap))
		#Find position with highest belief and its distance from current position
		moveToPos,dist=getBestSpace1(map,beliefMap,currentPos)

		#Add number of moves required to get to desired space and move to desired space
		turns=turns+dist
		print("MOVE FROM "+str(currentPos)+"TO "+str(moveToPos)+" IN "+str(dist)+ " MOVES AND SEARCH\n")
		currentPos=moveToPos

		#Perform a search at space, add 1 to turns
		turns=turns+1

		if map[currentPos[0]][currentPos[1]].target:
			#Get terrain probability of searched space
			if map[currentPos[0]][currentPos[1]].terrain=='F':
					pTerrain=terrainProbs[0]
			elif map[currentPos[0]][currentPos[1]].terrain=='H':
					pTerrain=terrainProbs[1]
			elif map[currentPos[0]][currentPos[1]].terrain=='T':
					pTerrain=terrainProbs[2]
			else:
				pTerrain=terrainProbs[3]

			#Find if no false negative
			if(random.random()<=pTerrain):
				found=True
			else:
				#If target not found update beliefs
				beliefMap=updateBelief(map,beliefMap,currentPos)
		else:
			#If target not found update beliefs
			beliefMap=updateBelief(map,beliefMap,currentPos)
		
	printMap(map)
	print(turns)
	return turns

def getBestSpace2(map,belief,currentPos):
	terrainProbs=[0.1, 0.3, 0.7, 0.9]

	if map[currentPos[0]][currentPos[1]].terrain=='F':
			pTerrain=terrainProbs[0]
	elif map[currentPos[0]][currentPos[1]].terrain=='H':
			pTerrain=terrainProbs[1]
	elif map[currentPos[0]][currentPos[1]].terrain=='T':
			pTerrain=terrainProbs[2]
	else:
			pTerrain=terrainProbs[3]
	
	max=belief[currentPos[0]][currentPos[1]]*pTerrain
	moveToPos=currentPos
	spaces=[currentPos]
	dim=len(map)

	for row in range(0,dim):
		for col in range(0,dim):

			if map[row][col].terrain=='F':
				pTerrain=terrainProbs[0]
			elif map[row][col].terrain=='H':
				pTerrain=terrainProbs[1]
			elif map[row][col].terrain=='T':
				pTerrain=terrainProbs[2]
			else:
				pTerrain=terrainProbs[3]

			#Target space has highest probability of finding. Reset list of spaces
			if belief[row][col]*pTerrain>max:
				moveToPos=(row,col)
				max=belief[row][col]*pTerrain
				spaces=[(row,col)]
			#Same belief, pick closest by Manhattan distance. Store both if equally far
			elif belief[row][col]*pTerrain==max:
				dist1=abs(currentPos[0]-moveToPos[0])+abs(currentPos[1]-moveToPos[1])
				dist2=abs(currentPos[0]-row)+abs(currentPos[1]-col)
				if dist2<dist1:
					moveToPos=(row,col)
					spaces=[(row,col)]
				elif dist1==dist2:
					spaces.append((row,col))
	#Pick random of equidistant points
	moveToPos=spaces[random.randrange(0,len(spaces))]
	dist=abs(currentPos[0]-moveToPos[0])+abs(currentPos[1]-moveToPos[1])
	return moveToPos,dist

def basicAgent2(map):
	dim=len(map)

	#Initial Beliefs at t=0
	beliefMap=[[1/dim**2 for i in range(dim)] for j in range(dim)]

	found=False
	currentPos=(random.randrange(0,dim),random.randrange(0,dim))

	turns=0

	while not found:
		print(np.array(beliefMap))
		#Find position with highest belief and its distance from current position
		moveToPos,dist=getBestSpace2(map,beliefMap,currentPos)

		#Add number of moves required to get to desired space and move to desired space
		turns=turns+dist
		currentPos=moveToPos
		print("MOVE TO "+str(currentPos)+"\n")

		#Perform a search at space, add 1 to turns
		turns=turns+1
		if map[currentPos[0]][currentPos[1]].target:
			#Get terrain probability of searched space
			if map[currentPos[0]][currentPos[1]].terrain=='F':
					pTerrain=terrainProbs[0]
			elif map[currentPos[0]][currentPos[1]].terrain=='H':
					pTerrain=terrainProbs[1]
			elif map[currentPos[0]][currentPos[1]].terrain=='T':
					pTerrain=terrainProbs[2]
			else:
				pTerrain=terrainProbs[3]

			#Find if no false negative
			if(random.random()<=pTerrain):
				found=True
		else:
			#If target not found update beliefs
			beliefMap=updateBelief(map,beliefMap,currentPos)
		
	printMap(map)
	print(turns)
	return turns



if __name__ == "__main__":
	main()


