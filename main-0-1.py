import evdev
import rtmidi
import time

midiout = rtmidi.MidiOut()
midiout.open_virtual_port("MoteMidi")

gamepad = evdev.InputDevice('/dev/input/event22')
print(gamepad)

class Input(object):
    def __init__(self, code, type, message="debug", note="1"):
        #type 0 = dummy, 1 = midi
        self.code = code
        self.type = type
        self.message = message
        self.note = note

    def payload(self, val=0):
        if self.type == 1:
            if val != 0:
                print(self.message + str(val))
                note_on = [0x90, self.note, 127]
                midiout.send_message(note_on)
            else:
                pass
        else:
            print(self.message + str(val))

PadGreen = Input(18, 1, "green", 45)
PadBlue = Input(17, 1, "blue", 56)
PadRed = Input(16, 1, "red", 38)
PadYellow = Input(20, 1, "yello", 42)
PadOrange = Input(21, 1, "orange", 64)
Pedal = Input(22, 1, "pedal", 36)
StickX = Input(0, 0, "StickX")
StickY = Input(1, 0, "StickY")

lsInput = [PadGreen, PadBlue, PadRed, PadYellow, PadOrange, StickX, StickY, Pedal]

for event in gamepad.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        print(event)
    elif event.type == evdev.ecodes.EV_ABS:
        #if event.value !=0:
        for i in lsInput:
            if event.code == i.code:
                i.payload(event.value)
