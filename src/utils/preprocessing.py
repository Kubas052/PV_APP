import pandas as pd
import holidays
import os
from src.utils.pv_utils import estimate_pv_output

def load_and_process_data():
    # data initialization
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
    hourly_data = pd.read_csv(os.path.join(data_dir, 'hourly_data.csv'))
    hourly_electricity_price = pd.read_csv(os.path.join(data_dir, 'hourly_electricity_price.csv'))
    hourly_production_by_type = pd.read_csv(os.path.join(data_dir, 'hourly_production_by_type.csv'))
    pl_holidays = holidays.Poland(years=[2021, 2022, 2023, 2024, 2025])

    # Date handling
    hourly_data['date'] = pd.to_datetime(hourly_data['date'])
    hourly_data['year'] = hourly_data['date'].dt.year
    hourly_data['month'] = hourly_data['date'].dt.month
    hourly_data['day'] = hourly_data['date'].dt.day
    hourly_data['hour'] = hourly_data['date'].dt.hour  # godzina
    hourly_electricity_price['date'] = pd.to_datetime(hourly_electricity_price['date'], format='%d.%m.%Y %H:%M')
    hourly_production_by_type['date'] = pd.to_datetime(hourly_production_by_type['date'], format='%d.%m.%Y %H:%M')
    merged_data = pd.merge(hourly_data, hourly_electricity_price, on='date')
    merged_data = pd.merge(merged_data, hourly_production_by_type, on='date')
    merged_data['weekday'] = merged_data['date'].dt.weekday #just in case it would improve learning time
    merged_data['weekend'] = merged_data['date'].dt.weekday.isin([5, 6]).astype(int)
    merged_data['weekday_test'] = merged_data['date'].dt.day_name()
    merged_data['is_holiday'] = merged_data['date'].dt.date.isin(pl_holidays.keys()).astype(int)

    # if statements and drops
    merged_data = merged_data[(merged_data['date'] >= '2021-06-01') & (merged_data['date'] < '2025-01-01')]
    merged_data = merged_data.drop(columns=['date_utc', 'other', 'other_renewable'])
    #print(merged_data.info())

    merged_data = merged_data.dropna()
    merged_data['pv_output_estimate'] = merged_data.apply(estimate_pv_output, axis=1)
    return merged_data
load_and_process_data()
#output
#merged_data.to_csv('../data/merged_data.csv', index=False)
#print(merged_data.columns)


#controll
#print(merged_data.info())

#print(merged_data.describe())
#print(merged_data.isnull().sum())
#print(merged_data['weekday'].value_counts())
