#!python3
print("this is a first draft. Midi off has not been sent. Only play terminal sounds or have a midi panic ready")

#import
import evdev, rtmidi, time
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import eventlist

#establish midi port
midiout = rtmidi.MidiOut(name="MoteMidi")
midiout.open_virtual_port("events-out")

#declairing variables
run = True
gamepad = ""
longPrompt = True

#define gamepad function
def getGamepad(test):
    global run
    global gamepad
    global longPrompt
    try:
        gamepad = evdev.InputDevice("/dev/input/event" + str(test))
    except:
        if longPrompt == True:
            print("Could not access input device /dev/input/event" + str(test) + " You might not have permisson or it might not exist. Try another.")
            longPrompt = False
        else:
            print("Could not access input device./dev/input/event" + str(test))
    else:
        print('#' * 80)
        print(gamepad)
#        print("press q to quit")
        print('#' * 80)
        run = False


#define class for each physical button
class Control(object):
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
            if val != 0:
                print(self.message + str(val))
                note_on = [0x90, self.note, 64]
                midiout.send_message(note_on)
            else:
                pass
        elif self.type == 2:
            pass

        else:
            print(self.message + str(val))


# define all the notes

PadGreen = Control(18, 1, "green", 45)
PadBlue = Control(17, 1, "blue", 40)
PadRed = Control(16, 1, "red", 38)
PadYellow = Control(20, 1, "yello", 42)
PadOrange = Control(21, 1, "orange", 61)
Pedal = Control(22, 1, "pedal", 36)
StickX = Control(0, 2, "StickX", 1)
StickY = Control(1, 2, "StickY", 2)

lsControl = [PadGreen, PadBlue, PadRed, PadYellow, PadOrange, StickX, StickY, Pedal]



#START

#get event numbers
print('#' * 80)
print("""Select /dev/input/event number (enter "list" to scan)""")
print('#' * 80)
while run == True:
    num = input()

    #cycle exception
    if num == "list":
        eventlist.list()
        print
        print('#' * 80)
        print("""Select /dev/input/event number""")
        print('#' * 80)

    else:
        getGamepad(num)

#main
for event in gamepad.read_loop():
    #read gamepad
    if event.type == evdev.ecodes.EV_KEY:
        print(event)
    elif event.type == evdev.ecodes.EV_ABS:
        #if event.value !=0:
        for i in lsControl:
            if event.code == i.code:
                i.payload(event.value)


del gamepad
del midiout
sys.exit()
