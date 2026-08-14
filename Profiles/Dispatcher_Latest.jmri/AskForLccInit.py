#
# Ask for all the event IDs, similar to redoing the LCC initialization
#
# Bob Jacobsen  2026

import jmri
global AskForLccInit
class AskForLccInit (jmri.jmrit.automat.AbstractAutomaton) :

    def handle(self) :
        import jmri
        import org.openlcb
        
        self.waitMsec(30000) # wait for other initialization to end
        memories.provideMemory("IMProgramStatus").setValue("Requesting LCC data")
        
        # get node table
        olcbConfigMgr = jmri.InstanceManager.getDefault().getInstance(jmri.jmrix.openlcb.OlcbConfigurationManager)
        store = olcbConfigMgr.get(org.openlcb.MimicNodeStore)

        systemMemo = jmri.InstanceManager.getDefault(jmri.jmrix.can.CanSystemConnectionMemo)
        connection = systemMemo.get(org.openlcb.Connection)
        nid = systemMemo.get(org.openlcb.NodeID)
        
        # assumes that a VerifyNodes has been done and all nodes are in the MimicNodeStore
        tempMemoList = store.getNodeMemos()  # to avoid concurrent mode if something arrives late anyway
        for memo in tempMemoList :
            destNodeID = memo.getNodeID()
            m = org.openlcb.IdentifyEventsAddressedMessage(nid, destNodeID);
            connection.put(m, None)

            self.waitMsec(400) # allow for about 200 events

        return False
        
a = AskForLccInit()
a.setName("AskForLccInit")
a.start()
