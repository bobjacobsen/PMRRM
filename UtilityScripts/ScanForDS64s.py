# This scans the LocoNet for DS64s.
#
# This script assumes the default ops-mode programmer is configured in Preferences
# to be the LocoNet programmer.
#
# Before running the script, open the Script Output window.
#
# The script will quit after scanning all 256 addresses.
#
# Change `testCV` to scan for other types of Digitrax boards
#
# Requires JMRI 5.17.2 or later
#
# By Bob Jacobsen 2026 for the PMRRM

import jmri

global testCV
testCV = "115.01" # 115 is DS64 type; 112 is PM4x; 113 is BDL16x; 114 is SE8c

class Listener (jmri.ProgListener) :
    def programmingOpReply(self, value, status) :
        global ds64Number
        global testCV
        if status == 0 :
            print "***** DS64 found at ", ds64Number
        else :
            print "No DS64 at", ds64Number
        
        if ds64Number >= 256 : 
            print "Scan complete"
            return
        
        ds64Number = ds64Number+1
        programmer = jmri.InstanceManager.getDefault(jmri.AddressedProgrammerManager).getAddressedProgrammer(True, ds64Number)
        programmer.setMode(jmri.jmrix.loconet.LnProgrammerManager.LOCONETBDOPSWMODE)
        programmer.readCV(testCV, Listener())  # 115 is DS64 type

global ds64Number
ds64Number = 1

programmer = jmri.InstanceManager.getDefault(jmri.AddressedProgrammerManager).getAddressedProgrammer(True, ds64Number)
programmer.setMode(jmri.jmrix.loconet.LnProgrammerManager.LOCONETBDOPSWMODE)
programmer.readCV(testCV, Listener())  

        