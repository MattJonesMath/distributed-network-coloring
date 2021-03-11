###############################################################################
# Graph Coloring Problem
# Creates a number of networks with certain parameters
###############################################################################

#from playerColoringCoordination import Player
from playerMemoryCC import Player
#from rFMPlayer import Player
import random as rand
from statistics import mean
import matplotlib.pyplot as plt

#Parameters
iterations = 1000

graphSize = 50
randProb = 0.8
randFrac = 1.0
colNum = 2
aveDeg = 2

randPlayers = int(graphSize*randFrac)
    

#############################################################
#parameters
averageDegree = aveDeg
colorNumber = colNum


conflictListList = []


# Create and solve networks
for iter in range(iterations):
    if iter%50==0:
        print(iter)
    
    players = []
    adjList = []
    
    # Create the players in the population, adjacency lists
    edgeProb=colorNumber*averageDegree/(graphSize*(colorNumber-1))
    colorList = [[] for _ in range(colorNumber)]
    
    for indx in range(graphSize):
        player = Player()
        player.setMemory(1)
        player.colorOptions = list(range(colorNumber))
        players.append(player)
        adjList.append([])
        rand.choice(colorList).append(indx)
        
    for i in range(colorNumber):
        for j in range(i):
            for indx in colorList[i]:
                for nindx in colorList[j]:
                    if rand.random()<edgeProb:
                        adjList[indx].append(nindx)
                        adjList[nindx].append(indx)
                    
    # Make randPlayers have random behavior
    tempList = list(range(graphSize))
    rand.shuffle(tempList)
    randList = tempList[0:randPlayers]
    
    for indx in randList:
        players[indx].randProb = randProb
        
    # Initialize with random colors
    for player in players:
        player.color = rand.choice(player.colorOptions)
    
    #######################################################################
    # Continually update graph until time limit
    #######################################################################
    updateCycles = 0
    conflictList = []
    
    # A randomized order in which the players will update
    upOrder = list(range(graphSize))
    rand.shuffle(upOrder)
    upSpot = 0
    
    conflicts = 0
    
    # Count initial number of conflicts
    for indx in range(graphSize):
        for nindx in adjList[indx]:
            if players[indx].color == players[nindx].color:
                conflicts += 0.5   
    conflictList.append(conflicts)
    
    while updateCycles < 2000:
        if upSpot == 0:
            updateCycles += 1
            
        if not conflicts==0:
            ncolors=[players[indx].color for indx in adjList[upOrder[upSpot]]]
            oldColor = players[upOrder[upSpot]].color
            if players[upOrder[upSpot]].update(ncolors):
                # change the number of conflicts
                newColor = players[upOrder[upSpot]].color
                conflicts -= ncolors.count(oldColor)
                conflicts += ncolors.count(newColor)
            
        upSpot = (upSpot + 1) % graphSize
        
        conflictList.append(conflicts)
        
        
    conflictListList.append(conflictList)
    
conflictMeans = [mean([x[i] for x in conflictListList]) for i in range(len(conflictList))]
#plt.plot(conflictMeans)
            