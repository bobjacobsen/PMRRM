# Dispatcher Machine Setup

There are three primary Dispatcher profiles in the `Profiles` directory:

 - `Dispatcher Work in Progress` - This is where development happens.
 - `Dispatcher Latest` - This is the one recommended for general use on the layout.
 - `Dispatcher Previous` - This is the previous version recommended for general use.
 
 Images, configuration (panel) files and script files are stored at the top level in each profile.  There's no cross-loading between profiles so that they can be independently updated.
 
Temporarily (May 2026), there are also some inactive Dispatcher profiles.  These have been deprecated and will eventually go away.

 - `Dispatcher Complex` - this was the original primary dispatching profile.  
 - `Dispatcher Simple` - a _visually_ simplified version of `Dispatcher Complex`.  
 - `Dispatcher WIP` - a copy of `Dispatcher Work in Progress` at one point.
 
 These profiles use the JMRI local-override mechanism so that they can run on different hardware (or as a simulator) on different machines.  
 
 ## Repository deployment on the PMRRM Dispatcher machine
 
 At the Museum, there are two clones of this repository under the `electricalcrew` account:
 - `~electricalcrew/OneDrive/PMRRM-Repository` - This is the checkout for development and testing when logged into the `electricalcrew` account.
 - `~dispatch/Documents/PMRRM-snapshot` - Contains the specific checked-out tag used by the `dispatch` account.

 ## Development
 
 New development should be done in the `Work in Progress` profile.  This means that you start the `Work in Progress` profile when running the program. If you want to directly edit a file, you edit the version that's found in `Profiles/Dispatcher_Work_in_Progress.jmri` directory in the PMRRM repository that's cloned to your computer.
 
 ## Process for updating the development profiles being used at the PMRRM
 
 Development on the `Work in Progress` profile is relatively continuous. 
 
 Working at the PMRRM on development, including testing the most recent changes, is done by running while logged into the `electricalcrew` account.  JMRI for development runs from the `~/PMRRM` directory on that account. To get the most recent contents from off-site development into that directory, use the usual `get fetch` and `get merge` commands either on the command line or via GitHub Desktop.  These will download the most recent content from the main GitHub repository, so please push your changes from your local machine and synchronize first.
 
 ## Process for updating the profiles being used at the PMRRM for normal running
 
General operations at the PMRRM is done by running on the `Dispatch` account.  The profiles in that account are not updated at every work session, but rather when development has reached a useful point.
 
For reasons of content protection, JMRI for operations runs from the `PMRRM-snapshot` directory within the `electricalcrew` account. To get the most recent contents from development into that directory, sign on to `electricalcrew`, change directory to `PMRRM-snapshot` and use the usual `get fetch` and `get merge` commands on the command line or via GitHub Desktop.  These will load the most recent content from the main GitHub repository, so please synchronize and push your changes from your local machine first.

Once you have updated the content of `PMRRM-snapshot`, place a date tag on it in the form e.g. `2025-07-10-snapshot`. This allows us to accurately return to those specific contents for debugging elsewhere if a problem develops. The commands to do this from the command line is `git tag 2025-07-10-snapshot` followed `git push --tags` (two dashes) where the `--tags` says to push the tags too. In GitHub Desktop, tags are automatically pushed when you do any push operation.

Finally, sign into the `dispatch` account and check each of the three profiles for
 - basic launching
 - proper steps in startup and layout communications
 - check that menu items are disabled
 - none have "check files on shutdown" configured
 
 ## Process for rolling profiles at Github head
 
 Periodically, we move the contents of the `Latest` profile to the `Previous` profile and move the contents of the current `Work in Progress` profile to the `Latest` profile
 
 These are the steps for doing that profile-contents move in the `~electricalcrew/PMRRM` directory. This is done occasionally when the most recent development`Work in Progress` is considered stable and further development will be happening on it.
 
 Note that this updates the profiles used by the `~electricalcrew` account and the GitHub contents, but does not update the profiles used by the `~dispatch` account.  That has to be done separately, see the section above on how to update the `dispatch` account.
  
 These steps are done from the `electricalcrew` account which has write access to the relevant files. Note that this is _not_ copying the current files in the `Dispatch` account, but the `electricalcrew` account.  Make sure that's what you want to do.
 
  - Check for any uncommitted changes in `~electricalcrew/PMRRM/` and cope.
    
  - Update the `~electricalcrew/PMRRM/` repository to the most recent contents of Github using the usual `get fetch` and `git merge` commands or GitHub Desktop.
  
  - If you're using GitHub Desktop, quit the program at this point.
  
  - Move the `~electricalcrew/PMRRM/Profile/Dispatcher_Previous.jmri` directory aside, e.g. to the Desktop.  This can be deleted at the end of the process as that directory will be superceded in the next step.
  
  - Rename the `~electricalcrew/PMRRM/Profile/Dispatcher_Latest.jmri` directory to `~electricalcrew/PMRRM/Profile/Dispatcher_Previous.jmri`
  
  - Make a *copy* of the `~electricalcrew/PMRRM/Profile/Dispatcher_Work_in_Progress.jmri` directory and name it `~electricalcrew/PMRRM/Profile/Dispatcher_Latest.jmri`
  
  - If you're using GitHub Desktop, you can restart it now.
  
  - Check the changes, either with the `git status` command or by looking at changes in GitHub Desktop.  There should be some, but not too many: maybe up to two dozen or so. (There may be quite a few in the `roster/` subdirectory; that's OK.)
  If you see much more than that, make sure that you've titled the renamed directories properly. Also check that you don't see any changes in the `~electricalcrew/PMRRM/Profile/Dispatcher_Work_in_Progress.jmri` directory.
  
  - Now we have to *undo* the changes to two files.  With GitHub desktop, this is done by selecting the files in the following lines and telling it to drop changes. From the command line, this is done with (note the third term in the lines below is _two_ hyphens)
    - `git checkout -- ~electricalcrew/PMRRM/Profile/Dispatcher_Previous.jmri/profile/profile.properties`
    - `git checkout -- ~electricalcrew/PMRRM/Profile/Dispatcher_Latest.jmri/profile/profile.properties`
  
  - Check the number of changes again and make sure those two files are _not_ marked as changed.
  
  - Start JMRI and check each of the three profiles for
    - basic launching
    - proper steps in startup and layout communications

  - Using either the command line or GitHub Desktop, commit all those changes. Push them up to the GitHub repository.
  
  - If appropriate, do the "Process for updating the profiles being used at the PMRRM for normal running" process above.
  
