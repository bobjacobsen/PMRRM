# Check a LocoNet-LCC gateway by periodically 
# sending a turnout command in each direction and
# checking for receipt.
#
# Written by Bob Jacobsen for the PMRRM 2026
#
# To cancel this script, go to the Thread Monitor in the Scripting menu
# and kill the GatewayPongGame thread.

import java
import jmri
import org.slf4j.Logger
import org.slf4j.LoggerFactory

to_lt = turnouts.provideTurnout("LT2021")
from_lt = turnouts.provideTurnout("MTT2021")

to_mt = turnouts.provideTurnout("MTT2022")
from_mt = turnouts.provideTurnout("LT2022")

failSound = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/EndGame.wav"))

lt_mt = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Pong1.wav"))
mt_lt = jmri.jmrit.Sound(jmri.util.FileUtil.getExternalFilename("preference:resources/sounds/Pong2.wav"))

status = memories.provideMemory("IMProgramStatus")  # for status display on panel

log = org.slf4j.LoggerFactory.getLogger(
        "script.GatewayPongGame"
        )

class GatewayPongGame (jmri.jmrit.automat.AbstractAutomaton) :

    def check(self, source, sink, oksound, direction) :
        # figure out needed change
        oldstate = sink.getKnownState()
        newstate = THROWN
        if oldstate == THROWN : newstate = CLOSED
        
        source.setCommandedState(newstate)
        self.waitMsec(1000) # long due to traffic delays during startup

        if sink.getKnownState() == newstate :
            # success!
            log.debug("{} OK", direction)
            status.setValue("Gateway OK")
            oksound.play()
        else :
            # fail - play sound
            log.error("{} failed", direction)
            status.setValue("Gateway Failed: "+direction)
            failSound.play()
            # and wait a bit to reduce repetition rate of sound
            self.waitMsec(10000)

    def init(self) : 
        status.setValue("Loading, please wait")
        self.waitMsec(45000) # wait for layout to stabilize
        
    def handle(self) : 

        # ping sound - MTT to LT
        self.check(to_mt, from_mt, mt_lt, "LCC -> LocoNet")
        self.waitMsec(5000)

        # pong sound - LT to MTT
        self.check(to_lt, from_lt, lt_mt, "LocoNet -> LCC")
        self.waitMsec(5000)
        
        # repeat
        return True
        
t = GatewayPongGame()
t.setName("GatewayPongGame")
t.start()
