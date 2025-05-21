# A class and specific instantiations to run dual lower-quadrant semaphore masts.
# Written for the Pasadena Model Railroad Museum, PMRRM
#
# Bob Jacobsen, 2025
#

# You specify 
#  .upper   The upper semaphore being controlled
#  .lower   The lower semaphone being controlled
#  .blocks  A list of the sensors being protected
#  .turnouts A list of the turnouts being protected
#  .next    The next upper semaphore (or signal) being protected
# 
# You must specify _all_ of these.  Store [] if the lists have no content

import jmri
import time
from org.slf4j import LoggerFactory

class ControlDualSemaphore (jmri.jmrit.automat.AbstractAutomaton) :
    def current_milli_time(self):
        return int(time.time() * 1000)
        
    def init(self) :
        
        self.minAcceptableTime = 200
        
        # create a list of inputs to watch
        self.beans = []
        self.beans.extend(self.blocks)
        self.beans.extend(self.turnouts)
        if self.next and self.next != False : self.beans.append(self.next)
        
        # Remember the current state of the beans for a later waitCheck
        self.waitChangePrecheck(self.beans)
        
        self.lastTime = self.current_milli_time() - self.minAcceptableTime # subtract to skip warning on 1st cycle
        self.priorBeans = []
        self.lastBeans = []
        self.log = LoggerFactory.getLogger("PMRRM_semaphores");
        
        # Printing the equivalent STL goes here
        
        return
        
    def handle(self) :
        # this defers to immediately run on Layout Thread

        # check for running too quickly
        delta = self.current_milli_time() - self.lastTime 
        if delta < self.minAcceptableTime :
            # ran abnormally quickly
            self.log.info("Semaphore logic {} ran in {} msec", self.getName(), delta)
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
            def __init__(self, blocks, turnouts, upper, lower, next):
                self.blocks = blocks
                self.turnouts = turnouts
                self.upper = upper
                self.lower = lower
                self.next = next

            def run(self):
                # do the work that needs to access the GUI
                        
                # calculate the semaphore positions and write if needed
                upper = GREEN
        
                for sensor in self.blocks :
                    if sensor.state != INACTIVE :
                        upper = RED
                        
                for turnout in self.turnouts :
                    if turnout.state != CLOSED :
                        upper = RED
                        
                if upper != self.upper.getAppearance() :
                    self.upper.setAppearance(upper)
                
                lower = RED             # might not have next signal, in which case show Approach
                if self.next and self.next != False :
                    if self.next.getAppearance() != RED :
                        lower = GREEN
                if upper == RED : 
                    lower = RED
        
                if lower != self.lower.getAppearance() :
                    self.lower.setAppearance(lower)
        
        # invoke on layout thread
        jmri.util.ThreadingUtil.runOnLayout(workOnLayout(self.blocks, self.turnouts, self.upper, self.lower, self.next))

        self.waitChange(self.beans)  # run again when something changes or after a delay (just in case)?
        
        return True

# ##################################
# PMRRM-specific applications follow
# ##################################

# ###### West to East ######

a = ControlDualSemaphore()
a.setName("W LN Sem")
a.upper    = signals.getSignalHead("W LN Sem")
a.lower    = signals.getSignalHead("W LN Sem L")
a.blocks   = [sensors.getSensor("Narrows Lower")]
a.turnouts = []
a.next     = False
a.start()

