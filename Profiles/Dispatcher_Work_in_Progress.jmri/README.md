
# Background Information on this JMRI Profile #

This is a profile for the PMRRM dispatcher system.

## Startup ##

At startup, JMRI processes several files:

 - DispatcherDefault.xml  - Main Layout Editor panel which defines and displays the layout items.
 - CommonInitializationScript.py - This is a single script to invoke all other startup scripts.  This lets us centralize that list of files across multiple profiles.
    - HideMemoryIcons.py - Hides the memory icons used to display LocoNet turnout numbers
    - DontListenDoubleHead.py - Prevent DoubleTurnoutSignalHead objects from listening to external changes
    - PMRRM_searchlights.py - Controls searchlight signals from Sierra to Whiskey.
    - PMRRM_semaphores.py - Controls semaphore signals from Narrows to Sierra.
    - MenuItemDisable.py - Disable certain items on the main menu to prevent their use when running under the `dispatcher` account.  See comments in the script for which ones.
    - HighlightUnknownBlockSensors.py - after a delay, any blocks with UNKNOWN sensor status are set to light blue
    - MaintainFileHistory.py - What it says on the tin, to reduce Git conflicts
    - QueryLnSensorState.py - redoes the initial query of sensor states after a delay in an attempt to clear blue-set blocks
    - LnSignalsToLCC.py - echos some CTC (LCC) signals to loconet for inclusion in ABS signal logic
    - HideHiResPanel.py - hides multiple panels, some transiently and some permanently
    - SignalMastIconsLit.py - start with all CTC (LCC) signal masts lit
    - ChangeDefaultBackupFileName.py - customize file names from LCC backups for ease of use with Git
 
It also
 - Starts the JMRI web server to display on the secondary screens.
 - Sets the "compare files on shutdown" option to "no"
 
Note that when working on the panel, you might want to _temporarily_ turn off the "don't compare files on shutdown" option.  Don't commit that change!

When configuring the LCC connection, select protocol settings:

 - User Name: Dispatcher JMRI

When configuring the LocoNet connection, select additional connection settings:

 - Interrogate Sensors/Turnouts On Start: Yes
 - Expanded Protocol (XP Slots): Auto Detect
 - Packetizer type: Normal (recommended)
 - Transponding present: No
 - Turnout command handling: Spread


