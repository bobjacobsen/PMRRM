#
# Setup for the Zion East panel, before being connected to final hardware
#
# Organized from right to left
# 

import jmri

class InitializeZionEPanel(jmri.jmrit.automat.AbstractAutomaton) :

    # handle() is called repeatedly until it returns false.
    def handle(self):

        # Remote levers
        sensors.getSensor("ZE XY Remote - Local").state = ACTIVE
        sensors.getSensor("ZE Remote - Local").state = INACTIVE

        # Whiskey occupancy and signals - defer to gateway
        #sensors.getSensor("Whiskey 1 occupancy").state = INACTIVE
        #sensors.getSensor("Whiskey 2 occupancy").state = INACTIVE
        #sensors.getSensor("Whiskey 3 occupancy").state = INACTIVE
        #signals.getSignalHead("Whiskey 1 Exit W").appearance = GREEN
        #signals.getSignalHead("Whiskey 2 Exit W").appearance = GREEN
        #signals.getSignalHead("Whiskey 3 Exit W").appearance = GREEN

        #sensors.getSensor("Whisky Xerox transition occupancy").state = INACTIVE
        #sensors.getSensor("Xerox 1 occupancy").state = INACTIVE
        #sensors.getSensor("Xerox 2 occupancy").state = INACTIVE

        # Yazoo NX buttons
        # turnouts.getTurnout("ZE NX X1 request").state = CLOSED
        # turnouts.getTurnout("ZE NX X2 request").state = CLOSED
        # turnouts.getTurnout("ZE NX Y1 request").state = CLOSED
        # turnouts.getTurnout("ZE NX Y2 request").state = CLOSED
        # turnouts.getTurnout("ZE NX Y3 request").state = CLOSED
        sensors.getSensor("ZE NX X1 ack").state = INACTIVE
        self.waitMsec(50)
        sensors.getSensor("ZE NX X2 ack").state = INACTIVE
        self.waitMsec(50)
        sensors.getSensor("ZE NX Y1 ack").state = INACTIVE
        self.waitMsec(50)
        sensors.getSensor("ZE NX Y2 ack").state = INACTIVE
        self.waitMsec(50)
        sensors.getSensor("ZE NX Y3 ack").state = INACTIVE
        self.waitMsec(50)

        # Set ladders to a particular track
        turnouts.getTurnout("ZE EABECR FrtA request").state = THROWN
        turnouts.getTurnout("ZE EABECR FrtB request").state = THROWN
        turnouts.getTurnout("ZE T1 request").state = THROWN
        turnouts.getTurnout("ZE P1 request").state = THROWN
        turnouts.getTurnout("ZE F1 request").state = THROWN
        self.waitMsec(50)
        turnouts.getTurnout("ZE F8 request").state = THROWN  # clear Run West
        self.waitMsec(50)
        turnouts.getTurnout("ZE F5 request").state = THROWN

        # Zion team tracks power
        sensors.getSensor("ZE Team power ack").state = ACTIVE
        sensors.getSensor("ZE Team power request").state = INACTIVE

        # Zion power buttons are single-address Sensors
        sensors.getSensor("ZE F1 power request").state = INACTIVE
        sensors.getSensor("ZE F2 power request").state = INACTIVE
        sensors.getSensor("ZE F3 power request").state = INACTIVE
        sensors.getSensor("ZE F4 power request").state = INACTIVE
        sensors.getSensor("ZE F5 power request").state = INACTIVE
        sensors.getSensor("ZE F6 power request").state = INACTIVE
        sensors.getSensor("ZE F7 power request").state = INACTIVE
        sensors.getSensor("ZE F8 power request").state = INACTIVE

        sensors.getSensor("ZE P1 power request").state = INACTIVE
        sensors.getSensor("ZE P2 power request").state = INACTIVE
        sensors.getSensor("ZE P3 power request").state = INACTIVE
        sensors.getSensor("ZE P4 power request").state = INACTIVE
        sensors.getSensor("ZE P5 power request").state = INACTIVE
        sensors.getSensor("ZE P6 power request").state = INACTIVE
        sensors.getSensor("ZE P7 power request").state = INACTIVE

        sensors.getSensor("ZE Misc power request").state = INACTIVE

        return False

# create one of these
a = InitializeZionEPanel()

# set the name, as a example of configuring it
a.setName("Initialize Zion E Panel")

# and start it running - this will only take a short time
a.start()
