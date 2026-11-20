
# No longer used since mainline NX (yellow dots) routing has been disabled.

# PMRRM script to throw in-block turnouts when a block is allocated, e.g.
# when a route is established to/through that block.
#
# Don't include turnouts that are already being thrown because they're on a 
# block boundary.
#
# Bob Jacobsen   2025

import jmri

class CloseTurnoutsWhenBlockAllocated (java.beans.PropertyChangeListener) :

    def __init__(self, blockName, turnoutNames) :
        self.turnoutNames = turnoutNames
        
        log = org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.CloseTurnoutsWhenBlockAllocated"
            )

        block = blocks.getBlock(blockName)
        if block == None :
            log.error("Invalid block name `{}`", blockName)
            return
        
        # check for invalid turnout names
        for turnoutName in self.turnoutNames:
            if turnouts.getTurnout(turnoutName) == None :
                log.error("invalid turnout name `{}` in block `{}`", turnoutName, blockName)
                return

        # add a listener to that block
        block.addPropertyChangeListener(self)
              
    def propertyChange(self, event):
        # listener fired, check whether it's because block is allocated
        if event.getPropertyName() == jmri.Block.PROPERTY_ALLOCATED :
            if event.getNewValue() == True :
                # here we need to throw turnouts
                for turnoutName in self.turnoutNames :
                    turnout = turnouts.getTurnout(turnoutName)
                    turnout.setCommandedState(CLOSED)
        

# and set up the necessary instances
CloseTurnoutsWhenBlockAllocated("Whiskey siding 2", ["Whiskey Grain silo", "Whiskey Grain storage"])

CloseTurnoutsWhenBlockAllocated("Troy main", ["Troy station"])

CloseTurnoutsWhenBlockAllocated("Sierra siding east", ["Sierra E 2"])
CloseTurnoutsWhenBlockAllocated("Sierra siding west", ["Sierra W 2"])
CloseTurnoutsWhenBlockAllocated("Sierra main", ["Sierra camp spur (Bob G guess )"])

CloseTurnoutsWhenBlockAllocated("Powderhorn main", ["Powderhorn crossover main", "Powderhorn housetrack"])
CloseTurnoutsWhenBlockAllocated("Powderhorn siding", ["Powderhorn crossover main", "Powderhorn pocket crossover"])

# Osage 162 may have to be done after changes there

CloseTurnoutsWhenBlockAllocated("Midway main 3 station", ["Midway W Team 1", "Midway E Team 1"])
CloseTurnoutsWhenBlockAllocated("Midway East Main passenger approach", ["Midway E P approach"])

CloseTurnoutsWhenBlockAllocated("Hudson siding", ["Hudson Oil Cans load 1"])
CloseTurnoutsWhenBlockAllocated("Gary siding", ["Gary Tyson Steel"])
# 32 at Gary coming from Hudson siding needs another solution
# 33 at Hudson coming from Gary siding needs another solution

CloseTurnoutsWhenBlockAllocated("Echo 3", ["Echo Street"])

CloseTurnoutsWhenBlockAllocated("Delta 1", ["Colton Ind W"])
CloseTurnoutsWhenBlockAllocated("Delta 4", ["Colton Oil Cans unload", "Colton Grain silo"])

CloseTurnoutsWhenBlockAllocated("Bend 1", ["LT10"])
CloseTurnoutsWhenBlockAllocated("Bend 4", ["Colton Power plant"])

class ThrowTurnoutsWhenBlockAllocated (java.beans.PropertyChangeListener) :

    def __init__(self, blockName, turnoutNames) :
        self.turnoutNames = turnoutNames
        
        log = org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.CloseTurnoutsWhenBlockAllocated"
            )

        block = blocks.getBlock(blockName)
        if block == None :
            log.error("Invalid block name `{}`", blockName)
            return
        
        # check for invalid turnout names
        for turnoutName in self.turnoutNames:
            if turnouts.getTurnout(turnoutName) == None :
                log.error("invalid turnout name `{}` in block `{}`", turnoutName, blockName)
                return

        # add a listener to that block
        block.addPropertyChangeListener(self)
              
    def propertyChange(self, event):
        # listener fired, check whether it's because block is allocated
        if event.getPropertyName() == jmri.Block.PROPERTY_ALLOCATED :
            if event.getNewValue() == True :
                # here we need to throw turnouts
                for turnoutName in self.turnoutNames :
                    turnout = turnouts.getTurnout(turnoutName)
                    turnout.setCommandedState(THROWN)
        

ThrowTurnoutsWhenBlockAllocated("Powderhorn siding", ["Powderhorn work track spur"])
