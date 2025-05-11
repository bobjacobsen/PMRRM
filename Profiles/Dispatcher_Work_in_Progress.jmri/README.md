
# Background Information on this JMRI Profile #

This is the development profile for the PMRRM dispatcher system.

## Startup ##

At startup, JMRI processes several files:

 - DispatcherDefault.xml  - Main Layout Editor panel which defines and displays the layout items.
 - PMRRM_searchlights.py - Controls searchlight signals from Sierra to Whiskey.
 - PMRRM_semaphores.py - Controls semaphore signals from Narrows to Sierra.
 - DontListenDoubleHead.py - Prevent DoubleTurnoutSignalHead objects from listening to external changes
 - MenuItemDisable.py - Disable certain items on the main menu to prevent their use.  See comments in the script for which ones.
 - ClearFileHistory.py - What it says on the tin, to reduce Git conflicts
 
It also
 - Starts the JMRI web server to display on the secondary screens.
 - Puts a button for opening the Block Table on the main panel. The Block Table is accessed to enter train information.
 - Sets the "don't compare files on shutdown" option
 
Note that when working on the panel, you might want to _temporarily_ disable the MenuItemDisable.py file and turn on the "don't compare files on shutdown" option.  Don't commit that change!


