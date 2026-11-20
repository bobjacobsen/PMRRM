# QueryLnSensorState.py
# 
# Does a sensor state query using the same messages that a LocoNet
# command station issues on power up, without sending power up itself.
#
# Bob Jacobsen  2025

import java
import jmri

class QueryLnSensorState (jmri.jmrit.automat.AbstractAutomaton) :

    def handle(self) : 
        self.waitMsec(25000) # compare to HighlightUnknownBlockSensors
        memories.provideMemory("IMProgramStatus").setValue("Querying LocoNet Sensors")

        manager = jmri.InstanceManager.getList(jmri.jmrix.loconet.LocoNetSystemConnectionMemo).get(0).getSensorManager()
        if manager != None :
            manager.updateAll()   # starts a separate thread
        else : 
            print "Did not retrieve the LnSensorManager"
    
QueryLnSensorState().start()
