import sys
import random
from time import sleep
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


   
  

#function that turn one lights on or off
def turn_one_light(x, i):
    if (x == ON):
        GPIO.output(ports[i], GPIO.HIGH)
    else:
        GPIO.output(ports[i], GPIO.LOW)
   
               
#function for setting button pressed +++++ GLOBAL VARIABLES ++++++
def set_button_pressed(channel):
    global button
    global eventport
    button = PRESSED
    eventport = channel
    print("EVENT DETECTED ON PORT:", eventport)

    

#Initiate Main Program
TIME1 = 0.5
TIME2 = 0.3
turn_all_lights(OFF)
button = NOT_PRESSED
GPIO.add_event_detect(22, GPIO.FALLING, callback=set_button_pressed, bouncetime = 300) #interrupt detection
GPIO.add_event_detect(27, GPIO.FALLING, callback=set_button_pressed, bouncetime = 300) #interrupt detection
GPIO.add_event_detect(17, GPIO.FALLING, callback=set_button_pressed, bouncetime = 300) #interrupt detection
GPIO.add_event_detect(4, GPIO.FALLING, callback=set_button_pressed, bouncetime = 300) #interrupt detection

#Execute Main Program

while button == NOT_PRESSED:
    blink_all_lights_one_by_one()
blink_all_lights_same_time()

selection=input_data()
print(selection)

turn_all_lights(ON)

blink_random(1)



GPIO.cleanup()                  #close all output ports



