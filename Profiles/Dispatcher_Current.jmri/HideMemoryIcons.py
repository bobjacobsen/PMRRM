# HideMemoryIcons.py
#
# This hides all the memory icons on the layout editor panel(s)
# by removing their border
# It's used to simplify a panel by removing the memory icon boxes
#
# Bob Jacobsen  2025

import java
import javax
import jmri

panelMenu = jmri.InstanceManager.getDefault(jmri.jmrit.display.EditorManager)
layoutPanels = panelMenu.getList(jmri.jmrit.display.layoutEditor.LayoutEditor)
for layoutEditor in layoutPanels :
    for memoryIcon in layoutEditor.getMemoryLabelList() :
        memoryIcon.setBorder(javax.swing.BorderFactory.createEmptyBorder())
        popupUtil = memoryIcon.getPopupUtility()
        popupUtil.setBorderSize(0)
        popupUtil.setBorderColor(layoutEditor.getBackgroundColor()) # makes it invisible
        popupUtil.setBorder(False)
    layoutEditor.repaint()
