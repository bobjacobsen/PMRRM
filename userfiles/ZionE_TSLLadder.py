# Watches remote accesses to the TE3-SL8,9 ladder amd
# drives the indicators based on its positions.
#
# Bob Jacobsen for the PMRRM, Copyright 2024
    
class ZTSLdriver(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        turnouts.getTurnout("ZE T5 request").state = CLOSED
        turnouts.getTurnout("ZE P8 request").state = CLOSED
        turnouts.getTurnout("ZE P9 request").state = CLOSED
        sensors.getSensor("ZE T5 ack").state = INACTIVE
        sensors.getSensor("ZE P8 ack").state = INACTIVE
        sensors.getSensor("ZE P9 ack").state = INACTIVE
        return
        
    def handle(self):

        T5Lamp = sensors.getSensor("ZE T5 ack")
        P8Lamp = sensors.getSensor("ZE P8 ack")
        P9Lamp = sensors.getSensor("ZE P9 ack")
        
        # get inputs to process
        P89T5 = turnouts.getTurnout("Zion Branch East P89-TE5").state
        P98 =  turnouts.getTurnout("Zion Branch East P9-P8").state      
        
        # compute yard configuration
        if P89T5 == THROWN : # track TE5
            T5Lamp.state = ACTIVE; P8Lamp.state = INACTIVE; P9Lamp.state = INACTIVE
        elif P89T5 == CLOSED :
            if P98 == CLOSED : # track P8
                T5Lamp.state = INACTIVE; P8Lamp.state = ACTIVE; P9Lamp.state = INACTIVE
            elif P98 == THROWN : # track P9
                T5Lamp.state = INACTIVE; P8Lamp.state = INACTIVE; P9Lamp.state = ACTIVE
        # UNKNOWN, INCONSISTENT fall through                       
     
        self.waitMsec(300)  # to simulate -Q node
        
        return True
        

ztsldriver = ZTSLdriver()
ztsldriver.name = "TE5-P89 ladder"
ztsldriver.start()
