#rigidSolver - Motion Capture tool for Maya
This tool works using the rigid body function from peelSolve, an open source project property of Alastair Macleod.
to find more about peelSolve visit http://www.mocap.ca

It rebuilds a marker's data(animation) adquired in a motion capture session, using data from markers close to it. 
The manual action for this process takes too much time and not enough accuracy for pin-pointing the relative position of a marker 


rigidSolver uses selected markers to create a rigid body, it asks the user which markers have more reliable data to make them have more influence in to the broken ones.
It also asks for the time lapse it needs to rebuild the data. 
Once, defined high and low reliability, creates a relative for each broken marker and substitutes the original animation with the relative's.
Finally it deletes the relative, resulting in all of the broken markers with a clean and averaged animation. 

Notes:
*needs at least three markers to work.
*at least one marker needs to be above 0.6 acurracy.
*depending on the acuracy of the markers, the data created will be reliable or not.
*it will recreate the data for each marker below 0.5 acurracy
*places the new data automatically and creates connections of 10 frames between the new data and the old. 