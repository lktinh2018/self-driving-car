                   .:                     :,                                          
,:::::::: ::`      :::                   :::                                          
,:::::::: ::`      :::                   :::                                          
.,,:::,,, ::`.:,   ... .. .:,     .:. ..`... ..`   ..   .:,    .. ::  .::,     .:,`   
   ,::    :::::::  ::, :::::::  `:::::::.,:: :::  ::: .::::::  ::::: ::::::  .::::::  
   ,::    :::::::: ::, :::::::: ::::::::.,:: :::  ::: :::,:::, ::::: ::::::, :::::::: 
   ,::    :::  ::: ::, :::  :::`::.  :::.,::  ::,`::`:::   ::: :::  `::,`   :::   ::: 
   ,::    ::.  ::: ::, ::`  :::.::    ::.,::  :::::: ::::::::: ::`   :::::: ::::::::: 
   ,::    ::.  ::: ::, ::`  :::.::    ::.,::  .::::: ::::::::: ::`    ::::::::::::::: 
   ,::    ::.  ::: ::, ::`  ::: ::: `:::.,::   ::::  :::`  ,,, ::`  .::  :::.::.  ,,, 
   ,::    ::.  ::: ::, ::`  ::: ::::::::.,::   ::::   :::::::` ::`   ::::::: :::::::. 
   ,::    ::.  ::: ::, ::`  :::  :::::::`,::    ::.    :::::`  ::`   ::::::   :::::.  
                                ::,  ,::                               ``             
                                ::::::::                                              
                                 ::::::                                               
                                  `,,`


http://www.thingiverse.com/thing:1836395
Raspberry Pi Camera v2 Print Bed Mount by jlarsenwy is licensed under the Creative Commons - Attribution license.
http://creativecommons.org/licenses/by/3.0/

# Summary

This is a ground-up rebuild of <a href="http://www.thingiverse.com/TimOdell">TimOdell's</a>  fantastic raspberry pi <a href="http://www.thingiverse.com/thing:1003252">camera mount</a>.  It's designed to fit the Raspberry Pi V2 camera and mount to the build plate.  This allows the camera to move along with the print to get a more stable image and some pretty sweet time lapses.

You'll need a single M3 bolt and lock nut to mount the camera hinge to the arm.  While the original design had a pin, I found this too hard to print so I just omitted it.

Here are the changes I made to his design:

+ The camera back is re-worked to fit the Raspberry Pi V2 Camera better.  The original version had some clearance issues that wouldn't allow the enclosure to close.  I'm not sure if my version will still fit the V1 camera because I don't have one on hand.  If you have any suggestions on a new version that would fit both please let me know.  

+ The camera base has a narrower gap.  I wanted something that mounted to the aluminum bed mount of my Makerfarm Pegasus (under the heated bed) so it didn't reduce the usable build space.

+ The camera is a little lower to the bed.  I found that the majority of my prints were less than ~3-4 inches tall so this allows me to get a better side view of the layers on smaller prints.

+ The camera's ribbon cable exits the top of the mount, which seems to be the default orientation when using the camera with OctoPrint.  

+ The camera arm is a little thicker and the dimensions are a little tighter to try and help reduce picture wobble when using faster acceleration and movement speeds.  To be honest I have no idea if this helps but I figure it can't hurt... right?

All .step files are included.  Let me know if there's another format you'd like and I'll do my best to provide it.

# Print Settings

Printer: Makerfarm Pegasus 10
Rafts: No
Supports: Yes
Resolution: .2mm
Infill: Up to you

Notes: 
The only place you might need supports is on the camera arm where the one part is angled in.