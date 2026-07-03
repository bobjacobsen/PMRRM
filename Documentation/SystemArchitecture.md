# PMRRM Control System Architecture

This note describes the long-term goal architecture of the PMRRM's control systems.

It will also have some notes about various intermediate states

## Control Networks

### LocoNet

The LocoNet connects

 - Throttles to the Digitrax DCS-240 DCC command station
 - The Dispatcher to turnouts and occupancy sensors
 - Signal heads on the western half (west of Narrows) of the railroad to PanelPro-resident logic
 
 Currently, LocoNet throttles can directly throw mainline and off-mainline turnouts via LocoNet commands. In the long run, this ability needs to be under Dispatcher control when there's a Dispatcher present.  One possible mechanism for this is to have the actual DS64 turnout controller responding to e.g. address X, have the throttle operators access the turnout via address Y, and have a central function that provides the Y->X conversion when appropriate.  This could be a dedicated device on LocoNet or on LCC via the Gateway, see below.  It should operate automatically, by default doing the conversion before any of the computers are brought up.

### LCC

(Most of) the control panels and their corresponding turnouts are directly driven from LCC. LCC also hosts the logic that drives the signals on the eastern half of the railroad, sometimes referred to as the "CTC signals" from Narrows eastward.

Some control panels will have local/remote switches to control whether other soft and/or hard panels can control their area of responsibility.  There's a separate document that describes how this will be done, but briefly:  Soft panels will have that built into them by having the remote position of the switch disable their on-screen controls. Hard panels will use the "veto event" operations built into the line-control events in an RR-Cirkits node.

Someday, the DCC command station _may_ move onto the LCC network, e.g. using a TCS CS-105.  That will require that the LocoNet-LCC gateway properly supports LocoNet throttles with the DCC command station on LCC.

### WiFi Throttles

Currently, WiFi throttles are not available at the PMRRM due to issues with the making and breaking of local consists.

## TCP/IP Networks

### Wired Ethernet

The Dispatcher computer is connected to the central router via wired Ethernet.

### SSID ???

### SSID ???

## Computers

### Central Server

In the long term, there will be a Central Server computer that's a Windows machine 

- providing any necessary logic that's not resident on LCC
- serving content to web clients for the gallery operators and the dispatcher(s)

This machine should automatically start with Work power. It will have LCC and LocoNet connections.

### Dispatcher Computer

Now, the Dispatcher Computer is a Windows machine that run PanelPro to both display the dispatcher's panel to the dispatcher and also 

- provides the PanelPro-based logic that runs east-end signals
- serves the display content to the gallery operator's web displays

These latter functions in the long run will be moved to the Central Server, leaving the Dispatcher Computer as only a web client for use by the Dispatcher.

See additional documentation in the Profiles directory in git.

In the long run, there may be more than one dispatcher position, in which case there will be more than one dispatcher computer working as a web client to the Central Server.

The Dispatcher machine(s) should automatically start with Work power. in the long run, no LocoNet nor LCC connections are needed, just a TCP/IP connection.  Until the central server is in place, LocoNet, LCC, and TCP/IP connections are needed.


### Test Area Computer

This computer is connected to two test tracks through various kinds of DCC adapter hardware.  These are used with DecoderPro

 - by users to configure their locomotive decoders
 - by the test crew to document in the Roster the performance of locomotives, and to print out summaries of that information for the various layout operators

See additional documentation in the Profiles directory in git.

This machine only needs a TCP/IP connection for updates.  It has local connections to various programming hardware components, but no connection to the main LCC nor LocoNet networks.


### Subsidiary Raspberry Pi's

Some functions have been distributed to Raspberry Pi computers distributed around the railroad. These operate from dedicated SD memory cards.  Those cards are based on Steve Todd's JMRI image, with function-specific additions and modifications.  The master copy for these cards is stored in OneDrive.

#### Operator Display RPis

The gallery displays are driven from two Raspberry Pi's that act as web clients to the Central Server (now, the Dispatcher Computer).  These are only displays, with no control function.

These devices are accessible via VPN as `operator-display-rpi.local` perhaps with a -1 or -2 after "rpi" in the name.

#### Zion East Panel RPi

Now, there's a Raspberry Pi at Zion East that runs a soft panel for the Zion E operator. It both drives the display (from the Zion_East_Panel profile) and provides the logic for the yard track selection, cross-over control, etc.

This will eventually be replaced by a hardware panel and LCC-resident logic.

This device is accessible via VPN as `Zion-E.local`

This machine has a LCC connection for control and a TCP/UP connection for occasional updates and VNC access.

#### Monitoring Server RPi

The Monitoring Server exists to provide network attachments to the LocoNet and LCC networks, typically for monitoring and test use.  It has no direct operating function.

This device is accessible via VPN as `monitoring-rpi.local`

#### Alhambra RPi

Originally a provider of the Alhambra panel(s) logic, this RPi no longer has an operational function. It will eventually be removed.

It may not be currently accessible over TCP/IP.



## Selective Control of Turnouts

Sometimes a turnout on the layout should be controllable via multiple sources:

 - Soft panels e.g. the dispatcher panel
 - One or more local control panels
 - Individual throttles
 
 At other times, one or more of these sources should be disabled from controlling the device. This will need to be done at various levels of granularity.  For example, a remote/local switch on a hardware control panel may, at times, lock out access to the items controlled by the panel from individual throttles and the dispatcher panel.
 
### Disabling Throttle Access
 
 Controlling throttle access to turnouts is done via address aliasing.
 
 For example, if access to turnout 123 is to be controlled, the hardware-driving DS64 channel would be set to 123 + 1024 = 1147.  The 1147 number wouldn't be generally advertised.  When access is to be provided, a hardware device will receive commands for 123 and re-emit them for address 1147.
 
 Doing this via a TowerLCC-Q node requires that the messages traverse the LocoNet-LCC gateway twice, once in each direction.  This raises questions of reliability...
 
### Disabling Soft Panel (Dispatcher) Access
 
 Disabling of soft panel access, e.g. of the dispatcher panel or panels, is done in the coding for those panels themselves.  They check the status of their enabling remote/local switch and disable the control icons on the panel as needed.
 
### Disabling local control panels
 
In some cases, there might be more than one hardware control panel, and there's a need to disable access from one of those. This would then be done using the "Veto Events" capability built into the RR-CirKits LCC nodes.  The remote/local switch would control the veto for the specific outputs.  Access that needs to be controller when then used the vetoable events; access that should always be allowed uses non-vetoed events.


 
