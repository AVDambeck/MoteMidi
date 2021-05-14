# MoteMidi
Use wii peripherals to send midi data

MoteMidi reads /dev/inpout/eventX to interface with input devices. Was made with the intension of using [Guitar Hero World Tour drums](https://en.wikipedia.org/wiki/Guitar_Hero_World_Tour#Drums) plugged into a Nintendo Wiimote. 

# Usage
The project is in very early devlopment. You'll first need to make sure you have [evdev](https://python-evdev.readthedocs.io/en/latest/) and [rtmidi](https://spotlightkid.github.io/python-rtmidi/). Then you'll need pair your wiimote to your computer and detirmine which event file corrisponds to the drums (the wiimote buttons and the drums are different events). Then simply run main.py and enter that number. If you wish to change the midi notes, you'll have to change the values in main.py.
