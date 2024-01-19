# X1-X2 on the left
# Y1-Y2-Y3 on the right
# 
# 6 individual valid routes by name
#     Route_Z1_X1 through Route_Z3_X2
#     
#     
#     Conflicts:
#         Any shared end point
#             Note an end point can't be both Allocated and On at the same time
#         X2-Y1 conflicts with X1-Y2 and X1-Y3
#         X2-Y2 conflicts with X1-Y3
#         X1-Y2 conflicts with X2-Y1
#         X1-Y3 conflicts with X2-Y1 and X2-Y2
#         
# Lamp states:
#     "On" indicates an assigned route: lit
#     "Off" not allocated to a route, dark
#     "Allocated" not yet an assigned route, indicating one (future) end: lit
#     
# "Allocated" is before assignment of a complete route, waiting for the other end.
# There can only be one "Allocated" in each side at a time.
# 
# Button "pressed" is a newly-encountered down button.
#     Could be a request on
#     Could be a request off
# 
# Assumes only one button Pressed on any given pass


# Initialize the global variables
# These are global for diagnostic purposes
global X1InputLast, X1On, X1Allocated, X1Off
global X2InputLast, X2On, X2Allocated, X2Off
global Y1InputLast, Y1On, Y1Allocated, Y1Off
global Y2InputLast, Y2On, Y2Allocated, Y2Off
global Y3InputLast, Y3On, Y3Allocated, Y3Off

global Route_X1_Y1, Route_X1_Y2, Route_X1_Y3
global Route_X2_Y1, Route_X2_Y2, Route_X2_Y3

X1InputLast = X1On = X1Allocated = False; X1Off = True
X2InputLast = X2On = X2Allocated = False; X2Off = True
Y1InputLast = Y1On = Y1Allocated = False; Y1Off = True
Y2InputLast = Y2On = Y2Allocated = False; Y2Off = True
Y3InputLast = Y3On = Y3Allocated = False; Y3Off = True

Route_X1_Y1 = Route_X1_Y2 = Route_X1_Y3 = False
Route_X2_Y1 = Route_X2_Y2 = Route_X2_Y3 = False
    
