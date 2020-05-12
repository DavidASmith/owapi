# -*- coding: utf-8 -*-
import os
import requests
from pandas import json_normalize
from pandas import to_datetime


def get_api_key():
    return(os.environ.get('OPENWEATHERAPIKEY'))

def set_api_key(api_key):
    os.environ['OPENWEATHERAPIKEY'] = api_key
    
def get_current_and_forecast(lat, lon):
    
    url = "https://api.openweathermap.org/data/2.5/onecall"
    
    params = {
        "lat": lat, 
        "lon": lon,
        "units": "metric",
        "appid": get_api_key()
        }
    
    response = requests.get(url, 
                            params = params)
    
    data = response.json()
      
    return(data)


def get_current_obs(lat, lon):
    current_forecast_response = get_current_and_forecast(lat, lon)

    current = json_normalize(current_forecast_response['current'])
    current.dt = (to_datetime(current.dt, unit='s'))
    current.sunrise = (to_datetime(current.sunrise, unit='s'))
    current.sunset = (to_datetime(current.sunset, unit='s'))
    return(current)

def get_daily_forecast(lat, lon):
    current_forecast_response = get_current_and_forecast(lat, lon)

    daily = json_normalize(current_forecast_response['daily'])
    
    return(daily)