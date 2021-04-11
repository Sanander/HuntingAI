import random
import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

def main():
	###TESTING
	# dim=50
	# map,targetPos=generateMap(dim)
	# printMap(map)
	# startingPos=(random.randrange(0,dim),random.randrange(0,dim))
	# a=advancedAgent(map,startingPos)
	# print(a)

	################################################
	n=50
	sum1=0
	sum2=0
	sum3=0
	dim=50
	for i in range(0,n):
		startingPos=(random.randrange(0,dim),random.randrange(0,dim))
		map,targetPos=generateMap(dim)
		print("MAP: "+str(i))
		print("TARGET IN "+str(targetPos))
		printMap(map)
		print("\n")
		sum1=sum1+basicAgent1(map,startingPos)
		print("1 done")
		sum2=sum2+basicAgent2(map,startingPos)
		print("2 done")
		sum3=sum3+advancedAgent(map,startingPos)
		print("AVG TURNS 1: "+str(sum1/(i+1)))
		print("AVG TURNS 2: "+str(sum2/(i+1)))
		print("AVG TURNS 3: "+str(sum3/(i+1)))



#Flat='F', Hilly='H', Forrest='T', Caves='C'
class Space():
	def __init__(self, terrain, target=False):
		self.terrain=terrain
		self.target=target
	def __str__(self):
		return self.terrain

#Generate Map
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

#Print Map
def printMap(map):
	print("\n".join([" ".join([str(item) for item in row]) for row in map]))

#Update beleifs using probabilities in Q1 and Q2
def updateBelief(map, belief, observedPos):
	dim=len(map)
	terrainProbs=[0.1, 0.3, 0.7, 0.9]

	sum=0

	if map[observedPos[0]][observedPos[1]].terrain=='F':
			pTerrain=terrainProbs[0]
	elif map[observedPos[0]][observedPos[1]].terrain=='H':
			pTerrain=terrainProbs[1]
	elif map[observedPos[0]][observedPos[1]].terrain=='T':
			pTerrain=terrainProbs[2]
	else:
			pTerrain=terrainProbs[3]

	observedBel=belief[observedPos[0]][observedPos[1]]
	denom=0
	
	denom=1-observedBel+observedBel*pTerrain
	#Update beleifs simultaneously
	for row in range(0,dim):
		for col in range(0,dim):
			if(row!=observedPos[0] or col!=observedPos[1]):
			  belief[row][col]=belief[row][col]/denom
			else:
				belief[row][col]=belief[row][col]*pTerrain/denom
			if(belief[row][col]<0):
				raise Exception("NEGATIVE BELIEF")

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

def basicAgent1(map, startingPos):
	dim=len(map)

	#Initial Beliefs at t=0
	beliefMap=[[1/dim**2 for i in range(dim)] for j in range(dim)]

	found=False
	currentPos=startingPos

	turns=0
	terrainProbs=[0.1, 0.3, 0.7, 0.9]


	while not found:
		
		#Find position with highest belief and its distance from current position
		moveToPos,dist=getBestSpace1(map,beliefMap,currentPos)

		#Add number of moves required to get to desired space and move to desired space
		turns=turns+dist
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
			rand=(random.random())
			#print(str(rand)+" "+str(pTerrain))
			if(rand>=pTerrain):
				found=True
			else:
				#If target not found update beliefs
				beliefMap=updateBelief(map,beliefMap,currentPos)
		else:
			#If target not found update beliefs
			beliefMap=updateBelief(map,beliefMap,currentPos)
			
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
	
	max=belief[currentPos[0]][currentPos[1]]*(1-pTerrain)
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
			if belief[row][col]*(1-pTerrain)>max:
				moveToPos=(row,col)
				max=belief[row][col]*(1-pTerrain)
				spaces=[(row,col)]
			#Same belief, pick closest by Manhattan distance. Store both if equally far
			elif belief[row][col]*(1-pTerrain)==max:
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

def basicAgent2(map,startingPos):
	dim=len(map)
	terrainProbs=[0.1, 0.3, 0.7, 0.9]

	#Initial Beliefs at t=0
	beliefMap=[[1/dim**2 for i in range(dim)] for j in range(dim)]

	found=False
	currentPos=startingPos

	turns=0

	while not found:
		#Find position with highest best chance of finding and its distance from current position
		moveToPos,dist=getBestSpace2(map,beliefMap,currentPos)

		#Add number of moves required to get to desired space and move to desired space
		turns=turns+dist
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
			if(random.random()>=pTerrain):
				found=True
			else:
				#If target not found update beliefs
				beliefMap=updateBelief(map,beliefMap,currentPos)
		else:
			#If target not found update beliefs
			beliefMap=updateBelief(map,beliefMap,currentPos)
		
	return turns

