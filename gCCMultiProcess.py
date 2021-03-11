###############################################################################
# multiprocess graph color coordination code
# create a list of parameter values
# run a given number of iterations for each parameter set
###############################################################################

import multiprocessing
#from playerColoringCoordination import Player
from playerMemoryCC import Player
import random as rand
from statistics import mean
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def runSimulations(parameters):
    # Unpack parameters
    randProb = parameters[0]
    randFrac = parameters[1]
    graphSize = parameters[2]
    averageDegree = parameters[3]
    randPlayers = int(graphSize*randFrac)
    iterations = parameters[4]
    colorNumber = parameters[5]
    memory = parameters[6]
    
    updateCyclesList = []
    updatedPlayersList = []
    unsolvedNetworks = 0
    
    # Create and solve networks
    for iter in range(iterations):
        
        players = []
        adjList = []
        
        # Create the players in the population, adjacency lists
        edgeProb=colorNumber*averageDegree/(graphSize*(colorNumber-1))
        colorList = [[] for _ in range(colorNumber)]
        
        for indx in range(graphSize):
            player = Player()
            player.setMemory(memory)
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
        # Continually update graph until coloring is found
        #######################################################################
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
#                updateCycles=0
#                updatedPlayers = 0
                break
            
            
        if updateCycles == 10000:
            unsolvedNetworks+=1
             
        updateCyclesList.append(updateCycles)
        updatedPlayersList.append(updatedPlayers)
            
    results = [updateCyclesList, updatedPlayersList, unsolvedNetworks]
    return results
        
        
    
if __name__ == '__main__':
    ###########################################################################
    # create the parameter values for each run
    # [randProb, randFrac, graphSize, averageDegree, iterations, color number, memory]
    ###########################################################################
    graphSize = 50 
    aveDeg = 2
    iters = 2
    colNum = 2
    memory = 0
    
    randProbs = []
    for i in range(20):
        randProbs.append(0.05 + i/20)
    randFracs = []
    for i in range(20):
        randFracs.append(0.05 + i/20)   
        
    paramValues = []
    paramValues.append([0.0,0.0,graphSize,aveDeg, iters, colNum, memory])
    for randProb in randProbs:
        for randFrac in randFracs:
            paramValues.append([randProb,randFrac,graphSize,aveDeg, iters, colNum, memory])
            
    ###########################################################################
    # Multiprocessing
    ###########################################################################
    poolSize = 10
    pool = multiprocessing.Pool(processes=poolSize)
    
    results = pool.map(runSimulations, paramValues)
    
    ###########################################################################
    # Process results
    ###########################################################################
    
    unsolvedNetworks = [temp[2] for temp in results]
    updateCycles = [mean(temp[0]) for temp in results]
    updatedPlayers = [mean(temp[1]) for temp in results]
    
    noRandNet = unsolvedNetworks[0]
    noRandCycle = updateCycles[0]
    noRandPlayers = updatedPlayers[0]
    for randProb in randProbs:
        paramValues.append([randProb, 0.0, graphSize, aveDeg, iters, colNum, memory])
        unsolvedNetworks.append(noRandNet)
        updateCycles.append(noRandCycle)
        updatedPlayers.append(noRandPlayers)
    for randFrac in randFracs:
        paramValues.append([0.0, randFrac, graphSize, aveDeg, iters, colNum, memory])
        unsolvedNetworks.append(noRandNet)
        updateCycles.append(noRandCycle)
        updatedPlayers.append(noRandPlayers)
        
    
    randProbVals = [param[0] for param in paramValues]
    randFracVals = [param[1] for param in paramValues]
    unNetTrunc = [min([10,x]) for x in unsolvedNetworks]
    
    
    #########################
    # Only create plots on pc
    #########################
#    plt.subplots()
#    ax = plt.axes(projection='3d')
#    ax.plot_trisurf(randProbVals,randFracVals,unsolvedNetworks, 
#                    cmap='viridis', edgecolor='none')
#    ax.set_xlabel('random probability')
#    ax.set_ylabel('fraction of population')
#    
#    plt.subplots()
#    ax = plt.axes(projection='3d')
#    ax.plot_trisurf(randProbVals,randFracVals,unNetTrunc, 
#                    cmap='viridis', edgecolor='none')
#    ax.set_xlabel('random probability')
#    ax.set_ylabel('fraction of population')
#    
#    plt.subplots()
#    ax = plt.axes(projection='3d')
#    ax.plot_trisurf(randProbVals,randFracVals,updateCycles, 
#                    cmap='viridis', edgecolor='none')
#    ax.set_xlabel('random probability')
#    ax.set_ylabel('fraction of population')
#    
#    plt.subplots()
#    ax = plt.axes(projection='3d')
#    ax.plot_trisurf(randProbVals,randFracVals,updatedPlayers, 
#                    cmap='viridis', edgecolor='none')
#    ax.set_xlabel('random probability')
#    ax.set_ylabel('fraction of population')


    print('parameter values are:')
    print(paramValues)
    print('unsolved network numbers are:')
    print(unsolvedNetworks)
    print('update cycle numbers are:')
    print(updateCycles)
    print('updated player numbers are:')
    print(updatedPlayers)
    

    
    
    
    