a = ControlDualSemaphore()
a.setName("W UN Sem")
a.upper    = signals.getSignalHead("W UN Sem")
a.lower    = signals.getSignalHead("W UN Sem L")
a.blocks   = [sensors.getSensor("Narrows Upper")]
a.turnouts = []
a.next     = signals.getSignalHead("W LN Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W Osage Sem")
a.upper    = signals.getSignalHead("W Osage Sem")
a.lower    = signals.getSignalHead("W Osage Sem L")
a.blocks   = [sensors.getSensor("Osage main"), sensors.getSensor("Osage approach")]
a.turnouts = [turnouts.getTurnout("Osage W"), turnouts.getTurnout("Osage crossover"), turnouts.getTurnout("Osage pocket")]
a.next     = signals.getSignalHead("W UN Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W OP Sem")
a.upper    = signals.getSignalHead("W OP Sem")
a.lower    = signals.getSignalHead("W OP Sem L")
a.blocks   = [sensors.getSensor("O-P")]
a.turnouts = [turnouts.getTurnout("McSweeney")]
a.next     = signals.getSignalHead("W Osage Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W Powder Sem")
a.upper    = signals.getSignalHead("W Powder Sem")
a.lower    = signals.getSignalHead("W Powder Sem L")
a.blocks   = [sensors.getSensor("Powderhorn main")]
a.turnouts = [turnouts.getTurnout("Powderhorn W"), turnouts.getTurnout("Powderhorn E"), turnouts.getTurnout("Powderhorn house"), turnouts.getTurnout("Powderhorn pocket"), turnouts.getTurnout("Powderhorn crossover")]
a.next     = signals.getSignalHead("W OP Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E RP Sem")
a.upper    = signals.getSignalHead("E RP Sem")
a.lower    = signals.getSignalHead("E RP Sem L")
a.blocks   = [sensors.getSensor("Quartz")]
a.turnouts = []
a.next     = signals.getSignalHead("W Powder Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W Redcliff Sem")
a.upper    = signals.getSignalHead("W Redcliff Sem")
a.lower    = signals.getSignalHead("W Redcliff Sem L")
a.blocks   = [sensors.getSensor("Redcliff main")]
a.turnouts = [turnouts.getTurnout("Redcliff W"), turnouts.getTurnout("Redcliff E"), turnouts.getTurnout("Staging")]
a.next     = signals.getSignalHead("E RP Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W R-S Sem")
a.upper    = signals.getSignalHead("W R-S Sem")
a.lower    = signals.getSignalHead("W R-S Sem L")
a.blocks   = [sensors.getSensor("R-S")]
a.turnouts = []
a.next     = signals.getSignalHead("W Redcliff Sem")
a.start()


# ###### East to West ######

a = ControlDualSemaphore()
a.setName("E Sierra Sem")
a.upper    = signals.getSignalHead("E Sierra Sem")
a.lower    = signals.getSignalHead("E Sierra Sem L")
a.blocks   = [sensors.getSensor("Sierra main")]
a.turnouts = [turnouts.getTurnout("Sierra W"), turnouts.getTurnout("Sierra E")]
a.next     = signals.getSignalHead("E S-T")
a.start()

a = ControlDualSemaphore()
a.setName("E RS Sem")
a.upper    = signals.getSignalHead("E RS Sem")
a.lower    = signals.getSignalHead("E RS Sem L")
a.blocks   = [sensors.getSensor("R-S")]
a.turnouts = []
a.next     = signals.getSignalHead("E Sierra Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Redcliff Sem")
a.upper    = signals.getSignalHead("E Redcliff Sem")
a.lower    = signals.getSignalHead("E Redcliff Sem L")
a.blocks   = [sensors.getSensor("Redcliff main")]
a.turnouts = [turnouts.getTurnout("Redcliff W"), turnouts.getTurnout("Redcliff E"), turnouts.getTurnout("Staging")]
a.next     = signals.getSignalHead("E RS Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Quartz Sem")
a.upper    = signals.getSignalHead("E Quartz Sem")
a.lower    = signals.getSignalHead("E Quartz Sem L")
a.blocks   = [sensors.getSensor("Quartz")]
a.turnouts = []
a.next     = signals.getSignalHead("E Redcliff Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Powder Sem")
a.upper    = signals.getSignalHead("E Powder Sem")
a.lower    = signals.getSignalHead("E Powder Sem L")
a.blocks   = [sensors.getSensor("Powderhorn main")]
a.turnouts = [turnouts.getTurnout("Powderhorn W"), turnouts.getTurnout("Powderhorn E"), turnouts.getTurnout("Powderhorn house"), turnouts.getTurnout("Powderhorn pocket"), turnouts.getTurnout("Powderhorn crossover")]
a.next     = signals.getSignalHead("E Quartz Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E OP Sem")
a.upper    = signals.getSignalHead("E OP Sem")
a.lower    = signals.getSignalHead("E OP Sem L")
a.blocks   = [sensors.getSensor("O-P")]
a.turnouts = [turnouts.getTurnout("McSweeney")]
a.next     = signals.getSignalHead("E Powder Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Osage Sem")
a.upper    = signals.getSignalHead("E Osage Sem")
a.lower    = signals.getSignalHead("E Osage Sem L")
a.blocks   = [sensors.getSensor("Osage main"), sensors.getSensor("Osage approach")]
a.turnouts = [turnouts.getTurnout("Osage W"), turnouts.getTurnout("Osage crossover"), turnouts.getTurnout("Osage pocket")]
a.next     = signals.getSignalHead("E OP Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E UN Sem")
a.upper    = signals.getSignalHead("E UN Sem")
a.lower    = signals.getSignalHead("E UN Sem L")
a.blocks   = [sensors.getSensor("Narrows Upper")]
a.turnouts = []
a.next     = signals.getSignalHead("E Osage Sem")
a.start()

