# MoteMidi
Use wii peripherals to send midi data on linux

MoteMidi reads /dev/inpout/eventX to interface with input devices. Was made with the intension of using [Guitar Hero World Tour drums](https://en.wikipedia.org/wiki/Guitar_Hero_World_Tour#Drums) plugged into a Nintendo Wiimote. 

# Usage
The project is in very early devlopment. You'll first need to make sure you have [evdev](https://python-evdev.readthedocs.io/en/latest/) and [rtmidi](https://spotlightkid.github.io/python-rtmidi/). Then you'll need pair your wiimote to your computer and detirmine which event file corrisponds to the drums (the wiimote buttons and the drums are different events). Then simply run main.py and enter that number. If you wish to change the midi notes, you'll have to change the values in main.py.

In main.py you can ajust the default parameters relating to velocity, such as the default minimum, or the streangth of velocity smoothing. You can change the midi notes, and velocity scaling for each button. The default mapping is intended for [avldrums](http://x42-plugins.com/x42/x42-avldrums).

If you are using a controller other than the guitar hero drums, define each of your buttons as a "control" class object, and add them to the lsControl list

# Notes
Nothing here is specific to jack audio, and rtmidi is supposed to support alsa midi aswell, though this is untested.
