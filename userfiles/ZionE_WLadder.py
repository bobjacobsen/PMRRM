# Watches remote accesses to the Whisky west ladder amd
# drives the indicators based on its positions.
#
# Bob Jacobsen for the PMRRM, Copyright 2024
    
class WWLdriver(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        return
        
    def handle(self):

        W3Lamp = sensors.getSensor("ZE W3 ack")
        W2Lamp = sensors.getSensor("ZE W2 ack")
        W1Lamp = sensors.getSensor("ZE W1 ack")
        
        # get inputs to process
        W123 = turnouts.getTurnout("Whiskey 12-3").state == THROWN
        W12 = turnouts.getTurnout("Whiskey 1-2").state == THROWN        
        
        # compute yard configuration
        if not W123 : # track 3
            W3Lamp.state = INACTIVE; W2Lamp.state = INACTIVE; W1Lamp.state = ACTIVE
        elif not W12 : # track 2
            W3Lamp.state = INACTIVE; W2Lamp.state = ACTIVE; W1Lamp.state = INACTIVE
        else :        # track 1
            W3Lamp.state = ACTIVE; W2Lamp.state = INACTIVE; W1Lamp.state = INACTIVE
                              
        self.waitMsec(300)  # to simulate -Q node
        
        return True
        

wwldriver = WWLdriver()
wwldriver.name = "Whiskey West Ladder"
wwldriver.start()
