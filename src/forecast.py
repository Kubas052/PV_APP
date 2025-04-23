import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import holidays
from preprocessing import estimate_pv_output

def get_forecast(days):
	pl_holidays = holidays.Poland(years=[2021, 2022, 2023, 2024, 2025])

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": 52,
		"longitude": 21,
		"hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "cloud_cover", "shortwave_radiation", "diffuse_radiation", "precipitation_probability", "precipitation", "direct_normal_irradiance"],
		"forecast_days": days
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
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
	hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
	hourly_shortwave_radiation = hourly.Variables(4).ValuesAsNumpy()
	hourly_diffuse_radiation = hourly.Variables(5).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(6).ValuesAsNumpy()
	hourly_precipitation = hourly.Variables(7).ValuesAsNumpy()
	hourly_direct_normal_irradiance = hourly.Variables(8).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s"),
		end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["cloud_cover"] = hourly_cloud_cover
	hourly_data["shortwave_radiation"] = hourly_shortwave_radiation
	hourly_data["diffuse_radiation"] = hourly_diffuse_radiation
	hourly_data["precipitation_probability"] = hourly_precipitation_probability
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["direct_normal_irradiance"] = hourly_direct_normal_irradiance


	forecast_dataframe = pd.DataFrame(data = hourly_data)

	forecast_dataframe['date'] = pd.to_datetime(forecast_dataframe['date']) #must have
	forecast_dataframe['year'] = forecast_dataframe['date'].dt.year
	forecast_dataframe['month'] = forecast_dataframe['date'].dt.month
	forecast_dataframe['day'] = forecast_dataframe['date'].dt.day
	forecast_dataframe['hour'] = forecast_dataframe['date'].dt.hour
	forecast_dataframe['weekday'] = forecast_dataframe['date'].dt.weekday  # just in case it would improve learning time
	forecast_dataframe['weekend'] = forecast_dataframe['date'].dt.weekday.isin([5, 6]).astype(int)
	forecast_dataframe['weekday_test'] = forecast_dataframe['date'].dt.day_name()
	forecast_dataframe['is_holiday'] = forecast_dataframe['date'].dt.date.isin(pl_holidays.keys()).astype(int)
	forecast_dataframe['pv_output_estimate'] = forecast_dataframe.apply(estimate_pv_output, axis=1)
	return forecast_dataframe

forecast_data = get_forecast(days=14)
