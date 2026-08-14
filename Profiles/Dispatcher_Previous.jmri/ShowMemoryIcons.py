# ShowMemoryIcons.py
#
# This shows all the memory icons on the layout editor panel(s)
# by setting their border visible
# It's used to simplify a panel by showing the memory icon boxes on command.
# Only memory icons that don't have a "$" in their system name are highlighted
#
# Bob Jacobsen  2025

import java
import javax
import jmri

panelMenu = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)
layoutPanels = panelMenu.getList(jmri.jmrit.display.layoutEditor.LayoutEditor)
for layoutEditor in layoutPanels :
    for memoryIcon in layoutEditor.getMemoryLabelList() :
        if memoryIcon.getMemory() != None and not "$" in memoryIcon.getMemory().getSystemName():
            popupUtil = memoryIcon.getPopupUtility()
            popupUtil.setBorderColor(java.awt.Color.yellow)
            popupUtil.setBorderSize(1)
            popupUtil.setBorder(True)
            memoryIcon.setBorder(javax.swing.BorderFactory.createLineBorder(java.awt.Color.yellow))
    layoutEditor.repaint()
