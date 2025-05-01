# a script for the PMRRM to suppress (make invisible and inactive) the 
# "yellow dot" sensor icons used for NX routing.
#
# Bob Jacobsen    2025

import java
import jmri

panelMenu = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)
layoutPanels = panelMenu.getList(jmri.jmrit.display.layoutEditor.LayoutEditor)
for layoutEditor in layoutPanels :
    for p in layoutEditor.getSensorList() :
        if p.getSensor().getUserName().startswith("NX") :
            p.setVisible(False)
            p.setControlling(False)
