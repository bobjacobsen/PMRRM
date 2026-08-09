# Hides the in-progress HiRes panel

import jmri

class HideHiResPanel(jmri.jmrit.automat.AbstractAutomaton) :
    from org.slf4j import LoggerFactory
    log = LoggerFactory.getLogger(
            "script.HideHiResPanel"
        )
        
    def handle(self):
        self.waitMsec(4000)

        thisUser = java.lang.System.getProperty("user.name").lower()
        #thisUser = "dispatch"  # here for debugging, comment out for normal operation
        desiredUser = "dispatch"
        if thisUser != desiredUser:
            self.log.info("Skip hiding panels because user '{}' is not '{}'", thisUser, desiredUser)
            return False # done early
            
        # Now proceed to windows that are to be hidden, but left in Windows menu
        
        #frame = jmri.util.JmriJFrame.getFrame("PMRRM Dispatcher HiRes")
        #frame.setVisible(False)         
        #self.log.info("Set the HiRes panel invisible")

        frame = jmri.util.JmriJFrame.getFrame("LCC Node Status")
        frame.setVisible(False)         
        self.log.info("Set the LCC Node Status panel invisible")

        frame = jmri.util.JmriJFrame.getFrame("Midway Yard")
        frame.setVisible(False)         
        self.log.info("Set the Midway Yard panel invisible")

        frame = jmri.util.JmriJFrame.getFrame("PanelPro")
        frame.setVisible(False)         
        self.log.info("Set the main PanelPro window invisible")

        # and set some Window menu entries disabled
        try :
            targets = ["Port Area", "Midway Freight", "Midway Engine Service", "Vista", "Vista Doering Branch"]
            jmri.util.WindowMenu.setIgnoredFrames(targets)
            for target in targets :
                self.log.info("Set the {} fully panel hidden", target)
                frame = jmri.util.JmriJFrame.getFrame(target)
                if frame is not None : frame.setVisible(False) 
                else : self.log.error("Frame {} not found", target)        
                
        except AttributeError:
            self.log.error("Could not adjust JMRI Window menu, you need at least JMRI 5.15.6")

HideHiResPanel().start()
        