print("this is a first draft. Midi off has not been sent. Only play terminal sounds or have a midi panic ready")

#import
import evdev
import rtmidi
import time
import sys

#establish midi port
midiout = rtmidi.MidiOut()
midiout.open_virtual_port()

#initiate gamepad
print("Select /dev/input/event number")
gamepadLoc = "/dev/input/event" + str(input())
gamepad = evdev.InputDevice(gamepadLoc)
print("selected " + str(gamepad))



#class for each physical button
class Input(object):
    def __init__(self, code, type, message="debug", note="1"):
        #type 0 = dummy, 1 = midi, 2 = controls
        self.code = code
        self.type = type
        self.message = message
        self.note = note

    #input.payload is intended to be run when the button is pressed. depends on button type
    def payload(self, val=0):
        #midi - play slef.note
        if self.type == 1:
            #if the pressure isnt 0 play note
            if val = 1:
                print(self.message + str(val))
                note_on = [0x90, self.note, 64]
                midiout.send_message(note_on)
            else:
                pass
        elif self.type == 2:
            if

        else:
            print(self.message + str(val))

# define all the notes

PadGreen = Input(18, 1, "green", 45)
PadBlue = Input(17, 1, "blue", 56)
PadRed = Input(16, 1, "red", 38)
PadYellow = Input(20, 1, "yello", 42)
PadOrange = Input(21, 1, "orange", 64)
Pedal = Input(22, 1, "pedal", 36)
StickX = Input(0, 2, "StickX", 1)
StickY = Input(1, 2, "StickY", 2)

lsInput = [PadGreen, PadBlue, PadRed, PadYellow, PadOrange, StickX, StickY, Pedal]


#main
for event in gamepad.read_loop():
    #read gamepad
    if event.type == evdev.ecodes.EV_KEY:
        print(event)
    elif event.type == evdev.ecodes.EV_ABS:
        #if event.value !=0:
        for i in lsInput:
            if event.code == i.code:
                i.payload(event.value)



print("this was supposed to stop the program :/")
sys.exit()
