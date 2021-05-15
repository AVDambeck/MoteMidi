#Python function that lists devices
from evdev import InputDevice, categorize, ecodes
import os

dev = ""
longPrompt = True

#gamepad function
def getGamepad(test):
    global dev
    global longPrompt
    try:
        dev = InputDevice("/dev/input/event" + str(test))
    except:
        if longPrompt == True:
            print("Could not access input device /dev/input/event" + str(test) + " You might not have permisson or it might not exist. Try another.")
            longPrompt = False
        else:
            print("Could not access input device./dev/input/event" + str(test))
    else:
        print(dev)

def list():
    #get highest event
    for i in os.listdir("/dev/input"):
        if "event" in i:
          max = int(i.replace("event", ""))
          break

    #list events
    for i in range(1,max):
        getGamepad(i)


#exit
#del dev
#exit()
