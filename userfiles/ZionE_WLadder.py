# Watches remote accesses to the Whisky west ladder amd
# drives the indicators based on its positions.
#
# Bob Jacobsen for the PMRRM, Copyright 2024
    
class WWLdriver(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):

        turnouts.getTurnout("ZE W3 request").state = CLOSED
        turnouts.getTurnout("ZE W2 request").state = CLOSED
        turnouts.getTurnout("ZE W1 request").state = CLOSED

        sensors.getSensor("ZE W3 ack").state = INACTIVE
        sensors.getSensor("ZE W2 ack").state = INACTIVE
        sensors.getSensor("ZE W1 ack").state = INACTIVE

        return
        
    def handle(self):

        W3Lamp = sensors.getSensor("ZE W3 ack")
        W2Lamp = sensors.getSensor("ZE W2 ack")
        W1Lamp = sensors.getSensor("ZE W1 ack")
        
        # get inputs to process
        W123 = turnouts.getTurnout("Whiskey 12-3").state
        W12 = turnouts.getTurnout("Whiskey 1-2").state      
        
        # compute yard configuration
        if W123 == CLOSED : # track 3
            W3Lamp.state = INACTIVE; W2Lamp.state = INACTIVE; W1Lamp.state = ACTIVE
        elif W123 == THROWN:
            if W12 == CLOSED : # track 2
                W3Lamp.state = INACTIVE; W2Lamp.state = ACTIVE; W1Lamp.state = INACTIVE
            elif W12 == THROWN : # track 1
                W3Lamp.state = ACTIVE; W2Lamp.state = INACTIVE; W1Lamp.state = INACTIVE
        # UNKNOWN, INCONSISTENT fall through                       

        self.waitMsec(300)  # to simulate -Q node
        
        return True
        

wwldriver = WWLdriver()
wwldriver.name = "Whiskey West Ladder"
wwldriver.start()
