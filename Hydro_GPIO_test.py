import sys
import time
import RPi.GPIO as GPIO         #import IO module
from flask import Flask
from flask import jsonify
from requests import get
import json

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





#Execute Main Program
app = Flask(__name__)



@app.route("/")
def main():
    while True:
    if (GPIO.input(22)==False):
        blink(sprinklerValue(12))
        sprinklerValue = str("Calculated sprinkler value is: "+ str(SprinklerValue(12)))
        temperature = str("Average Temperature: " + str(AverageWeather('t',12)) + " degrees")
        humidity = str("Average Air Humidity: " + str(AverageWeather('r',12)) + "%")
        windSpeed = str("Average Wind Speed: " + str(AverageWeather('ws',12)) + " m/s")
        precipitation = str("Average Precipitation: " + str(AverageWeather('pmean',12)) + "mm")
        return jsonify(sprinklerValue, temperature, humidity, windSpeed, precipitation)
    else: 
        return ""
    

url = 'https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/16.158/lat/58.5812/data.json'
weatherData = get(url).json()['timeSeries']

def AverageWeather(name, timePeriod):
  nestedObjects = 18
  weatherValue = 0
  for i in range(timePeriod):
    for j in range(nestedObjects):
      if (weatherData[i]['parameters'][j]['name'] == name):
        weatherValue = weatherValue+(weatherData[i]['parameters'][j]['values'][0])
  return (weatherValue/timePeriod)


def SprinklerValue(timePeriod):
  SprinklerValue = 1
  if AverageWeather('r',timePeriod)>65:
    SprinklerValue = SprinklerValue - 0.25
  if AverageWeather('t',timePeriod)>24:
    SprinklerValue = SprinklerValue + 0.25
  if AverageWeather('ws',timePeriod)>8:
    SprinklerValue = SprinklerValue - 0.5
  if AverageWeather('pmean',timePeriod)>0.2:
    SprinklerValue = 0
  return SprinklerValue

def blink(sprinklerValue):
    blink_amount = round((sprinklerValue)*10)
    for i in range(blink_amount):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        
GPIO.cleanup()                  #close all output ports

if __name__== '__main__':
    app.run()

