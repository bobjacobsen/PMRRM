# a script for the PMRRM to convert the Dispatcher Complex profile into
# the desired Dispatcher Simple configuration
#
# Bob Jacobsen    2025

import java
import jmri

panelMenu = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)
layoutPanels = panelMenu.getList(jmri.jmrit.display.layoutEditor.LayoutEditor)
for layoutEditor in layoutPanels :
    # disable and hide the "yellow dot" sensor icons
    for p in layoutEditor.getSensorList() :
        if p.getSensor().getUserName().startswith("NX") :
            p.setVisible(False)
            p.setControlling(False)

    # re-enable the Xerox E turnout icon
    for p in layoutEditor.getLayoutTurnouts() :
        if p.getTurnoutName() == "Xerox E" :
            p.setDisabled(False)
