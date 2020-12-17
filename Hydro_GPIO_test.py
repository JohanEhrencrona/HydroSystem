import sys
import time
import RPi.GPIO as GPIO         #import IO module
from flask import Flask
from flask import render_template
from flask import jsonify
from requests import get
import json
from flask_socketio import SocketIO



#Execute Main Program
app = Flask(__name__)




url = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/13.929/lat/55.473/data.json'
weatherData = get(url).json()['timeSeries']




@app.route('/')
def index():
    initiate_GPIO()
    moistureZone1 = {
        'buttonPress': soilMoistureZone1()
        }
    weatherZone1 ={
        'temperature': AverageWeather('t',12),
        'humidity': AverageWeather('r',12),
        'windSpeed': AverageWeather('ws',12),
        'precipitation': AverageWeather('pmean',12),
        'sprinklerValue': SprinklerValueZone1(12)
        }
    moistureZone2 = {
        'buttonPress': soilMoistureZone2()
        }
    weatherZone2 ={
        'temperature': AverageWeather('t',12),
        'humidity': AverageWeather('r',12),
        'windSpeed': AverageWeather('ws',12),
        'precipitation': AverageWeather('pmean',12),
        'sprinklerValue': SprinklerValueZone2(12)
        }
    moistureZone3 = {
        'buttonPress': soilMoistureZone3()
        }
    weatherZone3 ={
        'temperature': AverageWeather('t',12),
        'humidity': AverageWeather('r',12),
        'windSpeed': AverageWeather('ws',12),
        'precipitation': AverageWeather('pmean',12),
        'sprinklerValue': SprinklerValueZone3(12)
        }
    moistureZone4 = {
        'buttonPress': soilMoistureZone4()
        }
    weatherZone4 ={
        'temperature': AverageWeather('t',12),
        'humidity': AverageWeather('r',12),
        'windSpeed': AverageWeather('ws',12),
        'precipitation': AverageWeather('pmean',12),
        'sprinklerValue': SprinklerValueZone4(12)
        }
    return render_template('index.html', weatherZone1 = weatherZone1, moistureZone1 = moistureZone1, weatherZone2 = weatherZone2, moistureZone2 = moistureZone2, weatherZone3 = weatherZone3, moistureZone3 = moistureZone3, weatherZone4 = weatherZone4, moistureZone4 = moistureZone4)


def soilMoistureZone1():
    while True:
        if (GPIO.input(22)==False):
            GPIO.output(18, GPIO.HIGH)
            time.sleep(0.6)
            GPIO.output(18, GPIO.LOW)
            return "Soil dry"
            time.sleep(2)
        if (GPIO.input(22)==True):
            return "Soil moist"
        time.sleep(2)
def soilMoistureZone2():
    while True:
        if (GPIO.input(27)==False):
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.6)
            GPIO.output(23, GPIO.LOW)
            return "Soil dry"
            time.sleep(2)
        if (GPIO.input(27)==True):
            return "Soil moist"
        time.sleep(2)

def soilMoistureZone3():
    while True:
        if (GPIO.input(17)==False):
            GPIO.output(24, GPIO.HIGH)
            time.sleep(0.6)
            GPIO.output(24, GPIO.LOW)
            return "Soil dry"
            time.sleep(2)
        if (GPIO.input(17)==True):
            return "Soil moist"
        time.sleep(2)

def soilMoistureZone4():
    while True:
        if (GPIO.input(4)==False):
            GPIO.output(25, GPIO.HIGH)
            time.sleep(0.6)
            GPIO.output(25, GPIO.LOW)
            return "Soil dry"
            time.sleep(2)
        if (GPIO.input(4)==True):
            return "Soil moist"
        time.sleep(2)


def initiate_GPIO():
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
    


def AverageWeather(name, timePeriod):
  nestedObjects = 18
  weatherValue = 0
  for i in range(timePeriod):
    for j in range(nestedObjects):
      if (weatherData[i]['parameters'][j]['name'] == name):
        weatherValue = weatherValue+(weatherData[i]['parameters'][j]['values'][0])
  return (weatherValue/timePeriod)


def SprinklerValueZone1(timePeriod):
    ##Tomatoe
  SprinklerValue = 1

  if AverageWeather('r',timePeriod)>65:
      SprinklerValue = SprinklerValue - 0.25
  if AverageWeather('t',timePeriod)>24:
      SprinklerValue = SprinklerValue + 0.25
  if AverageWeather('ws',timePeriod)>8:
      SprinklerValue = SprinklerValue - 0.5
  if AverageWeather('pmean',timePeriod)>0.2:
      SprinklerValue = 0
  if soilMoistureZone1() == 'Soil moist':
      SprinklerValue = 0
  return SprinklerValue

def SprinklerValueZone2(timePeriod):
    ##Potatoe
  SprinklerValue = 1

  if AverageWeather('r',timePeriod)>65:
      SprinklerValue = SprinklerValue - 0.25
  if AverageWeather('t',timePeriod)>2:
      SprinklerValue = SprinklerValue + 0.25
  if AverageWeather('ws',timePeriod)>8:
      SprinklerValue = SprinklerValue - 0.5
  if AverageWeather('pmean',timePeriod)>0.5:
      SprinklerValue = 0
  if soilMoistureZone2() == 'Soil moist':
      SprinklerValue = 0
  return SprinklerValue

def SprinklerValueZone3(timePeriod):
    #Carrot
  SprinklerValue = 1

  if AverageWeather('r',timePeriod)>65:
      SprinklerValue = SprinklerValue - 0.25
  if AverageWeather('t',timePeriod)>24:
      SprinklerValue = SprinklerValue + 0.25
  if AverageWeather('ws',timePeriod)>8:
      SprinklerValue = SprinklerValue - 0.5
  if AverageWeather('pmean',timePeriod)>0.5:
      SprinklerValue = 0
  if soilMoistureZone3() == 'Soil moist':
      SprinklerValue = 0
  return SprinklerValue

def SprinklerValueZone4(timePeriod):
    ##Corn
  SprinklerValue = 1

  if AverageWeather('r',timePeriod)>65:
      SprinklerValue = SprinklerValue - 0.25
  if AverageWeather('t',timePeriod)>24:
      SprinklerValue = SprinklerValue + 0.25
  if AverageWeather('ws',timePeriod)>8:
      SprinklerValue = SprinklerValue - 0.5
  if AverageWeather('pmean',timePeriod)>0.2:
      SprinklerValue = 0
  if soilMoistureZone4() == 'Soil moist':
      SprinklerValue = 0
  return SprinklerValue

def blink(sprinklerValue):
    blink_amount = round((sprinklerValue)*10)
    for i in range(blink_amount):
        GPIO.output(18, GPIO.HIGH)
        print("gh")
        time.sleep(0.6)
        GPIO.output(18, GPIO.LOW)
        print("bbbbb")
    return ""
        
        

if __name__ == "__main__":
    app.run(ssl_context='adhoc')
            



