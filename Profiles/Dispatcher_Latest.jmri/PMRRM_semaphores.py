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
#
# Because of how the physical semaphores are wired, we set them to "red" here
# even though the actual appearance is yellow.
#
# We're setting two semaphores _plus_ one internal signal which is placed on the 
# PanelPro panels.

import jmri
import time
import org.slf4j

global nextdelay
nextdelay = 15000

class ControlDualSemaphore (jmri.jmrit.automat.AbstractAutomaton) :
    def current_milli_time(self):
        import time
        return int(time.time() * 1000)
        
    def init(self) :
        
        global nextdelay
        nextdelay = nextdelay+100  # stagger startup
        self.waitMsec(nextdelay)
        memories.provideMemory("IMProgramStatus").setValue("Initializing Semaphores ")
        
        self.minAcceptableTime = 200
        
        import org.slf4j.LoggerFactory
        self.log = org.slf4j.LoggerFactory.getLogger("script.PMRRM_semaphores");

        # print checks
        if self.upper == None : self.log.error("semaphore {} has null upper head", self.name)
        if self.lower == None : self.log.error("semaphore {} has null lower head", self.name)
        if None in self.blocks : 
            self.log.error("semaphore {}  has null block", self.name)
            i = 1
            for item in self.blocks :
                if item == None : self.log.error("       item {}", i)
                i = i+1
        if None in self.turnouts : 
            self.log.error("semaphore {}  has null turnout", self.name)
            i = 1
            for item in self.blocks :
                if item == None : self.log.error("        item {}", i)
                i = i+1

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
        
        return
        
    def handle(self) :
        # this defers to immediately run on Layout Thread

        # check for running too quickly
        delta = self.current_milli_time() - self.lastTime 
        if delta < self.minAcceptableTime :
            # ran abnormally quickly
            self.log.debug("Semaphore logic {} ran in {} msec", self.getName(), delta)
            self.log.debug("prior time {}", str(self.priorBeans))
            self.log.debug("last time  {}", str(self.lastBeans))
            beansNow = []
            for bean in self.beans:
                beansNow.append(bean.describeState(bean.state))
            self.log.debug("     now   {}", str(beansNow))
            
        self.lastTime = self.current_milli_time()
        self.priorBeans = self.lastBeans
        self.lastBeans = []
        for bean in self.beans:
            self.lastBeans.append(bean.describeState(bean.state))
        
        class workOnLayout(jmri.util.ThreadingUtil.ThreadAction):
            def __init__(self, blocks, turnouts, upper, lower, display, next):
                self.blocks = blocks
                self.turnouts = turnouts
                self.upper = upper
                self.lower = lower
                self.display = display
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
        
                if lower != self.lower.getAppearance() :
                    self.lower.setAppearance(lower)
        
                if lower == RED and upper == GREEN : self.display.setAppearance(YELLOW)
                elif upper == GREEN : self.display.setAppearance(GREEN)
                else : self.display.setAppearance(RED)
                
        # invoke on layout thread
        jmri.util.ThreadingUtil.runOnLayout(workOnLayout(self.blocks, self.turnouts, self.upper, self.lower, self.display, self.next))

        self.waitChange(self.beans, 4000)  # run again when something changes or after a delay (just in case)?
        
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
a.display  = signals.getSignalHead("W LN Sem Display")
a.next     = False
a.start()

a = ControlDualSemaphore()
a.setName("W UN Sem")
a.upper    = signals.getSignalHead("W UN Sem")
a.lower    = signals.getSignalHead("W UN Sem L")
a.blocks   = [sensors.getSensor("Narrows Upper")]
a.turnouts = []
a.display  = signals.getSignalHead("W UN Sem Display")
a.next     = signals.getSignalHead("W LN Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W Osage Sem")
a.upper    = signals.getSignalHead("W Osage Sem")
a.lower    = signals.getSignalHead("W Osage Sem L")
a.blocks   = [sensors.getSensor("Osage main"), sensors.getSensor("Osage approach")]
a.turnouts = [turnouts.getTurnout("Osage W"), turnouts.getTurnout("Osage E"), turnouts.getTurnout("Osage pocket E")]
a.display  = signals.getSignalHead("W Osage Sem Display")
a.next     = signals.getSignalHead("W UN Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W OP Sem")
a.upper    = signals.getSignalHead("W OP Sem")
a.lower    = signals.getSignalHead("W OP Sem L")
a.blocks   = [sensors.getSensor("Osage-Powderhorn")]
a.turnouts = [turnouts.getTurnout("McSweeney branch")]
a.display  = signals.getSignalHead("W OP Sem Display")
a.next     = signals.getSignalHead("W Osage Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W Powder Sem")
a.upper    = signals.getSignalHead("W Powder Sem")
a.lower    = signals.getSignalHead("W Powder Sem L")
a.blocks   = [sensors.getSensor("Powderhorn main")]
a.turnouts = [turnouts.getTurnout("Powderhorn W"), turnouts.getTurnout("Powderhorn E"), turnouts.getTurnout("Powderhorn housetrack"), turnouts.getTurnout("Powderhorn pocket"), turnouts.getTurnout("Powderhorn crossover main")]
a.display  = signals.getSignalHead("W Powder Sem Display")
a.next     = signals.getSignalHead("W OP Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E RP Sem")
a.upper    = signals.getSignalHead("E RP Sem")
a.lower    = signals.getSignalHead("E RP Sem L")
a.blocks   = [sensors.getSensor("Quartz")]
a.turnouts = []
a.display  = signals.getSignalHead("E RP Sem Display")
a.next     = signals.getSignalHead("W Powder Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W Redcliff Sem")
a.upper    = signals.getSignalHead("W Redcliff Sem")
a.lower    = signals.getSignalHead("W Redcliff Sem L")
a.blocks   = [sensors.getSensor("Redcliff main")]
a.turnouts = [turnouts.getTurnout("Redcliff W"), turnouts.getTurnout("Redcliff E"), turnouts.getTurnout("Redcliff Staging")]
a.display  = signals.getSignalHead("W Redcliff Sem Display")
a.next     = signals.getSignalHead("E RP Sem")
a.start()

