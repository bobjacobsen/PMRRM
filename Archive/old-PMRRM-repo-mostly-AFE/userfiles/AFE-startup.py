# Script for starting the AFE panels on first connection

# Trigger a refresh of the ladder indicators

s = sensors.provideSensor("MS02.01.57.00.01.9C.00.E2")
s.setUserName("AFE Initialize AF Lower Ladder")
s.setState(ACTIVE)  # will be reset automatically

s = sensors.provideSensor("MS02.01.57.00.01.9C.01.02")
s.setUserName("AFE Initialize AF Upper Ladder")
s.setState(ACTIVE)  # will be reset automatically

s = sensors.provideSensor("MS02.01.57.00.01.9C.01.1A")
s.setUserName("AFE Initialize AFE Ladder")
s.setState(ACTIVE)  # will be reset automatically

