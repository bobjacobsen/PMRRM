# Local/Remote Selection at Zion East

This note discusses the oepration of the Local/Remote switch on the Zion East hard panel.

The Zion East panel provides support for several jobs:

 - The Port operator
 - The Branchline operator
 - The Zion East Yardmaster
 
along with connections between their areas of responsibility.

To summarize:

 - When the Local/Remote switch is in  either position, the Zion East Yardmaster has control through the hard panel over the four Zion East yards (Freight A, Freight B, Garden and Passenger) through the Zion interlocking (Yazoo and Xerox) and Whiskey. Control over Whiskey is shared with the Dispatcher's soft panel.

 - Only when the Local/Remote switch is in the Remote position, the Dispatcher's soft panel can also control the Zion Interlocking (Yazoo and Xerox) through the Zion East yards.
 
 - Throttle control of the Zion Interlocking (Yazoo and Xerox) is only permitted when the Local/Remote switch is in Remote.

 - The Port operator has control over the Port turnouts via fascia switches and throttles at all times.  The Zion East panel also allows the Port operator to command the Port turnouts regardless of the position of the Local/Remote switch.
 
 - The Branchline operator has control over the Branchline turnouts via throttles at all times.  The Zion East panel also allows the Branchline operator to command the Branchline turnouts, including through Garden track 5 and the tracks behind the station, regardless of the position of the Local/Remote switch.
 
 - The hard panel allows operation of the crossovers between the Zion East yards and the Port/Branchline areas regardless of the position of the Local/Remote switch.  Operation of these is via discussion between the Zion East Yardmaster and the Port/Branchline operators.

 
## Additional Requirements

 - Only the Remote/Local switch on the physical panel will change modes; there won't be such a switch on the soft panels, nor can it be accessed via throttle.

 - It's desirable for as much as possible of this to work even when no computer is running.


## Current Status of Controls

 - The turnouts in the Zion East operator area are on direct LCC control
    - This includes the Zion East Branch - Zion crossover, which allows the Zion E operator to route directly to the T1/T2/G5 tracks above the Garden area
 - Some have LocoNet addresses:
    - The Port and Branchline area, with addresses 730-748 (Port), Branchline to the right (709-710) and the area above the Garden tracks (716, 729)
    - The Zion Branch East Port - Zion crossover (711) which allows the Zion East operator to route directly to the Port area 
    - The Whiskey area with addresses 95-99 and 188, 195
    - The Zion interlocking area with addresses 100-107
 - The Port area turnouts are also directly controlled by fascia buttons connected to their accessory decoders
 - Currently defined LocoNet turnouts on the layout:
    - Between 1000 and 1299 inclusive, there are a half-dozen or so LT turnouts defined that either seem to be not used, or are LT-LCC signal communication which can be moved.
    - None between 1300 and 2000 inclusive except the LT1800 power-relay control. The LT1800 turnout address can be moved as necessary.
 

## Proposed Solution 

 - Move the remote-vetoed LocoNet hardware addresses in Zion Interlocking up by 1024 and keep those numbers secret
    - Leave the lower numbers on the panels so that people still use them with throttles when they're functional in remote mode
    - Clear/re-define the pre-existing PanelPro LT turnout definitions as needed
    - Run a script in the main layout computer or in a TowerLCC-Q node that, when in remote mode, translates from the lower throttle-friendly LocoNet address to the higher actual-hardware LocoNet address.
 - The Zion E hard panel works directly with those new high LocoNet addresses as needed using logic resident in LCC nodes. No separate computer support is needed. 
 - The soft panels(s) will be coded to check the Local/Remote switch position before allowing control of anything in the Zion East area.
    - Initial approach, to be tested, is to use a script to set the 'controllable' attribute on Layout Editor turnout icons from the Local/Remote sensor. This is how the Zion Interlocking is handled on the current soft Dispatcher panel.
 
## Implementation Notes
 
  - The proposed solution will allow people who learn the higher LocoNet addresses to control the Zion East turnouts via throttle.  Keeping those addresses secret is not likely to succeed forever, so eventually there will need to be a way to discourage their use.
  - The proposed solution will still allow people with access to the Turnout Table in a JMRI instance to operate turnouts in the Zion East area and to learn the LocoNet hardware addresses there.  The Turnout Table can be disabled via JMRI startup script if that's required.
  - Migration to this solution will take significant time, as some of the turnouts in the area will have to have their hardware addresses changed manually. Keeping the old setup working while moving to the new one would add a lot of work.
    - Fall-back to the previous implementation during migration, if needed, is going to require a lot of thought and even more work.
  