a = ControlDualSemaphore()
a.setName("W R-S Sem")
a.upper    = signals.getSignalHead("W R-S Sem")
a.lower    = signals.getSignalHead("W R-S Sem L")
a.blocks   = [sensors.getSensor("Redcliff-Sierra")]
a.turnouts = []
a.display  = signals.getSignalHead("W R-S Sem Display")
a.next     = signals.getSignalHead("W Redcliff Sem")
a.start()


# ###### East to West ######

a = ControlDualSemaphore()
a.setName("E Sierra Sem")
a.upper    = signals.getSignalHead("E Sierra Sem")
a.lower    = signals.getSignalHead("E Sierra Sem L")
a.blocks   = [sensors.getSensor("Sierra main")]
a.turnouts = [turnouts.getTurnout("Sierra W"), turnouts.getTurnout("Sierra E")]
a.display  = signals.getSignalHead("E Sierra Sem Display")
a.next     = signals.getSignalHead("E S-T")
a.start()

a = ControlDualSemaphore()
a.setName("E RS Sem")
a.upper    = signals.getSignalHead("E RS Sem")
a.lower    = signals.getSignalHead("E RS Sem L")
a.blocks   = [sensors.getSensor("Redcliff-Sierra")]
a.turnouts = []
a.display  = signals.getSignalHead("E RS Sem Display")
a.next     = signals.getSignalHead("E Sierra Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Redcliff Sem")
a.upper    = signals.getSignalHead("E Redcliff Sem")
a.lower    = signals.getSignalHead("E Redcliff Sem L")
a.blocks   = [sensors.getSensor("Redcliff main")]
a.turnouts = [turnouts.getTurnout("Redcliff W"), turnouts.getTurnout("Redcliff E"), turnouts.getTurnout("Redcliff Staging")]
a.display  = signals.getSignalHead("E Redcliff Sem Display")
a.next     = signals.getSignalHead("E RS Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Quartz Sem")
a.upper    = signals.getSignalHead("E Quartz Sem")
a.lower    = signals.getSignalHead("E Quartz Sem L")
a.blocks   = [sensors.getSensor("Quartz")]
a.turnouts = []
a.display  = signals.getSignalHead("E Quartz Sem Display")
a.next     = signals.getSignalHead("E Redcliff Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Powder Sem")
a.upper    = signals.getSignalHead("E Powder Sem")
a.lower    = signals.getSignalHead("E Powder Sem L")
a.blocks   = [sensors.getSensor("Powderhorn main")]
a.turnouts = [turnouts.getTurnout("Powderhorn W"), turnouts.getTurnout("Powderhorn E"), turnouts.getTurnout("Powderhorn housetrack"), turnouts.getTurnout("Powderhorn pocket"), turnouts.getTurnout("Powderhorn crossover main")]
a.display  = signals.getSignalHead("E Powder Sem Display")
a.next     = signals.getSignalHead("E Quartz Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E OP Sem")
a.upper    = signals.getSignalHead("E OP Sem")
a.lower    = signals.getSignalHead("E OP Sem L")
a.blocks   = [sensors.getSensor("Osage-Powderhorn")]
a.turnouts = [turnouts.getTurnout("McSweeney branch")]
a.display  = signals.getSignalHead("E OP Sem Display")
a.next     = signals.getSignalHead("E Powder Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E Osage Sem")
a.upper    = signals.getSignalHead("E Osage Sem")
a.lower    = signals.getSignalHead("E Osage Sem L")
a.blocks   = [sensors.getSensor("Osage main"), sensors.getSensor("Osage approach")]
a.turnouts = [turnouts.getTurnout("Osage W"), turnouts.getTurnout("Osage E"), turnouts.getTurnout("Osage pocket E")]
a.display  = signals.getSignalHead("E Osage Sem Display")
a.next     = signals.getSignalHead("E OP Sem")
a.start()

a = ControlDualSemaphore()
a.setName("E UN Sem")
a.upper    = signals.getSignalHead("E UN Sem")
a.lower    = signals.getSignalHead("E UN Sem L")
a.blocks   = [sensors.getSensor("Narrows Upper")]
a.turnouts = []
a.display  = signals.getSignalHead("E UN Sem Display")
a.next     = signals.getSignalHead("E Osage Sem")
a.start()

