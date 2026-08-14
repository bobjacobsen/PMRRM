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
    log = org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.MenuItemDisable"
    	    )

    bar = frame.getJMenuBar()
    if bar is None:
        log.error("No menu bar on frame")
        return None
    for i in range(0,bar.getMenuCount()-1) :
        menu = bar.getMenu(i)
	if menu == None :
		log.debug("Found menu {} None", i)
		continue
        if menuName == menu.getLabel() : 
		log.debug("found menu {}", menuName)
		return menu
    log.error("Did not find menu {}", menuName)
    return None # error

def findItem(menu, itemName) :
    log = org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.MenuItemDisable"
    	    )
    for i in range(0, menu.getItemCount()) :
        item = menu.getItem(i)
	if item == None :
		log.debug("Found menu item {} None", i)
		continue
        if itemName == item.getLabel() : 
		log.debug("found item {}", itemName)
		return item
    log.error("Did not find item {}", itemName)
    return None # error

# this includes a delay to make sure the window is created if run during startup
class MenuItemDisable(jmri.jmrit.automat.AbstractAutomaton) :
    log = org.slf4j.LoggerFactory.getLogger(
            "jmri.jmrit.jython.exec.script.MenuItemDisable"
        )
        
    def handle(self):
        self.waitMsec(8000)

        thisUser = java.lang.System.getProperty("user.name").lower()
        # thisUser = "dispatch"  # here for debugging, comment out for normal operation
        desiredUser = "dispatch"
        if thisUser != desiredUser:
            self.log.info("Skip disabling menu items because user '{}' is not '{}'", thisUser, desiredUser)
            return False # done early
            
        # start with the PanelPro window

        # find the frame containing the menus to disable
        frame = jmri.util.JmriJFrame.getFrame("PanelPro")

        fileMenu = findMenu(frame, "File")      
	#fileMenu.setEnabled(False)
        
        if fileMenu is not None:

            # Find items within that menu and disable it
            item = findItem(fileMenu, "Load table content and panels...")
            item.setEnabled(False)

            item = findItem(fileMenu, "Store ALL table content and panels...")
            item.setEnabled(False)

        else :
            self.log.warn("Did not find File menu")
            
        toolsMenu = findMenu(frame, "Tools")

        if toolsMenu is not None:
      
            # Leave the WiThrottle Server items enabled

            # need to go down one extra level for these next
            servers = findItem(toolsMenu, "Servers")
            startWiThrottle = findItem(servers, "Start WiThrottle Server")
            startWiThrottle.setEnabled(False)
        
            throttles = findItem(toolsMenu, "Throttles")
            startWiThrottle = findItem(throttles, "Start WiThrottle Server")
            startWiThrottle.setEnabled(False)
            
        else :
            self.log.warn("Did not find Tools menu")
        

        rosterMenu = findMenu(frame, "Roster")      
        rosterMenu.setEnabled(False)
        
        panelMenu = findMenu(frame, "Panels")      
        panelMenu.setEnabled(False)
        
        scriptMenu = findMenu(frame, "Scripting")      
        scriptMenu.setEnabled(False)
        
        # find the LocoNet menu in the menu bar
        loconetMenu = findMenu(frame, "LocoNet")
        if loconetMenu is not None: # skip if run on some other connection
           
            # Find items within that menu and disable it
            monitorSlots = findItem(loconetMenu, "Monitor Slots")
            monitorSlots.setEnabled(False)
            
            configure = findItem(loconetMenu, "Configure BDL16/BDL162/BDL168")
            configure.setEnabled(False)
            
            configure = findItem(loconetMenu, "Configure PM4/PM42")
            configure.setEnabled(False)
            
            configure = findItem(loconetMenu, "Configure SE8C")
            configure.setEnabled(False)
            
            configure = findItem(loconetMenu, "Configure DS64")
            configure.setEnabled(False)
            
            configure = findItem(loconetMenu, "Configure Command Station")
            configure.setEnabled(False)
            
            configure = findItem(loconetMenu, "Configure LocoNet ID")
            configure.setEnabled(False)
            
            configure = findItem(loconetMenu, "Configure Duplex Group")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Manage LocoIO (LNSV1) Modules")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Manage LNCV Modules")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Send Throttle Messages")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Send LocoNet Packet")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Select PR3 Mode")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Download Firmware")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Download Sounds")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "Edit SPJ Sound File")
            configure.setEnabled(False)

            configure = findItem(loconetMenu, "LocoNet over TCP Server")
            configure.setEnabled(False)

        else :
            self.log.warn("Did not find LocoNet menu")
            
        # find the LCC menu in the menu bar
        lccMenu = findMenu(frame, "LCC")
        if lccMenu is not None: # skip if run on some other connection
            lccMenu.setEnabled(False)

        debugMenu = findMenu(frame, "Debug")  
        if debugMenu is not None :    
            debugMenu.setEnabled(False)
        else :
            self.log.warn("Did not find Debug menu")
        

        # Now proceed to the Layout Editor "Dispatcher" window
        frame = jmri.util.JmriJFrame.getFrame("PMRRM Dispatcher")
        
        if frame is not None :
            fileMenu = findMenu(frame, "File")   
            if fileMenu is not None :   
                fileMenu.setEnabled(False)
            else :
                self.log.warn("Did not find Dispatcher File menu")
    
            optMenu = findMenu(frame, "Options")      
            optMenu.setEnabled(False)
            optMenu.setEnabled(False)  # defeats the accelerator cmd-E
    
            toolsMenu = findMenu(frame, "Tools")      
            toolsMenu.setEnabled(False)

        else :
            self.log.warn("Did not find PMRRM Dispatcher window")

        # Now proceed to the Layout Editor "Dispatcher HiRes" window
        frame = jmri.util.JmriJFrame.getFrame("PMRRM Dispatcher HiRes")
        
        if frame != None :
            fileMenu = findMenu(frame, "File")      
            if fileMenu is not None :   
                fileMenu.setEnabled(False)
            else :
                self.log.warn("Did not find Dispatcher HiRes File menu")
    
            optMenu = findMenu(frame, "Options")      
            optMenu.setEnabled(False)  # also defeats the accelerator cmd-E
    
            toolsMenu = findMenu(frame, "Tools")      
            toolsMenu.setEnabled(False)

        else :
            self.log.warn("Did not find PMRRM Dispatcher HiRes window")

        # Now proceed to the Panel Editor "Midway Yard" window
        frame = jmri.util.JmriJFrame.getFrame("Midway Yard")
        
        if frame != None :
            menu = findMenu(frame, "Edit")      
            if menu is not None :   
                menu.setEnabled(False)
            else :
                self.log.warn("Did not find Midway Yard Edit menu")
        else :
            self.log.warn("Did not find Midway Yard Edit window")

        # Now proceed to the Panel Editor "Midway Yard Editor" window
        frame = jmri.util.JmriJFrame.getFrame("Midway Yard Editor")
                
        if frame != None :
            menu = findMenu(frame, "File")      
            if menu is not None :   
                menu.setEnabled(False)
            else :
                self.log.warn("Did not find Midway Yard Editor File menu")
            frame.setVisible(False) # we can't disable contents of window, so we hide it for now
        else :
            self.log.warn("Did not find Midway Yard Editor window")

        # and we're done!
        self.log.info("Menu update complete")

# create one of these
a = MenuItemDisable()

# set the name, as a example of configuring it
a.setName("Some editing of the menus")

# and start it running - this will only take a short time
a.start()

