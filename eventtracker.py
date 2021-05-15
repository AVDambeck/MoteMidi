#import
from evdev import InputDevice, categorize, ecodes
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import eventlist

run = True
dev = ""
longPrompt = True

#gamepad function
def getGamepad(test):
    global run
    global dev
    global longPrompt
    try:
        dev = InputDevice("/dev/input/event" + str(test))
    except:
        if longPrompt == True:
            print("Could not use input device. You might not have permisson or it might not exist. Try another.")
            longPrompt = False
        else:
            print("Could not use input device.")

    else:
        print('#' * 80)
        print(dev)
#        print("press q to quit")
        print('#' * 80)
        run = False

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




for event in dev.read_loop():
    print(categorize(event))
#    if q is pressed
#        break

del dev
exit()
