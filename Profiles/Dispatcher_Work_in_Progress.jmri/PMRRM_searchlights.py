# A class and specific instantiations to run single lamp ABS semaphore masts.
# Written for the Pasadena Model Railroad Museum, PMRRM
#
# Bob Jacobsen, 2025
#

# You specify 
#  .local    The local signal being controlled
#  .blocks   A list of the sensors being protected
#  .turnouts A list of the turnouts being protected
#  .next     The next signal being protected
#  .next2    A possible 2nd head on the next signal being protected
# 
# You must specify _all_ of these.  Store [] if the lists have no content

import jmri
import time
from org.slf4j import LoggerFactory

class ControlAbsSearchlight (jmri.jmrit.automat.AbstractAutomaton) :
    def current_milli_time(self):
        return int(time.time() * 1000)
        
    def init(self) :
        
        self.minAcceptableTime = 200

        # create a list of inputs to watch
        self.beans = []
        self.beans.extend(self.blocks)
        self.beans.extend(self.turnouts)
        if self.next != False :  self.beans.append(self.next)
        if self.next2 != False : self.beans.append(self.next2)
        
        # Remember the current state of the beans for a later waitCheck
        self.waitChangePrecheck(self.beans)
        
        self.lastTime = self.current_milli_time() - self.minAcceptableTime # subtract to skip warning on 1st cycle
        self.lastBeans = []
        self.log = LoggerFactory.getLogger("PMRRM_searchlights");

        # Printing the equivalent STL goes here
        
        return
        
    def handle(self) :
        # check for running too quickly
        delta = self.current_milli_time() - self.lastTime 
        if delta < self.minAcceptableTime :
            # ran abnormally quickly
            self.log.info("Searchlight logic {} ran in {} msec", self.getName(), delta)
            self.log.info("prior time {}", str(self.priorBeans))
            self.log.info("last time  {}", str(self.lastBeans))
            beansNow = []
            for bean in self.beans:
                beansNow.append(bean.describeState(bean.state))
            self.log.info("     now   {}", str(beansNow))
            
        self.lastTime = self.current_milli_time()
        self.priorBeans = self.lastBeans
        self.lastBeans = []
        for bean in self.beans:
            self.lastBeans.append(bean.describeState(bean.state))

        class workOnLayout(jmri.util.ThreadingUtil.ThreadAction):
            def __init__(self, blocks, turnouts, local, next, next2):
                self.blocks = blocks
                self.turnouts = turnouts
                self.local = local
                self.next = next
                self.next2 = next2

            def run(self):
                # do the work that needs to access the GUI
                        
                # calculate the searchlight appearances and write if needed

                local = GREEN
        
                nextRed = True
                if self.next != False :
                    if self.next.getAppearance() != RED :
                        nextRed = False
                if self.next2 != False :
                    if self.next2.getAppearance() != RED :
                        nextRed = False
                if nextRed : local = YELLOW
        
                for sensor in self.blocks :
                    if sensor.state != INACTIVE :
                        local = RED
                        
                for turnout in self.turnouts :
                    if turnout.state != CLOSED :
                        local = RED
                                    
                if local != self.local.getAppearance() :
                    self.local.setAppearance(local)
                
        # invoke on layout thread
        jmri.util.ThreadingUtil.runOnLayout(workOnLayout(self.blocks, self.turnouts, self.local, self.next, self.next2))

        self.waitChange(self.beans)  # run again when something changes or after a delay (just in case)?
        
        return True

# ##################################
# PMRRM-specific applications follow
# ##################################

# ###### West to East ######

