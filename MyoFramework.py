# MyoFramework.py
# Written by Gabriel Antoniak for Duke eNable
# First draft on 11/25/2017

# Set up control framework for Rasberry Pi - Arduino communication
# Rasberry Pi acts as the brain and tells Arduino which grip pattern
# is required.  Rasberry Pi then awaits for response from the Arduino
# before sending another signal. Framework rests for now on sending
# a random integer value in the set of [1, 3] to the Arduino, corresponding
# to the 3 possible grip patterns (open, grab, pinch). Myoband sensing
# and neural network still has to be added to the code for actual sensing,
# rather than random integer value.

import serial
from random import randint
from time import sleep

# Port depends on in which USB the Arduino is plugged into.
# For Rasberry Pi, it's of the form /dev/tty/ACM%d, where %d is an integer [0, 4]
# For computer, it is simply the COM port number (1 or 2 or 3, etc.)

ser = serial.Serial('/dev/ttyACM1', 9600)
optionVal = 0  # initial key value, get data from Myo band


def getFromArduino():      # method to recieve integer signal from Arduino
    byte_data = ser.readline()
    ser_data = byte_data.decode('utf-8')
    list_data = ser_data.split()
    strVal = ''.join(list_data)
    intVal = int(strVal)
    return intVal


def waitForArduino():  # method to wait for Arduino signal
    global optionVal

    print('Waiting')
    readVal = getFromArduino()
    if (readVal == 0):
        optionVal = 0  # changes key from 4 (waiting) to 0 (get Myo Data)

    return


def sendToArduino():  # send current key value to the Arduino
        ser.write(str(optionVal).encode())


def pinchSignal():  # send key value for pinching to Arduino, and wait for response
    global optionVal

    print('Pinch Grip')
    sendToArduino()
    optionVal = 4
    return


def grabSignal():  # analogous to above but with grab signal
    global optionVal

    sendToArduino()
    optionVal = 4
    return


def openSignal():  # analogous to above but with open signal
    global optionVal

    print('Open Signal')
    sendToArduino()
    optionVal = 4
    return

def getMyoSignal():  # placeholder function, random integer corresponding to the three states
    global optionVal

    print('Getting MYO Data')
    sleep(2)  # delay to make lights easier to follow
    myoSignal = randint(1, 3)
    optionVal = myoSignal
    return


# create dicitionary for each of the possible functions of the Rasberry Pi brain
options = {0: getMyoSignal,
           1: openSignal,
           2: pinchSignal,
           3: grabSignal,
           4: waitForArduino,
           }

#dictionary will always go in the following manner:
# 0 ---> 1 OR 2 OR 3 --> 4 --> 0 --> 1 OR 2 OR 3 --> 4 ....

# ensure the program runs in a constant loop for all time
while 1:
    options[optionVal]()
