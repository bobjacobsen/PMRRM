# Profile Directory

There are three profiles here:

 - Dispatcher Complex - this is the primary dispatching profile.  It's got the full-function display, with stable contents.
 - Dispatcher Work in Progress - the development profile.  Once it's reached a stable point and been used for sufficient operations, this is copied to Dispatcher Complex to update that.
 - Dispatcher Simple - a _visually_ simplified version of Dispatcher Complex.  The content is basically the same, and is updated from Dispatcher Work in Progress in a similar way.  The visual simplification is done via a script run at startup which disables and hides certain panel icons.
 
 These profiles use the JMRI local-override mechanism so that they can run on different hardware (or as a simulator) on different machines.  These local configurations are also kept in Git.
 
 Images, configuration (panel) files and script files are stored at the top level in each profile.  There's no cross-loading between profiles so that they can be independently updated.
 