a = ControlAbsSearchlight()
a.setName("W Sierra Main")
a.local    = signals.getSignalHead("W Sierra Main")
a.blocks   = [sensors.getSensor("Sierra main")]
a.turnouts = [turnouts.getTurnout("Sierra W"), turnouts.getTurnout("Sierra E")]
a.next     = signals.getSignalHead("W R-S Sem")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W S-T")
a.local    = signals.getSignalHead("W S-T")
a.blocks   = [sensors.getSensor("S-T")]
a.turnouts = []
a.next     = signals.getSignalHead("W Sierra Main")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W Troy Main")
a.local    = signals.getSignalHead("W Troy Main")
a.blocks   = [sensors.getSensor("Troy main")]
a.turnouts = [turnouts.getTurnout("Troy W 1"), turnouts.getTurnout("Troy E 1"), turnouts.getTurnout("Troy station")]
a.next     = signals.getSignalHead("W S-T")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W U-T")
a.local    = signals.getSignalHead("W U-T")
a.blocks   = [sensors.getSensor("T-U")]
a.turnouts = []
a.next     = signals.getSignalHead("W Troy Main")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W Upton Main")
a.local    = signals.getSignalHead("W Upton Main")
a.blocks   = [sensors.getSensor("Upton main")]
a.turnouts = [turnouts.getTurnout("Upton W"), turnouts.getTurnout("Upton E")]
a.next     = signals.getSignalHead("W U-T")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W U-V")
a.local    = signals.getSignalHead("W U-V")
a.blocks   = [sensors.getSensor("U-Vw"), sensors.getSensor("U-Ve")]
a.turnouts = []
a.next     = signals.getSignalHead("W Upton Main")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W Vista Main")
a.local    = signals.getSignalHead("W Vista Main")
a.blocks   = [sensors.getSensor("Vista main")]
a.turnouts = [turnouts.getTurnout("Vista W 1"), turnouts.getTurnout("Vista E 1"), turnouts.getTurnout("Vista W 2"), turnouts.getTurnout("Vista E 2")]
a.next     = signals.getSignalHead("W U-T")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W V-W")
a.local    = signals.getSignalHead("W V-W")
a.blocks   = [sensors.getSensor("V-W")]
a.turnouts = []
a.next     = signals.getSignalHead("W Vista Main")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("W Whiskey Main")
a.local    = signals.getSignalHead("W Whiskey Main")
a.blocks   = [sensors.getSensor("Whiskey main")]
a.turnouts = [turnouts.getTurnout("Whiskey W 1"), turnouts.getTurnout("Whiskey E 1")]
a.next     = signals.getSignalHead("W V-W")
a.next2    = False
a.start()



# ###### East to West ######

a = ControlAbsSearchlight()
a.setName("E W-X")
a.local    = signals.getSignalHead("E W-X")
a.blocks   = [sensors.getSensor("W-X")]
a.turnouts = []
a.next     = signals.getSignalHead("E Xerox Main")
a.next2    = False # according to Mike, as E W-X is single-head, it only references top head at Xerox entrance
a.start()

a = ControlAbsSearchlight()
a.setName("E Whiskey Main")
a.local    = signals.getSignalHead("E Whiskey Main")
a.blocks   = [sensors.getSensor("Whiskey main")]
a.turnouts = [turnouts.getTurnout("Whiskey W 1"), turnouts.getTurnout("Whiskey E 1")]
a.next     = signals.getSignalHead("E W-X")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("E V-W")
a.local    = signals.getSignalHead("E V-W")
a.blocks   = [sensors.getSensor("V-W")]
a.turnouts = []
a.next     = signals.getSignalHead("E Whiskey Main")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("E Vista Main")
a.local    = signals.getSignalHead("E Vista Main")
a.blocks   = [sensors.getSensor("Vista main")]
a.turnouts = [turnouts.getTurnout("Vista W 1"), turnouts.getTurnout("Vista E 1"), turnouts.getTurnout("Vista W 2"), turnouts.getTurnout("Vista E 2")]
a.next     = signals.getSignalHead("E V-W")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("E U-V")
a.local    = signals.getSignalHead("E U-V")
a.blocks   = [sensors.getSensor("U-Vw"), sensors.getSensor("U-Ve")]
a.turnouts = []
a.next     = signals.getSignalHead("E Vista Main")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("E Upton Main")
a.local    = signals.getSignalHead("E Upton Main")
a.blocks   = [sensors.getSensor("Upton main")]
a.turnouts = [turnouts.getTurnout("Upton W"), turnouts.getTurnout("Upton E")]
a.next     = signals.getSignalHead("E U-V")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("E T-U")
a.local    = signals.getSignalHead("E T-U")
a.blocks   = [sensors.getSensor("T-U")]
a.turnouts = []
a.next     = signals.getSignalHead("E Upton Main")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("E Troy Main")
a.local    = signals.getSignalHead("E Troy Main")
a.blocks   = [sensors.getSensor("Troy main")]
a.turnouts = [turnouts.getTurnout("Troy W 1"), turnouts.getTurnout("Troy E 1"), turnouts.getTurnout("Troy station")]
a.next     = signals.getSignalHead("E T-U")
a.next2    = False
a.start()

a = ControlAbsSearchlight()
a.setName("E S-T")
a.local    = signals.getSignalHead("E S-T")
a.blocks   = [sensors.getSensor("S-T")]
a.turnouts = []
a.next     = signals.getSignalHead("E Troy Main")
a.next2    = False
a.start()
