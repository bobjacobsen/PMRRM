# BasicInitializationScript.py
#
# Runs the initialization scripts used across all
# related profiles, e.g. the setup for basic operation.
# Does not include any scripts that control railroad operations.
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

runscript("preference:MaintainFileHistory.py")
runscript("preference:ChangeDefaultBackupFileName.py")
runscript("preference:WatchNodesAndDisplay.py")
