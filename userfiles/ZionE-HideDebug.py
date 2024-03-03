# set the debug windows invisible
#
# The can still be retrieved via the Window meny
import jmri
import javax
import java

class HideWindows(jmri.jmrit.automat.AbstractAutomaton) :
        
    def handle(self):
         
        self.waitMsec(1000)  # time for windows to appear
        
        frame = jmri.util.JmriJFrame.getFrame("Port and Branch Debug")
        frame.setVisible(False)
        
        frame = jmri.util.JmriJFrame.getFrame("Zion East Debug")
        frame.setVisible(False)
        
        return False  # just once
        

hidewindow = HideWindows()
hidewindow.name = "Hide Windows"
hidewindow.start()
