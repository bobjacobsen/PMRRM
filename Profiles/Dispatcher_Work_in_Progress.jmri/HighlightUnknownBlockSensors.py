# a script for the PMRRM to convert change the color on LayoutBlocks whose
# sensor is in the Unknown state.  Only checks when run, i.e. at startup.
#
# Bob Jacobsen    2025

import java
import jmri
from javax.swing import JOptionPane

class ResetBlockColorListener(java.beans.PropertyChangeListener):
  def set(self, sensor, block) :
    self.sensor = sensor
    self.block = block
    self.savedColor = block.getBlockTrackColor()
    return
  def propertyChange(self, event):
    if self.sensor.getKnownState() == UNKNOWN :
        self.block.setBlockTrackColor(java.awt.Color(190, 190, 255))
    else :
        self.block.setBlockTrackColor(self.savedColor)
        self.sensor.removePropertyChangeListener(self)
    return


blockManager = jmri.InstanceManager.getDefault(jmri.jmrit.display.layoutEditor.LayoutBlockManager)
foundSome = False

for sensor in sensors.getNamedBeanSet():
    if sensor.getKnownState() == UNKNOWN :
        block = blockManager.getBlockWithSensorAssigned(sensor)
        if block != None :
            # have to deal with this one
            foundSome = True
            print ("Found sensor in UNKNOWN state:", sensor, "for layout block:", block)
            listener = ResetBlockColorListener()
            listener.set(sensor, block)
            sensor.addPropertyChangeListener(listener)
            listener.propertyChange(None)
            
# if foundSome :
#    JOptionPane.showMessageDialog(None,"Light blue lines are occupancy sensors that didn't report status","Some sensor states unknown",JOptionPane.INFORMATION_MESSAGE)
            
    