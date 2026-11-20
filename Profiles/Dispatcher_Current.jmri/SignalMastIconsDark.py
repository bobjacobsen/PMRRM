# HideSignalMastIcons.py
#
# This hides all the signal mast icons on the layout editor panel(s)
# by setting their "Lit" state to Unlit
#
# Bob Jacobsen  2025

import java
import javax
import jmri

panelMenu = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)
layoutPanels = panelMenu.getList(jmri.jmrit.display.layoutEditor.LayoutEditor)
for layoutEditor in layoutPanels :
    for signalMastIcon in layoutEditor.getSignalMastList() :
        signalMastIcon.getSignalMast().setHeld(False)
        signalMastIcon.getSignalMast().setLit(False)
    layoutEditor.repaint()
