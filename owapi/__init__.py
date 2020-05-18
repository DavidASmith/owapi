# -*- coding: utf-8 -*-
import os
import requests
import pandas as pd
from time import mktime
import datetime

def get_api_key():
    key = os.environ.get('OPENWEATHERAPIKEY')
    if key is None:
        raise ValueError('API key is not set.')
    return(key)

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


    current_weather_info = pd.json_normalize(current_forecast_response['current'],
                             record_path = 'weather', 
                             record_prefix = 'weather_')
    
    current_weather = pd.DataFrame(current_forecast_response['current'])
    current_weather = current_weather.drop('weather', axis = 1)
    current_weather = pd.concat([current_weather, current_weather_info], axis = 1)
    
    current_weather.dt = (pd.to_datetime(current_weather.dt, unit='s'))
    current_weather.sunrise = (pd.to_datetime(current_weather.sunrise, unit='s'))
    current_weather.sunset = (pd.to_datetime(current_weather.sunset, unit='s'))
    return(current_weather)



def get_daily_forecast(lat, lon):
    current_forecast_response = get_current_and_forecast(lat, lon)

    daily_weather_info = pd.json_normalize(current_forecast_response['daily'],
                             record_path = 'weather', 
                             record_prefix = 'weather_')

    daily_forecast = pd.json_normalize(current_forecast_response['daily'], 
                                       sep = '_')
    daily_forecast = daily_forecast.drop('weather', axis = 1)
    daily_forecast = pd.concat([daily_forecast, daily_weather_info], axis = 1)
    
    
    daily_forecast.dt = pd.to_datetime(daily_forecast.dt, unit = 's').dt.date
    daily_forecast.sunrise = pd.to_datetime(daily_forecast.sunrise, unit = 's')
    daily_forecast.sunset = pd.to_datetime(daily_forecast.sunset, unit = 's')
    
    return(daily_forecast)


def get_hourly_forecast(lat, lon):
    current_forecast_response = get_current_and_forecast(lat, lon)

    hourly_weather_info = pd.json_normalize(current_forecast_response['hourly'],
                             record_path = 'weather', 
                             record_prefix = 'weather_')

    hourly_forecast = pd.json_normalize(current_forecast_response['hourly'], 
                                       sep = '_')
    hourly_forecast = hourly_forecast.drop('weather', axis = 1)
    hourly_forecast = pd.concat([hourly_forecast, hourly_weather_info], axis = 1)
       
    hourly_forecast.dt = pd.to_datetime(hourly_forecast.dt, unit = 's')
    
    return(hourly_forecast)



def get_obs_date(lat, lon, dt):
    
    dt_POSIX = int(mktime(dt.timetuple()))    

    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

    params = {
        "lat": lat,  
        "lon": lon,
        "dt": dt_POSIX,
        "units": "metric",
        "appid": get_api_key()
        }
    
    response = requests.get(url, 
                        params = params)
    
    data = response.json()

    hourly_weather_info = pd.json_normalize(data['hourly'],
                             record_path = 'weather', 
                             record_prefix = 'weather_')

    hourly = pd.json_normalize(data['hourly'], 
                                       sep = '_')

    hourly = hourly.drop('weather', axis = 1)
    hourly = pd.concat([hourly, hourly_weather_info], axis = 1)

    hourly.dt = pd.to_datetime(hourly.dt, unit = 's')

    return(hourly)

def get_all_obs(lat, lon):
    datelist = [datetime.datetime.utcnow() - datetime.timedelta(days=i) for i in range(0, 6)]

    obs_list = [get_obs_date(lat, lon, dt) for dt in datelist]

    all_obs = pd.concat(obs_list)
    
    return(all_obs)

    