class NXdriver(jmri.jmrit.automat.AbstractAutomaton) :

    def init(self):
        signals.getSignalHead("Blinker").setAppearance(FLASHRED)
        return
        
    def handle(self):
        global X1InputLast, X1On, X1Allocated, X1Off
        global X2InputLast, X2On, X2Allocated, X2Off
        global Y1InputLast, Y1On, Y1Allocated, Y1Off
        global Y2InputLast, Y2On, Y2Allocated, Y2Off
        global Y3InputLast, Y3On, Y3Allocated, Y3Off

        global Route_X1_Y1, Route_X1_Y2, Route_X1_Y3
        global Route_X2_Y1, Route_X2_Y2, Route_X2_Y3
        
        X1Turnout = turnouts.getTurnout("ZE NX X1 request")
        X2Turnout = turnouts.getTurnout("ZE NX X2 request")
        Y1Turnout = turnouts.getTurnout("ZE NX Y1 request")
        Y2Turnout = turnouts.getTurnout("ZE NX Y2 request")
        Y3Turnout = turnouts.getTurnout("ZE NX Y3 request")
        
        X1Lamp = sensors.getSensor("ZE NX X1 ack")
        X2Lamp = sensors.getSensor("ZE NX X2 ack")
        Y1Lamp = sensors.getSensor("ZE NX Y1 ack")
        Y2Lamp = sensors.getSensor("ZE NX Y2 ack")
        Y3Lamp = sensors.getSensor("ZE NX Y3 ack")
        
        MTT103 = turnouts.getTurnout("MTT103")
        MTT104 = turnouts.getTurnout("MTT104")
        MTT106 = turnouts.getTurnout("MTT106")
        MTT107 = turnouts.getTurnout("MTT107")
    
        self.waitMsec(20)  # to simulate -Q node
        
        # get inputs to process
        X1InputNow = X1Turnout.getCommandedState() == THROWN
        X2InputNow = X2Turnout.getCommandedState() == THROWN
        Y1InputNow = Y1Turnout.getCommandedState() == THROWN
        Y2InputNow = Y2Turnout.getCommandedState() == THROWN
        Y3InputNow = Y3Turnout.getCommandedState() == THROWN

        # blink the Allocated sensors
        # this is disabled here, as it causes the CpmmandedState to change and 
        #   creates a spurious input.  I'm keeping the section to remind
        #   me to see whether this can be done in STL via a sacrificial output
        #
        blinker = (turnouts.getTurnout("Blinker").getState() == THROWN);
        if blinker :
            allocatedOutput = ACTIVE
        else :
            allocatedOutput = INACTIVE
        if X1Allocated : X1Lamp.state = allocatedOutput
        if X2Allocated : X2Lamp.state = allocatedOutput
        if Y1Allocated : Y1Lamp.state = allocatedOutput
        if Y2Allocated : Y2Lamp.state = allocatedOutput
        if Y3Allocated : Y3Lamp.state = allocatedOutput
        
        # compute changes
        X1Pressed = not X1InputLast and X1InputNow
        X1InputLast = X1InputNow
        X2Pressed = not X2InputLast and X2InputNow
        X2InputLast = X2InputNow
        Y1Pressed = not Y1InputLast and Y1InputNow
        Y1InputLast = Y1InputNow
        Y2Pressed = not Y2InputLast and Y2InputNow
        Y2InputLast = Y2InputNow
        Y3Pressed = not Y3InputLast and Y3InputNow
        Y3InputLast = Y3InputNow

        if not (X1Pressed or X2Pressed or Y1Pressed or Y2Pressed or Y3Pressed) : return True
        
        # check for turning off one a button
        if X1Pressed and (X1On or X1Allocated): # second push of lit button
            X1Off = True; X1On = False; X1Allocated = False 
            X1Lamp.state = INACTIVE
            if Route_X1_Y1:
                Route_X1_Y1 = False
                Y1Off = True; Y1On = False; Y1Allocated = False
                Y1Lamp.state = INACTIVE
            if Route_X1_Y2:
                Route_X1_Y2 = False
                Y2Off = True; Y2On = False; Y2Allocated = False
                Y2Lamp.state = INACTIVE
            if Route_X1_Y3:
                Route_X1_Y3 = False
                Y3Off = True; Y3On = False; Y3Allocated = False
                Y3Lamp.state = INACTIVE
            return True # end processing **
        if X2Pressed and (X2On or X2Allocated): # second push of lit button
            X2Off = True; X2On = False; X2Allocated = False 
            X2Lamp.state = INACTIVE
            if Route_X2_Y1:
                Route_X2_Y1 = False
                Y1Off = True; Y1On = False; Y1Allocated = False
                Y1Lamp.state = INACTIVE
            if Route_X2_Y2:
                Route_X2_Y2 = False
                Y2Off = True; Y2On = False; Y2Allocated = False
                Y2Lamp.state = INACTIVE
            if Route_X2_Y3:
                Route_X2_Y3 = False
                Y3Off = True; Y3On = False; Y3Allocated = False
                Y3Lamp.state = INACTIVE
            return True # end processing **
        if Y1Pressed and (Y1On or Y1Allocated): # second push of lit button
            Y1Off = True; Y1On = False; Y1Allocated = False 
            Y1Lamp.state = INACTIVE
            if Route_X1_Y1:
                Route_X1_Y1 = False
                X1Off = True; X1On = False; X1Allocated = False
                X1Lamp.state = INACTIVE
            if Route_X2_Y1:
                Route_X2_Y1 = False
                X2Off = True; X2On = False; X2Allocated = False
                X2Lamp.state = INACTIVE
            return True # end processing **
        if Y2Pressed and (Y2On or Y2Allocated): # second push of lit button
            Y2Off = True; Y2On = False; Y2Allocated = False 
            Y2Lamp.state = INACTIVE
            if Route_X1_Y2:
                Route_X1_Y2 = False
                X1Off = True; X1On = False; X1Allocated = False
                X1Lamp.state = INACTIVE
            if Route_X2_Y2:
                Route_X2_Y2 = False
                X2Off = True; X2On = False; X2Allocated = False
                X2Lamp.state = INACTIVE
            return True # end processing **
        if Y3Pressed and (Y3On or Y3Allocated): # second push of lit button
            Y3Off = True; Y3On = False; Y3Allocated = False 
            Y3Lamp.state = INACTIVE
            if Route_X1_Y3:
                Route_X1_Y3 = False
                X1Off = True; X1On = False; X1Allocated = False
                X1Lamp.state = INACTIVE
            if Route_X2_Y3:
                Route_X2_Y3 = False
                X2Off = True; X2On = False; X2Allocated = False
                X2Lamp.state = INACTIVE
            return True # end processing **

        # At this point, the pressed button is on Off state

        # Only one allocated track per side possible
        if X1Pressed :
            X1Allocated = True; X1Off = False; X1On = False
            X1Lamp.state = ACTIVE
            if X2Allocated :
                X2Off = True; X2On = False; X2Allocated = False 
                X2Lamp.state = INACTIVE
        if X2Pressed :
            X2Allocated = True; X2Off = False; X2On = False
            X2Lamp.state = ACTIVE
            if X1Allocated :
                X1Off = True; X1On = False; X1Allocated = False 
                X1Lamp.state = INACTIVE
        if Y1Pressed :
            Y1Allocated = True; Y1Off = False; Y1On = False
            Y1Lamp.state = ACTIVE
            if Y2Allocated :
                Y2Off = True; Y2On = False; Y2Allocated = False 
                Y2Lamp.state = INACTIVE
            if Y3Allocated :
                Y3Off = True; Y3On = False; Y3Allocated = False 
                Y3Lamp.state = INACTIVE
        if Y2Pressed :
            Y2Allocated = True; Y2Off = False; Y2On = False
            Y2Lamp.state = ACTIVE
            if Y1Allocated :
                Y1Off = True; Y1On = False; Y1Allocated = False 
                Y1Lamp.state = INACTIVE
            if Y3Allocated :
                Y3Off = True; Y3On = False; Y3Allocated = False 
                Y3Lamp.state = INACTIVE
        if Y3Pressed :
            Y3Allocated = True; Y3Off = False; Y3On = False
            Y3Lamp.state = ACTIVE
            if Y1Allocated :
                Y1Off = True; Y1On = False; Y1Allocated = False 
                Y1Lamp.state = INACTIVE
            if Y2Allocated :
                Y2Off = True; Y2On = False; Y2Allocated = False 
                Y2Lamp.state = INACTIVE


        # Exhaustively check available route candidates and assign as needed:
        if X1Allocated and Y1Allocated : # no conflicting route to check
            Route_X1_Y1 = True
            # fire Route-X1-Y1 outputs
            MTT107.state = CLOSED; MTT104.state = THROWN
            X1On = True; X1Off = False; X1Allocated = False
            X1Lamp.state = ACTIVE
            Y1On = True; Y1Off = False; Y1Allocated = False
            Y1Lamp.state = ACTIVE
        
        if X1Allocated and Y2Allocated and not Route_X2_Y1 :   # no conflicting route set
            Route_X1_Y2 = True
            # fire Route-X1-Y2 outputs
            MTT107.state = CLOSED; MTT106.state = CLOSED; MTT105 = CLOSED; MTT104.state = CLOSED
            X1On = True; X1Off = False; X1Allocated = False
            X1Lamp.state = ACTIVE
            Y2On = True; Y2Off = False; Y2Allocated = False
            Y2Lamp.state = ACTIVE
        if X1Allocated and Y2Allocated and Route_X2_Y1 :       # conflicting route set, drop allocations
            X1Off = True; X1On = False; X1Allocated = False 
            X1Lamp.state = INACTIVE
            Y2Off = True; Y2On = False; Y2Allocated = False 
            Y2Lamp.state = INACTIVE
        
        if X1Allocated and Y3Allocated and not (Route_X2_Y2 or Route_X2_Y1) :   # no conflicting route set
            Route_X1_Y3 = True
            # fire Route-X1-Y3 outputs
            MTT107.state = CLOSED; MTT106.state = THROWN; MTT105 = CLOSED; MTT104.state = CLOSED
            X1On = True; X1Off = False; X1Allocated = False
            X1Lamp.state = ACTIVE
            Y3On = True; Y3Off = False; Y3Allocated = False
            Y3Lamp.state = ACTIVE
        if X1Allocated and Y3Allocated and (Route_X2_Y2 or Route_X2_Y1) :       # conflicting route set, drop allocations
            X1Off = True; X1On = False; X1Allocated = False 
            X1Lamp.state = INACTIVE
            Y3Off = True; Y3On = False; Y3Allocated = False 
            Y3Lamp.state = INACTIVE
        
        if X2Allocated and Y1Allocated and not (Route_X1_Y2 or Route_X1_Y3) :
            Route_X2_Y1 = True
            # fire Route-X2-Y1 outputs
            MTT107.state = CLOSED; MTT106.state = THROWN; MTT105 = THROWN; MTT103.state = THROWN
            X2On = True; X2Off = False; X2Allocated = False
            X2Lamp.state = ACTIVE
            Y1On = True; Y1Off = False; Y1Allocated = False
            Y1Lamp.state = ACTIVE
        if X2Allocated and Y1Allocated and (Route_X1_Y2 or Route_X1_Y3) :       # conflicting route set, drop allocations
            X2Off = True; X2On = False; X2Allocated = False 
            X2Lamp.state = INACTIVE
            Y1Off = True; Y1On = False; Y1Allocated = False 
            Y1Lamp.state = INACTIVE
        
        if X2Allocated and Y2Allocated and not Route_X1_Y3 :   # no conflicting route set
            Route_X2_Y2 = True
            # fire Route-X2-Y2 outputs
            MTT107.state = CLOSED; MTT106.state = CLOSED; MTT105 = THROWN; MTT103.state = THROWN
            X2On = True; X2Off = False; X2Allocated = False
            X2Lamp.state = ACTIVE
            Y2On = True; Y2Off = False; Y2Allocated = False
            Y2Lamp.state = ACTIVE
        if X2Allocated and Y2Allocated and Route_X1_Y3 :       # conflicting route set, drop allocations
            X2Off = True; X2On = False; X2Allocated = False 
            X2Lamp.state = INACTIVE
            Y2Off = True; Y2On = False; Y2Allocated = False 
            Y2Lamp.state = INACTIVE
        
        if X2Allocated and Y3Allocated : # no conflicting route to check
            Route_X2_Y3 = True
            # fire Route-X2-Y3 outputs
            MTT106.state = CLOSED; MTT103.state = CLOSED
            X2On = True; X2Off = False; X2Allocated = False
            X2Lamp.state = ACTIVE
            Y3On = True; Y3Off = False; Y3Allocated = False
            Y3Lamp.state = ACTIVE
           
        return True
        
        

NXdriver().start()
