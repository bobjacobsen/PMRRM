#
# Setup for the Zion East panel, before being connected to final hardware
#
# Organized from right to left
# 

# Remote levers
sensors.getSensor("ZE XY Remote - Local").state = ACTIVE
sensors.getSensor("ZE Remote - Local").state = INACTIVE

# Whiskey occupancy and signals
sensors.getSensor("ZE Whiskey 1 Occupancy").state = INACTIVE
sensors.getSensor("ZE Whiskey 2 Occupancy").state = INACTIVE
sensors.getSensor("ZE Whiskey 3 Occupancy").state = INACTIVE
signals.getSignalHead("Whiskey 1 Exit W").appearance = GREEN
signals.getSignalHead("Whiskey 2 Exit W").appearance = GREEN
signals.getSignalHead("Whiskey 3 Exit W").appearance = GREEN

# Yazoo NX buttons
turnouts.getTurnout("ZE NX X1 request").state = CLOSED
turnouts.getTurnout("ZE NX X2 request").state = CLOSED
turnouts.getTurnout("ZE NX Y1 request").state = CLOSED
turnouts.getTurnout("ZE NX Y2 request").state = CLOSED
turnouts.getTurnout("ZE NX Y3 request").state = CLOSED
sensors.getSensor("ZE NX X1 ack").state = INACTIVE
sensors.getSensor("ZE NX X2 ack").state = INACTIVE
sensors.getSensor("ZE NX Y1 ack").state = INACTIVE
sensors.getSensor("ZE NX Y2 ack").state = INACTIVE
sensors.getSensor("ZE NX Y3 ack").state = INACTIVE


# Zion main power
sensors.getSensor("ZE Main 1 power ack").state = ACTIVE
sensors.getSensor("ZE Main 2 power ack").state = ACTIVE
sensors.getSensor("ZE Main 3 power ack").state = ACTIVE
sensors.getSensor("ZE Main 1 power request").state = INACTIVE
sensors.getSensor("ZE Main 2 power request").state = INACTIVE
sensors.getSensor("ZE Main 3 power request").state = INACTIVE

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



#sensors.getSensor("").state = INACTIVE
#turnouts.getTurnout("").state = CLOSED
#signals.getSignalHead("").appearance = GREEN