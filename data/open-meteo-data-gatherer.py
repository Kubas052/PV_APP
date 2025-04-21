import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
params = {
	"latitude": 52,
	"longitude": 21,
	"start_date": "2021-06-01",
	"end_date": "2025-01-01",
	"hourly": ["temperature_2m", "shortwave_radiation", "direct_normal_irradiance", "diffuse_radiation", "wind_speed_10m", "cloud_cover", "sunshine_duration", "precipitation", "relative_humidity_2m"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_shortwave_radiation = hourly.Variables(1).ValuesAsNumpy()
hourly_direct_normal_irradiance = hourly.Variables(2).ValuesAsNumpy()
hourly_diffuse_radiation = hourly.Variables(3).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(5).ValuesAsNumpy()
hourly_sunshine_duration = hourly.Variables(6).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(7).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(8).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s"),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance
hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["sunshine_duration"] = hourly_sunshine_duration
hourly_data["precipitation"] = hourly_precipitation
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)

hourly_dataframe.to_csv('hourly_data.csv', index=False)
