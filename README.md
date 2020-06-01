# owapi

owapi is a package to help you acquire weather data from the
[OpenWeather API](https://openweathermap.org/api).
It employs the [One Call API](https://openweathermap.org/api/one-call-api) and
can return, for any location:

* Current weather observations
* Weather forecast
  * Hourly (next 48 hours)
  * Daily (next 7 days)
* Historical observations for the previous five days.

All data is returned as Pandas DataFrames.

The API is limited to 1000 calls a day in the free tier. You can pay for more
requests if required.

## Getting Started

### Register for an API Key

You will need to get an API key by signing up to
[OpenWeather](https://openweathermap.org/guide).

### Set API Key for owapi

    owapi.set_api_key("my-api-key")

### Get Current Observations

    current = owapi.get_current_obs(53.381495, -1.471421)

### Get Hourly forecast

    hourly = owapi.get_hourly_forecast(53.381495, -1.471421)

### Get Daily forecast

    daily = owapi.get_daily_forecast(53.381495, -1.471421)

### Get All Available Historic Observations

    historic = owapi.get_all_obs(60.33, -1.33)
