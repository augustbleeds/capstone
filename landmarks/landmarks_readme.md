A quick and dirty readme for some quick and dirty code.
If you have any further questions, just ping me.

README
======

The python programs were written in Jupyter(Python 2.7) for testing and uploaded as such (hence the .ipynb extension).
These files will only work in Jupyter.

Unity-Listener.py contains the most recent copy of the whole program.
Dependencies are listed in the import section at the top.
Requires the files in the Haarcascades folder, as well as the shape_predictor_68_face_landmarks.dat to be present.
Also depends on software to duplicate the camera feed (I think it was "SplitCam," use at your own risk).

Start it up before the Unity program, using: python Unity-Listener.py
This starts a listening server on localhost, port 10000. This can be changed within the script. (look for HOST, PORT in main)
I think that's it, everything else should work.

One thing about the OpenCV2 window, if I remember correctly, is that the gui 'X' button doesn't really work, so Ctrl-C
on the command prompt is what you may have to use to close out of the program.
Also, occasionally crashes.
May look laggy because we average frames together to smooth out the facial landmark detection from jitters.

GL Rob.





