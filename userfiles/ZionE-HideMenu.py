# Hide the menu bar main contents on the "Zion East" panel window
#
# Does not hide the system menu elements

import jmri
import javax
import java

class HideMenu(jmri.jmrit.automat.AbstractAutomaton) :
        
    def handle(self):
         
        self.waitMsec(1000)  # time for window to appear
        
        frame = jmri.util.JmriJFrame.getFrame("Zion East")
        frame.setMenuBar(None)
        
        return False  # just once
        

hidemenu = HideMenu()
hidemenu.name = "Hide Menu on Zion East"
hidemenu.start()
