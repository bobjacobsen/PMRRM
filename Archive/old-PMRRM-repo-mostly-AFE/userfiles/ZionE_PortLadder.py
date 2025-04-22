# Watches remote accesses to the Port ladder amd
# drives the indicators based on its positions.
#
# Bob Jacobsen for the PMRRM, Copyright 2024
    
class ZPLdriver(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        turnouts.getTurnout("ZE PT1 request").state = CLOSED
        turnouts.getTurnout("ZE PT2 request").state = CLOSED
        turnouts.getTurnout("ZE PT3 request").state = CLOSED
        sensors.getSensor("ZE PT1 ack").state = INACTIVE
        sensors.getSensor("ZE PT2 ack").state = INACTIVE
        sensors.getSensor("ZE PT3 ack").state = INACTIVE
        print ("init done")
        
        return
        
    def handle(self):

        PT1Lamp = sensors.getSensor("ZE PT1 ack")
        PT2Lamp = sensors.getSensor("ZE PT2 ack")
        PT3Lamp = sensors.getSensor("ZE PT3 ack")
        
        # get inputs to process
        PT123 = turnouts.getTurnout("Zion Port PT23-PT1").state
        PT23 =  turnouts.getTurnout("Zion Port PT2-PT3").state       
        
        # compute yard configuration
        if PT123 == CLOSED : # track 1
            PT1Lamp.state = ACTIVE; PT2Lamp.state = INACTIVE; PT3Lamp.state = INACTIVE
        elif PT123 == THROWN : 
            if PT23 == CLOSED : # track 2
                PT1Lamp.state = INACTIVE; PT2Lamp.state = ACTIVE; PT3Lamp.state = INACTIVE
            elif PT23 == THROWN :         # track 3
                PT1Lamp.state = INACTIVE; PT2Lamp.state = INACTIVE; PT3Lamp.state = ACTIVE
        # UNKNOWN, INCONSISTENT fall through  
                             
        self.waitMsec(300)  # to simulate -Q node
        
        return True
        

zpldriver = ZPLdriver()
zpldriver.name = "Port ladder"
zpldriver.start()
