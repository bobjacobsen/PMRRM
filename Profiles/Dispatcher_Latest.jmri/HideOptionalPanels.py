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
        targets = ["LCC Node Status", "Midway Yard", "PanelPro"]
        for target in targets:
            frame = jmri.util.JmriJFrame.getFrame(target)
            frame.setVisible(False)         
            self.log.info("Set the "+target+" panel invisible")

        # and set some Window menu entries disabled and windows invisible
        try :
            targets = ["Port Area", "Midway Freight", "Midway Engine Service", 
                        "Vista Area", "Doering Branch", "Troy Industrial Zone", "McSweeny Branch", "Colton Industrial Zone"]
            jmri.util.WindowMenu.setIgnoredFrames(targets)
            for target in targets :
                self.log.info("Set the {} fully panel hidden", target)
                frame = jmri.util.JmriJFrame.getFrame(target)
                if frame is not None : frame.setVisible(False) 
                else : self.log.error("Frame {} not found", target)        
                
        except AttributeError:
            self.log.error("Could not adjust JMRI Window menu, you need at least JMRI 5.15.6")

HideHiResPanel().start()
        