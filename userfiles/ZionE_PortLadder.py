# Watches remote accesses to the Port ladder amd
# drives the indicators based on its positions.
#
# Bob Jacobsen for the PMRRM, Copyright 2024
    
class ZPLdriver(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        return
        
    def handle(self):

        PT1Lamp = sensors.getSensor("ZE PT1 ack")
        PT2Lamp = sensors.getSensor("ZE PT2 ack")
        PT3Lamp = sensors.getSensor("ZE PT3 ack")
        
        # get inputs to process
        PT123 = turnouts.getTurnout("Zion Port PT23-PT1").state == THROWN
        PT23 =  turnouts.getTurnout("Zion Port PT2-PT3").state == THROWN        
        
        # compute yard configuration
        if not PT123 : # track 1
            PT1Lamp.state = ACTIVE; PT2Lamp.state = INACTIVE; PT3Lamp.state = INACTIVE
        elif not PT23 : # track 2
            PT1Lamp.state = INACTIVE; PT2Lamp.state = ACTIVE; PT3Lamp.state = INACTIVE
        else :         # track 3
            PT1Lamp.state = INACTIVE; PT2Lamp.state = INACTIVE; PT3Lamp.state = ACTIVE
                              
        self.waitMsec(300)  # to simulate -Q node
        
        return True
        

zpldriver = ZPLdriver()
zpldriver.name = "Port ladder"
zpldriver.start()
