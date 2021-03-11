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
        
    def update(self, ncolors):
        oldColor = self.color
        updated = False
        
        # With probability self.randprob, choose random color
        r = rand.random()
        if updated==False and r<self.randProb:
            self.color=rand.choice(self.colorOptions)
            updated = True
        
        # Check if current color is acceptable
        if updated==False and self.color not in ncolors:
            updated = True
            
        # Check all possible colors to see if one is acceptable
        if updated==False:
            possibleColors = []
            for color in self.colorOptions:
                if color not in ncolors:
                    possibleColors.append(color)
            if possibleColors:
                self.color=rand.choice(possibleColors)
                updated=True
                
        # Pick the color with the fewest matching neighbors
        if updated==False:
            frequency = []
            for color in self.colorOptions:
                frequency.append(ncolors.count(color))
            lowfreq=min(frequency)   
            possibleColors = []
            for indx in range(len(frequency)):
                if frequency[indx]==lowfreq:
                    possibleColors.append(self.colorOptions[indx])
            self.color=rand.choice(possibleColors)
            updated=True
            
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
            
            
        
        
            
    
        