# HideBlueText.py
#
# This hides all the blue content on the layout editor panel(s)
# It's used to simplify a panel by removing the turnout numbers.
#
# Bob Jacobsen  2025

import java
import jmri

for memory in memories.getNamedBeanSet() :
    if memory.getSystemName().startswith("IMLABEL$") :
        memory.setValue("")

panelMenu = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)
layoutPanels = panelMenu.getList(jmri.jmrit.display.layoutEditor.LayoutEditor)
colorMatch = java.awt.Color(0,0,255)
for layoutEditor in layoutPanels :
    #for positionable in layoutEditor.getContents() :
    #    if positionable.getForeground() == colorMatch :
    #        positionable.setVisible(False)
    layoutEditor.repaint()
