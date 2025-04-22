# Monitor the LCC "Zion East Zion - Port" TO
# and use it's initial state to set the 
# state of the combined "ZE Branch - Port Interchange Request" sensor.
# That sensor is then used via a route to change
# both "Zion East Zion - Port" (LCC) and the
# LocoNet/LCC "Zion Branch East Port-Zion" TO

import jmri
import java

class PortEastStartup(jmri.jmrit.automat.AbstractAutomaton) :
        
    def handle(self):
         
        self.waitMsec(500)  # limit cycle time
        
        to = turnouts.getTurnout("Zion East Zion - Port")
        sensor = sensors.getSensor("ZE Branch - Port Interchange Request")
        
        if to.state == THROWN :
            sensor.state = ACTIVE
            return False # done
        elif to.state == CLOSED :
            sensor.state = INACTIVE
            return False # done
        
        # UNKNOWN, INCONISTENT go around again
        
        return True #repeat
        

portEastStartup = PortEastStartup()
portEastStartup.name = "Port East Startup"
portEastStartup.start()
