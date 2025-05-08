# Disable some specific menus at startup time.
#
# This might be useful if e.g. you're letting general users access the menus
#
# There are reports of it not working on Windows. These are
# not understood - it seems that some windows on Windows don't have 
# an accessible menu bar

import jmri
import org.slf4j.Logger
import org.slf4j.LoggerFactory

def findMenu(frame, menuName) :
    bar = frame.getMenuBar()
    if bar is None:
        org.slf4j.LoggerFactory.getLogger(
                "jmri.jmrit.jython.exec.script.MenuItemDisable"
        ).error("No menu bar on frame")
        return None
    for i in range(0,bar.getMenuCount()-1) :
        menu = bar.getMenu(i)
        if menuName == menu.getLabel() : return menu
    org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.MenuItemDisable"
    ).error("Did not find menu {}", menuName)
    return None # error

def findItem(menu, itemName) :
    for i in range(0, menu.getItemCount()) :
        item = menu.getItem(i)
        if itemName == item.getLabel() : return item
    org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.MenuItemDisable"
    ).error("Did not find item {}", itemName)
    return None # error

# this includes a delay to make sure the window is created if run during startup
class MenuItemDisable(jmri.jmrit.automat.AbstractAutomaton) :
    def handle(self):
        self.waitMsec(8000)

        # start with the PanelPro window
        
        # find the frame containing the menus to disable
        frame = jmri.util.JmriJFrame.getFrame("PanelPro")
        
        fileMenu = findMenu(frame, "File")      
        #fileMenu.disable()
        
        if fileMenu is not None:

            # Find items within that menu and disable it
            item = findItem(fileMenu, "Load table content and panels...")
            item.disable()

            item = findItem(fileMenu, "Store ALL table content and panels...")
            item.disable()

        else :
            print "Did not find File menu"
            
        toolsMenu = findMenu(frame, "Tools")

        if toolsMenu is not None:
        
            # need to go down one extra level for these next
            servers = findItem(toolsMenu, "Servers")
            startWiThrottle = findItem(servers, "Start WiThrottle Server")
            startWiThrottle.disable()
        
            throttles = findItem(toolsMenu, "Throttles")
            startWiThrottle = findItem(throttles, "Start WiThrottle Server")
            startWiThrottle.disable()
            
        else :
            print "Did not find Tools menu"
        

        rosterMenu = findMenu(frame, "Roster")      
        rosterMenu.disable()
        
        panelMenu = findMenu(frame, "Panels")      
        panelMenu.disable()
        
        scriptMenu = findMenu(frame, "Scripting")      
        scriptMenu.disable()
        
        # find the menu in the menu bar
        loconetMenu = findMenu(frame, "LocoNet")
        if loconetMenu is not None: # skip if run on some other connection
           
            # Find items within that menu and disable it
            monitorSlots = findItem(loconetMenu, "Monitor Slots")
            monitorSlots.disable()
            
            configure = findItem(loconetMenu, "Configure BDL16/BDL162/BDL168")
            configure.disable()
            
            configure = findItem(loconetMenu, "Configure PM4/PM42")
            configure.disable()
            
            configure = findItem(loconetMenu, "Configure SE8C")
            configure.disable()
            
            configure = findItem(loconetMenu, "Configure DS64")
            configure.disable()
            
            configure = findItem(loconetMenu, "Configure Command Station")
            configure.disable()
            
            configure = findItem(loconetMenu, "Configure LocoNet ID")
            configure.disable()
            
            configure = findItem(loconetMenu, "Configure Duplex Group")
            configure.disable()

            configure = findItem(loconetMenu, "Manage LocoIO (LNSV1) Modules")
            configure.disable()

            configure = findItem(loconetMenu, "Manage LNCV Modules")
            configure.disable()

            configure = findItem(loconetMenu, "Send Throttle Messages")
            configure.disable()

            configure = findItem(loconetMenu, "Send LocoNet Packet")
            configure.disable()

            configure = findItem(loconetMenu, "Select PR3 Mode")
            configure.disable()

            configure = findItem(loconetMenu, "Download Firmware")
            configure.disable()

            configure = findItem(loconetMenu, "Download Sounds")
            configure.disable()

            configure = findItem(loconetMenu, "Edit SPJ Sound File")
            configure.disable()

            configure = findItem(loconetMenu, "LocoNet over TCP Server")
            configure.disable()

        else :
            print "Did not find LocoNet menu"
            
        debugMenu = findMenu(frame, "Debug")      
        debugMenu.disable()
        

        # Now proceed to the Layout Editor "Dispatcher" window
        frame = jmri.util.JmriJFrame.getFrame("PMRRM Dispatcher")
        
        fileMenu = findMenu(frame, "File")      
        fileMenu.disable()

        optMenu = findMenu(frame, "Options")      
        optMenu.disable()
        optMenu.setEnabled(False)  # defeats the accelerator cmd-E

        toolsMenu = findMenu(frame, "Tools")      
        toolsMenu.disable()

        org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.MenuItemDisable"
        ).info("Menu update complete")

# create one of these
a = MenuItemDisable()

# set the name, as a example of configuring it
a.setName("Some editing of the menus")

# and start it running - this will only take a short time
a.start()

