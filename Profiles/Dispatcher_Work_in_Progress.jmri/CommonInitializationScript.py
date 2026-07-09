# CommonInitializationScript.py
#
# Runs all the initialization scripts for the 
# Dispatcher computer operation.
#
# This remains here for migration purposes.  Profiles
# should be migrated to using (as appropriate) the
# BasicInitializationScript.py and DispatcherInitializationScript.py 
# scripts directly.
#
# Does _not_ load any panel files nor invoke any actions (e.g.
# start servers, run routes, etc)
#
# April 2026

import java
import jmri
import org.slf4j.LoggerFactory

def runscript(name) :
    import org.slf4j.LoggerFactory
    org.slf4j.LoggerFactory.getLogger("script.CommonInitializationScript").info("Run script "+name)
    execfile(jmri.util.FileUtil.getExternalFilename(name))

runscript("preference:BasicInitializationScript.py")
runscript("preference:DispatcherInitializationScript.py")
