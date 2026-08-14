# a script for the PMRRM to convert change the color on LayoutBlocks whose
# sensor is in the Unknown state.  Only checks when run, i.e. at startup,
# after a short delay.
#
# Bob Jacobsen    2025

import java
import jmri
from javax.swing import JOptionPane
import org.slf4j.Logger
import org.slf4j.LoggerFactory

# redraw all LayoutEditor panels  - should run on GUI thread
class RedrawPanels(jmri.util.ThreadingUtil.ThreadAction):
  def run(self):  
    editorManager = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)
    for panel in editorManager.getAll(jmri.jmrit.display.layoutEditor.LayoutEditor) :
        panel.redrawPanel()
    return

class ResetBlockColorListener(java.beans.PropertyChangeListener):
  def set(self, sensor, block) :
    self.sensor = sensor
    self.block = block
    self.savedColor = block.getBlockExtraColor()
    return
  
  # should run on GUI thread
  def propertyChange(self, event):
    if self.sensor.getKnownState() == UNKNOWN :
        # still unknown
        return
    else :
        self.sensor.removePropertyChangeListener(self)
        self.block.setBlockExtraColor(self.savedColor)
        self.block.setUseExtraColor(False)
    return

class HighlightUnknownBlockSensors(jmri.util.ThreadingUtil.ThreadAction) :
    
    # this will be run on the GUI thread
    def run(self):
        self.log = org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.HighlightUnknownBlockSensors"
        )

        self.log.info("Start HighlightUnknownBlockSensors")
        
        blockManager = jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
        foundSome = False
        
        for sensor in sensors.getNamedBeanSet():
            block = blockManager.getBlockWithSensorAssigned(sensor)
            if block != None :
                block.setBlockExtraColor(java.awt.Color.green) # reset in case saved  with some other color active
                if sensor.getKnownState() == UNKNOWN :
                    # have to deal with this one
                    foundSome = True
                    self.log.warn("Found sensor in UNKNOWN state: {} for layout block: {}", sensor, block)
                    listener = ResetBlockColorListener()    # saves current color
                    listener.set(sensor, block)
                    block.setBlockExtraColor(java.awt.Color(190, 190, 255)) # light blue
                    block.setUseExtraColor(True)
                    sensor.addPropertyChangeListener(listener) # listener added after changing color
                    
        if foundSome :
            # request a redraw of all LayoutEditor panels to get rapid repaint
            jmri.util.ThreadingUtil.runOnGUIEventually(RedrawPanels())
            # JOptionPane.showMessageDialog(None,"Light blue lines are occupancy sensors that didn't report status","Some sensor states unknown",JOptionPane.INFORMATION_MESSAGE)
        return
    
# and launch on GUI thread after some delay        
jmri.util.ThreadingUtil.runOnGUIDelayed(HighlightUnknownBlockSensors(), 8000)  # time related to retry script(s)
  