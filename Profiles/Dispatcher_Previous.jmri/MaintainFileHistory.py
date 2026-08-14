# Loads the most recent file write from the history into a memory, 
# then truncates the history at one level deep

import jmri
import org.slf4j.Logger
import org.slf4j.LoggerFactory

logger = org.slf4j.LoggerFactory.getLogger("script.MaintainFileHistory")

history = jmri.InstanceManager.getDefault(jmri.jmrit.revhistory.FileHistory)
historyList = history.getList()

memories.provideMemory("IM$LastWrite").value = ""
def checkOneHistoryLevel(historyList) :
    for item in historyList :
        # logger.info(item.type+" "+item.date+" "+str(item.history == None))
        if item.type == "Store" and item.date > memories.provideMemory("IM$LastWrite").value :
            memories.provideMemory("IM$LastWrite").value = item.date
        if item.history is not None :
            checkOneHistoryLevel(item.history.getList())

checkOneHistoryLevel(historyList)

logger.info("Last write time is "+memories.provideMemory("IM$LastWrite").value)

history.purge(1)
logger.info("File history shortened")
