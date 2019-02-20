import sys
from phue import Bridge
import datetime
import time
import RPi.GPIO as GPIO
import logging
logging.basicConfig()
sys.path.append("/home/pi/.local/lib/python2.7/site-packages")

# This code will run each time the Pi reboots, wait 30 sec for Pi to boot and get connected to the network before attempting to connect to the Philips Hue Bridge
print 'Waiting for network...'
time.sleep(30)  # Change this to wait
print 'The wait is over. It\'s showtime!'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN)
b = Bridge('192.168.1.151')
try:
    b.connect()
except ImportError:
    print "Import error occurred!"
print "Connected to Hue bridge!"

# This sets times of a day (I guess I should use scheduler here but whatever)
day = datetime.time(8, 0, 0)
evening = datetime.time(16, 0, 0)
night = datetime.time(21, 0, 0)
midnight = datetime.time(23, 59, 59)
afterMidnight = datetime.time(0, 0, 0)

# Check if lights are already on
lightson = b.get_light(1, 'on')
if lightson:
    print "Lights are already on."

j = 0
k = 0

# This is the main functionality, it turns the lights on and off.
# Parameter changes the brightness between 1 to 254
def lightUp(brightness, group):
    global j
    global lightson
    global k
    if i == 1:
        j = j+1
        print datetime.datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"), ": Activity detected ", j, "time(s)."

        if j == 2:
            print "Lights will be on for 2 minutes"
            # Replace the number 3 with the light group number defined on Philips Hue.
            b.set_group(group, 'on', True)
            b.set_group(group, 'bri', brightness)

            lightson = True
            j = 0
            # Let the lights run at least 2 minutes (120 seconds) once they are on
            time.sleep(120)
        time.sleep(1)
        k = 0
    elif i == 0:
        if lightson == True:
            k = k+1
            print datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"), ": No activity detected."
            if k == 2:
                print datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"), ": Lights will go off"
                # Replace the number 3 with the light group number defined on Philips Hue.
                # b.set_group(
                #     3, 'on', False)
                b.set_group(group, 'on', False)
                lightson = False
                k = 0
        else:
            print "Lights are already off. No command was sent."
        j = 0
        # Don't sleep too much if lights are off, keep looking for motion. Increasing this value makes the motion sensor respond slower.
        time.sleep(2)

print 'Entering infinite loop...'
while True:
    i = GPIO.input(16)
    # Since 8 till 16 be inactive
    # Since 16 till 21 turn on 50%
    # Since 21 till Midnight turn on 25%
    # Since Midnight till 8 turn on 10%
    timestamp = datetime.datetime.now().time()
    if (timestamp > evening and timestamp < night):
        print "Evening, 50% Active"
        lightUp(127, 3)  # 50% lights between 16 - 21

    elif (timestamp > night and timestamp < midnight):
        print "Nighttime, 25% Active"
        lightUp(64, 3)  # 25% lights between 21 - Midnight

    elif(timestamp > afterMidnight and timestamp < day):
        print "After midnight, 10% Active"
        lightUp(26, 3)  # 10% lights between midnight - 8

    else:
        print "Daytime, inactive"
        time.sleep(60)  # sleep a lot more during daytime/bedtime
