# This scans the LocoNet for "LocoNet Attached Boards", e.g. the LocoNet boards
# from RR-CirKits. It's been used to find Watchman boards at the PMRRM.
#
# This script assumes the default ops-mode programmer is configured in Preferences
# to be the LocoNet programmer.
#
# Before running the script, open the LocoNet Monitor and put
# (no quotes) "B0 B1 B2 B4 BB EF" in the "Filter Bytes" field.
# Found boards will then show as lines in the LocoNet Monitor.
# (Almost) all other messages will be suppressed.
#
# You can track the progress of the script in the "Script Output" window.
#
# When you're done, you should clear the "Filter Bytes" field in the Monitor
# as it is retained from run to run of the program, then restart the program
# to end the script.
#
# By Bob Jacobsen 2026 for the PMRRM

import jmri
class Scanner (jmri.jmrit.automat.AbstractAutomaton) : 
	def init(self) :
		self.locoNumber = 11000  # change this if you want to start at other than one
	def handle(self) :
		self.locoNumber = self.locoNumber + 1
		programmer = jmri.InstanceManager.getDefault(jmri.AddressedProgrammerManager).getAddressedProgrammer(True, self.locoNumber)
		programmer.readCV("8", None)
		print self.locoNumber
		self.waitMsec(200)
		return True

Scanner().start()

