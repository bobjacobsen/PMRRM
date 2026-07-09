# DispatcherInitializationScript.py
#
# Runs the initialization scripts that control
# the operation of the railroad for the Dispatcher
# computer.  (Will eventually be refactored for the 
# central computer installation)
#
# Assumes that BasicInitializationScript.py has already been run.
#
# Does _not_ load any panel files nor invoke any actions (e.g.
# start servers, run routes, etc)
#
# July 2026

import java
import jmri
import org.slf4j.LoggerFactory

def runscript(name) :
    import org.slf4j.LoggerFactory
    org.slf4j.LoggerFactory.getLogger("script.CommonInitializationScript").info("Run script "+name)
    execfile(jmri.util.FileUtil.getExternalFilename(name))

runscript("preference:HideMemoryIcons.py")
runscript("preference:DontListenDoubleHead.py")
runscript("preference:PMRRM_semaphores.py")
runscript("preference:PMRRM_searchlights.py")
runscript("preference:MenuItemDisable.py")
runscript("preference:QueryLnSensorState.py")

# commented out due to not using NX routing
# runscript("preference:ThrowTurnoutsWhenBlockAllocated.py")

runscript("preference:LnSignalsToLCC.py")
runscript("preference:HideOptionalPanels.py")
runscript("preference:SignalMastIconsLit.py")
runscript("preference:AskForLccInit.py")

