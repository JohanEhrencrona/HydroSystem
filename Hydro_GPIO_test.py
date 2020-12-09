import sys
import random
#from graphics import *
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


def turn_on_water(selection):
    print()
    print("water lawn", selection)
    print()
    GPIO.output(ports[4], GPIO.HIGH)
 
 
def turn_off_water(selection):
    print()
    print("stop water lawn", selection)
    print()
    GPIO.output(ports[4], GPIO.LOW)
    

def turn_on_light(selection):
    print()
    print("turn on light", selection)
    print()
    
def turn_off_light(selection):
    print()
    print("turn off light", selection)
    print()
    
def blink_random(selection):
    print()
    print("turn on light", selection)
    print()
    port = random.randint(FIRST_PORT, LAST_PORT-1)
    print(port)
    GPIO.output(ports[port], GPIO.LOW)
    sleep(2)
    print()
    print("turn off light", selection)
    print()
    GPIO.output(ports[port], GPIO.HIGH)
    

def input_data():
    ask_for_input=True
    print("Här kan du styra ditt smarta hem")
    while ask_for_input == True:
        print("1. Vatten på: Gräsmattan vid altan mot vattnet")
        print("2. Vatten av: Gräsmattan vid altan mot vattnet")
        print("3. Vatten på: Gräsmattan vid altan mot altan")
        print("4. Vatten av: Gräsmattan vid altan mot altan")
        print("5. Vatten på: Buskarna på baksidan av huset")
        print("6. Vatten av: Buskarna på baksidan av huset")
        print("7. Vatten på: Gräsmattan mot gatan")
        print("8. Vatten av: Gräsmattan mot gatan")
        print("9. Vatten på: Växtlådorna")
        print("10.Vatten av: Växtlådorna")
        print("11.Tända lampa.......")
        print("12.Släck lampa.......")
        print("13. Avsluta")
        try:
            selection = int(input("Vad vill du göra ? "))
        except ValueError:
            print("Oops! Value error")
        if selection in (1,3,5,7,9):
            turn_on_water(selection)
        elif selection in (2,4,6,8,10):
            turn_off_water(selection)
        elif selection == 11:
            turn_on_light(selection)
        elif selection == 12:
            turn_off_light(selection)
        elif selection == 13:
            ask_for_input = False
            print()
            print("Programmet avslutas")
        else:
            print()
            print("ditt val fans inte")
            print("")
    return selection
   
    
#function that turn all lights on or off
def turn_all_lights(x):
    if (x == ON):
        for port in range(FIRST_PORT, LAST_PORT):
            GPIO.output(ports[port], GPIO.HIGH)
            print(port)
        print("All On")
    else:
        for port in range(FIRST_PORT, LAST_PORT):
            GPIO.output(ports[port], GPIO.LOW)
        print("All Off")

#function that turn one lights on or off
def turn_one_light(x, i):
    if (x == ON):
        GPIO.output(ports[i], GPIO.HIGH)
    else:
        GPIO.output(ports[i], GPIO.LOW)
        
        
def blink_all_lights_one_by_one():
    for i in range(FIRST_PORT, LAST_PORT):
        if button == NOT_PRESSED:
                 print("port used:", ports[i],i)
                 turn_one_light(ON, i)
                 sleep(TIME1)
                 turn_one_light(OFF, i)
                 sleep(TIME1)
                 
        
def blink_all_lights_same_time():       
  for i in range (0, 4):           #pulse all
    turn_all_lights(ON)
    sleep(TIME2)
    turn_all_lights(OFF)
    sleep(TIME2)      
        
               

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



