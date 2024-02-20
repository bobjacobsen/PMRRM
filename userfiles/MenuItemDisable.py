# Disable some specific menus at startup time

import jmri
frame = jmri.util.JmriJFrame.getFrame("PanelPro")

# disable slot monitor
frame.getMenuBar().getMenu(6).getItem(1).disable()
# disable configure command station
frame.getMenuBar().getMenu(6).getItem(9).disable()

# disable WiThrottle Server start
frame.getMenuBar().getMenu(2).getItem(2).getItem(9).disable()
frame.getMenuBar().getMenu(2).getItem(23).getItem(0).disable()

