import sys
import random
#from graphics import *
import time
import RPi.GPIO as GPIO         #import IO module
print("GPIO version = ", GPIO.VERSION)

#initiate IO Module
GPIO.setmode(GPIO.BCM)          #set pin numbering according to broadcom chip
GPIO.setwarnings(False)         #turn off warnings

#assign IO ports
GPIO.setup(18, GPIO.OUT)         #GPIO assign output
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
ports =[18, 23, 24, 25]   #string with the output port numbers
GPIO.setup(22, GPIO.IN)          #GPIO no 26 assigned as input
GPIO.setup(27, GPIO.IN)          #GPIO no 26 assigned as input
GPIO.setup(17, GPIO.IN)          #GPIO no 26 assigned as input
GPIO.setup(4, GPIO.IN)          #GPIO no 26 assigned as input

#assign constant values to variables
ON = 0
OFF = 1
FIRST_PORT  =0
LAST_PORT = (len(ports))           # CHECK LOOPS WHERE I USE LAST_PORT
print("last port is", LAST_PORT)
NOT_PRESSED = False
PRESSED = True


def blink(sprinklerValue):
    blink_amount = round((sprinklerValue)*10)
    for i in range(blink_amount):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)



def soil_is_moist():
    print("soil is moist")



#Execute Main Program

while True:
    if (GPIO.input(22)==False):
        blink(0.3)
    
    





GPIO.cleanup()                  #close all output ports



