
# Background Information on this JMRI Profile #

## Startup ##

At startup, JMRI processes several files:

 - DispatcherDefault.xml  - Main Layout Editor panel which defines and displays the layout items.
 - PMRRM_searchlights.py - Controls searchlight signals from Sierra to Whiskey.
 - PMRRM_semaphores.py - Controls semaphore signals from Narrows to Sierra.
 - MenuItemDisable.py - Disable certain items on the main menu to prevent their use.  See comments in the script for which ones.
 
It also
 - Starts the JMRI web server to display on the secondary screens.
 - Puts a button for opening the Block Table on the main panel. The Block Table is accessed to enter train information.
 
