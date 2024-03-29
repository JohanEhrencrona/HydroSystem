from flask import Flask
from flask import jsonify
from requests import get
import json


app = Flask(__name__)



@app.route("/")
def main():
    sprinklerValue = str("Calculated sprinkler value is: "+ str(SprinklerValue(12)))
    temperature = str("Average Temperature: " + str(AverageWeather('t',12)) + " degrees")
    humidity = str("Average Air Humidity: " + str(AverageWeather('r',12)) + "%")
    windSpeed = str("Average Wind Speed: " + str(AverageWeather('ws',12)) + " m/s")
    precipitation = str("Average Precipitation: " + str(AverageWeather('pmean',12)) + "mm")
    return jsonify(sprinklerValue, temperature, humidity, windSpeed, precipitation)
    

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