def getBestSpaceAdv(map,belief,currentPos):
	terrainProbs=[0.1, 0.3, 0.7, 0.9]

	if map[currentPos[0]][currentPos[1]].terrain=='F':
			pTerrain=terrainProbs[0]
	elif map[currentPos[0]][currentPos[1]].terrain=='H':
			pTerrain=terrainProbs[1]
	elif map[currentPos[0]][currentPos[1]].terrain=='T':
			pTerrain=terrainProbs[2]
	else:
			pTerrain=terrainProbs[3]
	
	max=belief[currentPos[0]][currentPos[1]]*(1-pTerrain)
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
			if belief[row][col]*(1-pTerrain)>max:
				moveToPos=(row,col)
				max=belief[row][col]*(1-pTerrain)
				spaces=[(row,col)]
			#Same belief, pick closest by Manhattan distance. Store both if equally far
			elif belief[row][col]*(1-pTerrain)==max:
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
	#print("BEST SPACE: "+str(moveToPos))


	#Look for points on the way to target, if best option is far enough
	#Search smaller map with corners at currentPos and moveToPos
	distThreshold=2

	#List of pos to visit en route in order of increasing distance
	listOfPos=PriorityQueue()
	listOfPos.put((dist,(moveToPos[0],moveToPos[1])))

	searchabilityThreshold=0.8*max
	if(dist>distThreshold):
		listOfPos=PriorityQueue()
		topSide=min([currentPos[0],moveToPos[0]])
		leftSide=min([currentPos[1],moveToPos[1]])
		height=abs(currentPos[0]-moveToPos[0])
		width=abs(currentPos[1]-moveToPos[1])
		for row in range(topSide, topSide+height+1):
			for col in range(leftSide, leftSide+width+1):

				if map[row][col].terrain=='F':
					pTerrain=terrainProbs[0]
				elif map[row][col].terrain=='H':
					pTerrain=terrainProbs[1]
				elif map[row][col].terrain=='T':
					pTerrain=terrainProbs[2]
				else:
					pTerrain=terrainProbs[3]

				dist=abs(currentPos[0]-row)+abs(currentPos[1]-col)
				searchability=belief[row][col]*(1-pTerrain)
				if(searchability>searchabilityThreshold):
					listOfPos.put((dist,(row,col)))


	return listOfPos, moveToPos

def advancedAgent(map,startingPos):
	dim=len(map)
	terrainProbs=[0.1, 0.3, 0.7, 0.9]

	#Initial Beliefs at t=0
	beliefMap=[[1/dim**2 for i in range(dim)] for j in range(dim)]

	found=False
	currentPos=startingPos

	turns=0

	while not found:

		#Find position with highest best chance of finding and its distance from current position
		listOfPos,goalPos=getBestSpaceAdv(map,beliefMap,currentPos)
		dist=0

		item=listOfPos.get()
		distanceGroup=item[0]
		itemPos=(item[1][0],item[1][1])
		if map[itemPos[0]][itemPos[1]].terrain=='F':
				pTerrain=terrainProbs[0]
		elif map[itemPos[0]][itemPos[1]].terrain=='H':
				pTerrain=terrainProbs[1]
		elif map[itemPos[0]][itemPos[1]].terrain=='T':
				pTerrain=terrainProbs[2]
		else:
			pTerrain=terrainProbs[3]

		max=beliefMap[itemPos[0]][itemPos[1]]*(1-pTerrain)
		maxItem=item

		while not listOfPos.empty():
			item=listOfPos.get()
			listOfPos.put(item)
			#Pick best of intermediate points
			if(item[0]==distanceGroup):
				item=listOfPos.get()
				itemPos=(item[1][0],item[1][1])
				if map[itemPos[0]][itemPos[1]].terrain=='F':
						pTerrain=terrainProbs[0]
				elif map[itemPos[0]][itemPos[1]].terrain=='H':
						pTerrain=terrainProbs[1]
				elif map[itemPos[0]][itemPos[1]].terrain=='T':
						pTerrain=terrainProbs[2]
				else:
					pTerrain=terrainProbs[3]

				if(beliefMap[itemPos[0]][itemPos[1]]*(1-pTerrain)>max and abs(itemPos[0]-goalPos[0])+abs(itemPos[1]-goalPos[1])<abs(currentPos[0]-goalPos[0])+abs(currentPos[1]-goalPos[1])):
					maxItem=item
			else:
				#If moving to a new distance search best at previous dist
				moveToPos=maxItem[1]
				dist=abs(moveToPos[0]-currentPos[0])+abs(moveToPos[1]-currentPos[1])

				#Add number of moves required to get to desired space and move to desired space
				turns=turns+dist
				#print("INTERMEDIATE MOVE FROM "+str(currentPos)+"TO "+str(moveToPos)+" IN "+str(dist)+ " MOVES AND SEARCH\n")
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
					if(random.random()>=pTerrain):
						found=True
					else:
						#If target not found update beliefs
						beliefMap=updateBelief(map,beliefMap,currentPos)
				else:
					#If target not found update beliefs
					beliefMap=updateBelief(map,beliefMap,currentPos)

				#Get next item
				item=listOfPos.get()
				distanceGroup=item[0]
				itemPos=(item[1][0],item[1][1])
				if map[itemPos[0]][itemPos[1]].terrain=='F':
						pTerrain=terrainProbs[0]
				elif map[itemPos[0]][itemPos[1]].terrain=='H':
						pTerrain=terrainProbs[1]
				elif map[itemPos[0]][itemPos[1]].terrain=='T':
						pTerrain=terrainProbs[2]
				else:
					pTerrain=terrainProbs[3]

				max=beliefMap[itemPos[0]][itemPos[1]]*(1-pTerrain)
				maxItem=item
				
		#Search last space in queue
		moveToPos=maxItem[1]
		dist=abs(moveToPos[0]-currentPos[0])+abs(moveToPos[1]-currentPos[1])
		turns=turns+dist
		#print("MOVE FROM "+str(currentPos)+"TO "+str(moveToPos)+" IN "+str(dist)+ " MOVES AND SEARCH\n")
		currentPos=moveToPos

		turns=turns+1
		if map[currentPos[0]][currentPos[1]].target:
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
		

	return turns



if __name__ == "__main__":
	main()


