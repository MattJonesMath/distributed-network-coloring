###############################################################################
# Graph Coloring Coordination Problem
###############################################################################

from playerColoringCoordination import Player
#from playerMemoryCC import Player
#from rFMPlayer import Player
import random as rand



###############################################################################
# Create Graph
###############################################################################

players = []
adjList = []

            
randProb = 0.5
randFrac = 0.5
colorNumber = 2
graphSize=50
averageDegree = 2
randPlayers = int(randFrac*graphSize)
    
edgeProb=colorNumber*averageDegree/(graphSize*(colorNumber-1))
colorList = [[] for _ in range(colorNumber)]

for indx in range(graphSize):
    player = Player()
    #player.setMemory(2)
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

###############################################################################
# Continually update graph until coloring is found
###############################################################################
updateCycles = 0
updatedPlayers = 0

# A randomized order in which the players will update
upOrder = list(range(graphSize))
rand.shuffle(upOrder)
upSpot = 0

localColoring = [False]*graphSize

while False in localColoring:
    if upSpot == 0:
        updateCycles += 1
        # Check if a coloring has been reached
        for indx in range(graphSize):
            ncolors = [players[indx].color for indx in adjList[indx]]
            localColoring[indx] = players[indx].checkLocal(ncolors)
        
    ncolors=[players[indx].color for indx in adjList[upOrder[upSpot]]]
    if players[upOrder[upSpot]].update(ncolors):
        updatedPlayers += 1

    upSpot = (upSpot + 1) % graphSize
    
    if updateCycles == 10000:
        break
        
colors = [players[indx].color for indx in range(graphSize)]
























