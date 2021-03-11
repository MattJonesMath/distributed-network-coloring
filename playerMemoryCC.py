###############################################################################
# Player class for the color coordination game
###############################################################################

import random as rand

class Player:
    def __init__(self):
        # Initial Color
        self.color = 0
        self.colorOptions = [0,1]
        self.randProb = 0.0
        self.memory = 0
        self.nLists = []
        
    def setMemory(self, n):
        self.memory = n
        self.nLists = [[] for _ in range(n)]
        
    def update(self, ncolors):
        oldColor = self.color
        updated = False
        
        while updated == False:
            
            # Check if current color is acceptable
            if self.color not in ncolors:
                updated = True
                break
            
            # Check all possible colors to see if one is acceptable
            possibleColors = []
            for color in self.colorOptions:
                if color not in ncolors:
                    possibleColors.append(color)
            if possibleColors:
                self.color = rand.choice(possibleColors)
                updated = True
                break
            
            # If neighborhood has remained unchanged for long enough, random
            if self.nLists==[ncolors]*self.memory and rand.random()<self.randProb:
                self.color = rand.choice(self.colorOptions)
                updated = True
                break
            
            # If all else fails, pick a color to minimize local conflicts
            frequency = []
            for color in self.colorOptions:
                frequency.append(ncolors.count(color))
            lowfreq = min(frequency)
            possibleColors = []
            for indx in range(len(frequency)):
                if frequency[indx] == lowfreq:
                    possibleColors.append(self.colorOptions[indx])
            self.color = rand.choice(possibleColors)
            updated = True
            
        #Update nLists
        if self.memory != 0:
            self.nLists.remove(self.nLists[0])
            self.nLists.append(ncolors)
            
        newColor = self.color
        if not oldColor == newColor:
            return True
        else:
            return False
                    
    def checkLocal(self, ncolors):
        if self.color not in ncolors:
            return True
        else:
            return False
            
            
        
        
            
    
        