# This removes Turnout listeners from DoubleTurnoutSignalHead heads so that they
# no longer respond to turnout-level changes.  This prevents the heads from getting
# into an update loop, where delayed turnout messages cause the head to change, sending
# more messages, which get delayed, etc.
#
# Written for the PMRRM
#
# Bob Jacobsen    2025

# For every head
for head in signals.getNamedBeanSet():
    # Select the DoubleTurnoutSignalHeads
    type  = head.getClass().getName()
    if type == "jmri.implementation.DoubleTurnoutSignalHead" :
        # Go through the red turnout's listeners to find the listener for this signal head
        for listener in head.getRed().getBean().getPropertyChangeListeners() :
            if listener.getClass().getName().startswith("jmri.implementation.DoubleTurnoutSignalHead$") :
                # And remove that listener
                head.getRed().getBean().removePropertyChangeListener(listener)
                head.getGreen().getBean().removePropertyChangeListener(listener)
