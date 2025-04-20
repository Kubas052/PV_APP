import pandas as pd
import holidays

# data initialization
hourly_data = pd.read_csv('../data/hourly_data.csv')
hourly_electricity_price = pd.read_csv('../data/hourly_electricity_price.csv')
hourly_production_by_type = pd.read_csv('../data/hourly_production_by_type.csv')
pl_holidays = holidays.Poland(years=[2021, 2022, 2023, 2024, 2025])

# Date handling
hourly_data['date'] = pd.to_datetime(hourly_data['date'])
hourly_electricity_price['date'] = pd.to_datetime(hourly_electricity_price['date'], format='%d.%m.%Y %H:%M')
hourly_production_by_type['date'] = pd.to_datetime(hourly_production_by_type['date'], format='%d.%m.%Y %H:%M')
merged_data = pd.merge(hourly_data, hourly_electricity_price, on='date')
merged_data = pd.merge(hourly_electricity_price, hourly_production_by_type, on='date')
merged_data['weekday'] = merged_data['date'].dt.weekday #just in case it would improve learning time
merged_data['weekend'] = merged_data['date'].dt.weekday.isin([5, 6]).astype(int)
merged_data['weekday_test'] = merged_data['date'].dt.day_name()
merged_data['is_holiday'] = merged_data['date'].dt.date.isin(pl_holidays.keys()).astype(int)

# if statements and drops
merged_data = merged_data[(merged_data['date'] >= '2021-06-01') & (merged_data['date'] < '2025-01-01')]
merged_data = merged_data.drop(columns=['date_utc', 'other', 'other_renewable'])
merged_data.to_csv('../data/merged_data.csv', index=False)
print(merged_data.columns)
