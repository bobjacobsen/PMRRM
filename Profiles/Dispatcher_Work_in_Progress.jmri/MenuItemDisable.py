# Disable some specific menus at startup time.
#
# This might be useful if e.g. you're letting general users access the menus
#
# There are reports of it not working on Windows. These are
# not understood - it seems that some windows on Windows don't have 
# an accessible menu bar

import jmri

def findMenu(frame, menuName) :
    bar = frame.getMenuBar()
    if bar is None:
        print "No menu bar on frame"
        return None
    for i in range(0,bar.getMenuCount()-1) :
        menu = bar.getMenu(i)
        if menuName == menu.getLabel() : return menu
    print "Did not find menu", menuName
    return None # error

def findItem(menu, itemName) :
    for i in range(0, menu.getItemCount()) :
        item = menu.getItem(i)
        if itemName == item.getLabel() : return item
    print "Did not find item", itemName
    return None # error

# this includes a delay to make sure the window is created if run during startup
class MenuItemDisable(jmri.jmrit.automat.AbstractAutomaton) :
    # handle() is called repeatedly until it returns false.
    def handle(self):
        self.waitMsec(8000)

        # start with the PanelPro window
        
        # find the frame containing the menus to disable
        frame = jmri.util.JmriJFrame.getFrame("PanelPro")
        
        fileMenu = findMenu(frame, "File")      
        fileMenu.disable()
        
        rosterMenu = findMenu(frame, "Roster")      
        rosterMenu.disable()
        
        panelMenu = findMenu(frame, "Panels")      
        panelMenu.disable()
        
        scriptMenu = findMenu(frame, "Scripting")      
        scriptMenu.disable()
        
        debugMenu = findMenu(frame, "Debug")      
        debugMenu.disable()
        
        # find the menu in the menu bar
        loconetMenu = findMenu(frame, "LocoNet")
        
        if loconetMenu is not None: # skip if run on some other connection
           
            # Find an item within that menu and disable it
            monitorSlots = findItem(loconetMenu, "Monitor Slots")
            monitorSlots.disable()
            
            configureCS = findItem(loconetMenu, "Configure Command Station")
            configureCS.disable()
        else :
            print "Did not find LocoNet menu"
            
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
        

        # Now proceed to the Layout Editor "Dispatcher" window
        frame = jmri.util.JmriJFrame.getFrame("PMRRM Dispatcher")
        
        fileMenu = findMenu(frame, "File")      
        fileMenu.disable()

        optMenu = findMenu(frame, "Options")      
        optMenu.disable()

        toolsMenu = findMenu(frame, "Tools")      
        toolsMenu.disable()


# create one of these
a = MenuItemDisable()

# set the name, as a example of configuring it
a.setName("Some editing of the menus")

# and start it running - this will only take a short time
a.start()

