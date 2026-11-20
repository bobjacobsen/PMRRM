# LnSignalsToLCC
#
# This copies the Stop/Not-Stopped status of a LocoNet-resident
# signal mast to a LocoNet Turnout which can be used (via a gateway)
# by LCC-resident signal mast logic.
#
# Written for the PMRRM - Bob  Jacobsen 2026

import java
import jmri
import org.slf4j.LoggerFactory as LoggerFactory

class LnSignalsToLCC(java.beans.PropertyChangeListener):
  def set(self, signalHeadName, turnoutSystemName, turnoutUserName) :
    self.signalHeadName = signalHeadName
    self.signal = signals.getSignalHead(signalHeadName)
    self.turnoutSystemName = turnoutSystemName
    self.turnoutUserName = turnoutUserName
    self.turnout = turnouts.provideTurnout(turnoutSystemName)
    self.turnout.setUserName(turnoutUserName)
    
    self.signal.addPropertyChangeListener(self)
  
  # will run on layout thread
  def propertyChange(self, event):
    if event.propertyName == "Appearance" :
        if event.newValue == RED :
            self.turnout.setCommandedState(THROWN)
        else :
            self.turnout.setCommandedState(CLOSED)
    
LnSignalsToLCC().set("W Xerox Main",   "LT1201", "W Xerox Main is at Stop")
LnSignalsToLCC().set("W Xerox Siding", "LT1202", "W Xerox Siding is at Stop")

LnSignalsToLCC().set("E UN Sem",       "LT1203", "E UN Sem is at Stop")
