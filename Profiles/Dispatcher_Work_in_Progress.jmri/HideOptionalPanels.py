# Hides the in-progress HiRes panel

import jmri

class HideHiResPanel(jmri.jmrit.automat.AbstractAutomaton) :
    from org.slf4j import LoggerFactory
    log = LoggerFactory.getLogger(
            "script.HideOptionalPanels"
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
        targets = ["PanelPro", "LccPro", "LCC Node Status"]
        for target in targets:
            frame = jmri.util.JmriJFrame.getFrame(target)
            if frame :
                frame.setVisible(False)         
                self.log.info("Set the "+target+" panel invisible")
            else :
                self.log.info("The "+target+" panel was not found when setting hidden")

        # and set some Window menu entries disabled and windows invisible
        try :
            targets = ["Midway Yard 2",
                        "Port Area", "Midway Freight", "Midway Engine Service", 
                        "Vista Area", "Doering Branch", "Troy Industrial Zone", "McSweeny Branch", "Colton Industrial Zone"]
            jmri.util.WindowMenu.setIgnoredFrames(targets)
            for target in targets :
                frame = jmri.util.JmriJFrame.getFrame(target)
                if frame : 
                    frame.setVisible(False) 
                    self.log.info("Set the {} fully panel hidden", target)
                else : self.log.error("Frame {} not found", target)        
                
        except AttributeError:
            self.log.error("Could not adjust JMRI Window menu, you need at least JMRI 5.15.6")

a = HideHiResPanel()
a.setName("HideOptionalPanels")
a.start()
        