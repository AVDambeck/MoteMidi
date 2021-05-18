#!python3
print("this is a first draft. Midi off has not been sent. Only play terminal sounds or have a midi panic ready")

#import
import evdev, rtmidi, time, random, asyncio
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import eventlist, vel

#establish midi port
midiout = rtmidi.MidiOut(name="MoteMidi")
midiout.open_virtual_port("events-out")

#declairing variables
run = True
gamepad = ""
longPrompt = True

#global configs
#note length (seconds)
defaultLength = 1

#velocity defaults
defaultMax = 127
defaultMin = 10
defaultMode = "linear"
defaultSteps = 7

#velocity manipulation
smooth = True
#higher will favor the new velocity. >1 will accent changes in velocity. <0 will crash
smoothWeight = 0.5
#final velocity = velocity + plus or minus up to velrandomize
velRandomize = 3

#velocity bounds
velAbsMin = 10
velAbsMax = 127

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


#note off-inator class
lsActiveNotes = []
class noteKiller(object):
    def __init__(self):
        self.length = 0
        self.note = 1
        self.channel = 1
        self.start = 0
        self.active = False
        #add self to list
        global lsActiveNotes
        lsActiveNotes.append(self)


    def set(self, length, note, channel=1):
        #write down the time
        self.length = length
        self.note = note
        self.channel = channel
        self.start = time.time()
        self.active = True
        print(str(self.channel) + " set!")

    def tryEnd(self, velocity=0):
        #if self is too old, send off command and remove from list
        if time.time() - self.start > self.length and self.active == True:
            #remove note
            note_off = [127+self.channel, self.note, 1]
            midiout.send_message(note_off)
            self.active = False
            print("killed " + str(self.channel))
            #remove list
            #global lsActiveNotes
            #lsActiveNotes.remove(self)



#define class for each physical button

lsControl = []
class Control(object):
    def __init__(self, code, type, message="debug", note=1, channel=1, length=defaultLength, velInfo=[defaultSteps, defaultMin, defaultMax, defaultMode]):
        #type 0 = dummy, 1 = midi, 2 = controls
        self.code = code
        self.type = type
        self.message = message
        self.note = note
        self.length = length
        self.channel  = channel
        self.velInfo = velInfo
        self.noteKiller = noteKiller()

        self.oldVel = vel.curve(self.velInfo[0]/2, self.velInfo[0], self.velInfo[1], self.velInfo[2], self.velInfo[3])

        global lsControl
        lsControl.append(self)


    #input.payload is intended to be run when the button is pressed. depends on button type
    def payload(self, val=0, offVel=0):
        #midi - play slef.note
        if self.type == 1:
            #if the pressure isnt 0 play note
            if val != 0:

                #deterimin velocity
                velocity = vel.curve(val, self.velInfo[0], self.velInfo[1], self.velInfo[2], self.velInfo[3])

                #this if statement avoids crashing because of an "empty range". I think randomrange(0, 0) should always return zero but oh well.
                if velRandomize != 0:
                    velocity = vel.trunc(velocity + random.randrange(-velRandomize, velRandomize))

                if smooth == True:
                    velocity = vel.trunc((smoothWeight*velocity)+((1-smoothWeight)*self.oldVel))

                #keep in range
                velocity = vel.trunc(velocity, velAbsMin, velAbsMax)


                #end previos note
                note_off = [(127+self.channel), self.note, offVel]
                midiout.send_message(note_off)

                #actually play the note
                print(self.message + str(val) + " - " + str(velocity))
                note_on = [(143+self.channel), self.note, velocity]
                midiout.send_message(note_on)
                # note velocty for smoothing
                self.oldVel = velocity
                # set note to be turned off
                self.noteKiller.set(self.length, self.note, self.channel)

            else:
                pass
        elif self.type == 2:
            #analog stick
            pass
        elif self.type == 3:
            #digital buttons
            print(self.message)

        else:
            print(self.message + str(val))

    def EndNote(self):
        note_off = [(127+self.channel), self.note, offVel]
        midiout.send_message(note_off)


# define all the notes

lightCurve = [defaultSteps, 40, 200, defaultMode]
heavyCurve = [defaultSteps, -40, 116, defaultMode]



#name = Control(device code, 1 (midi mode), "message", midi note, midi channe, velocity curve info)

#avldrum kit
PadRed = Control(16, 1, "red", 38, 1, lightCurve)
PadBlue = Control(17, 1, "blue", 40, 1, lightCurve)
PadGreen = Control(18, 1, "green", 45, 1, lightCurve)
PadYellow = Control(20, 1, "yello", 42, 1)
PadOrange = Control(21, 1, "orange", 60, 1, heavyCurve)
Pedal = Control(22, 1, "pedal", 36, 1, lightCurve)

#channel mode
#PadRed = Control(16, 1, "red", 64, 1, defaultLength, lightCurve)
#PadBlue = Control(17, 1, "blue", 64, 2, defaultLength, lightCurve)
#PadGreen = Control(18, 1, "green", 64, 3, defaultLength, lightCurve)
#PadYellow = Control(20, 1, "yello", 64, 4)
#PadOrange = Control(21, 1, "orange", 64, 5, defaultLength, heavyCurve)
#Pedal = Control(22, 1, "pedal", 64, 6, defaultLength, lightCurve)

StickX = Control(0, 2, "StickX", 1)
StickY = Control(1, 2, "StickY", 2)

Minus = Control(314, 3, "Minus Button", 1)
Plus = Control(315, 3, "Plus Button", 2)



#Player
async def player():
    #for event in gamepad.read_loop():
    async for event in gamepad.async_read_loop():
        #read gamepad
        #if event.type == evdev.ecodes.EV_KEY:
            #print(event)
        #elif event.type == evdev.ecodes.EV_ABS:
            #pass

        #if the event has a control tied to it, run that controls payload (play it's note)
        for i in lsControl:
            #await asyncio.sleep(0)
            if event.code == i.code:
                i.payload(event.value)
        await asyncio.sleep(0)

#Killer
killerRun = True
async def killer():
    while killerRun == True:
        #print("looped!")
        await asyncio.sleep(0)
        for i in lsActiveNotes:
            i.tryEnd()

#Main
async def main():
    await asyncio.gather(
        killer(),
        player()
    )

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
asyncio.run(main())





#close
for i in lsControl:
    i.EndNote()

del gamepad
del midiout
sys.exit()
