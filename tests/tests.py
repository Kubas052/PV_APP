import pandas as pd
import holidays
import pytest

@pytest.fixture
def merged_data_fixture():
    hourly_data = pd.read_csv('../data/hourly_data.csv')
    hourly_electricity_price = pd.read_csv('../data/hourly_electricity_price.csv')
    hourly_production_by_type = pd.read_csv('../data/hourly_production_by_type.csv')
    pl_holidays = holidays.Poland(years=[2021, 2022, 2023, 2024, 2025])

    hourly_data['date'] = pd.to_datetime(hourly_data['date'])
    hourly_electricity_price['date'] = pd.to_datetime(hourly_electricity_price['date'], format='%d.%m.%Y %H:%M')
    hourly_production_by_type['date'] = pd.to_datetime(hourly_production_by_type['date'], format='%d.%m.%Y %H:%M')

    merged = pd.merge(hourly_data, hourly_electricity_price, on='date')
    merged = pd.merge(merged, hourly_production_by_type, on='date')

    merged['weekday'] = merged['date'].dt.weekday
    merged['weekend'] = merged['date'].dt.weekday.isin([5, 6]).astype(int)
    merged['weekday_test'] = merged['date'].dt.day_name()
    merged['is_holiday'] = merged['date'].dt.date.isin(pl_holidays.keys()).astype(int)

    merged = merged[(merged['date'] >= '2021-06-01') & (merged['date'] < '2025-01-01')]
    merged = merged.drop(columns=['date_utc', 'other', 'other_renewable'], errors='ignore')  # just in case

    return merged


def test_date_range(merged_data_fixture):
    assert merged_data_fixture['date'].min() >= pd.Timestamp('2021-06-01')
    assert merged_data_fixture['date'].max() < pd.Timestamp('2025-01-01')


def test_columns_exist(merged_data_fixture):
    expected_columns = {'weekday', 'weekend', 'is_holiday', 'date'}
    assert expected_columns.issubset(set(merged_data_fixture.columns))


def test_weekend_values(merged_data_fixture):
    # Check that weekend values are 0 or 1
    assert set(merged_data_fixture['weekend'].unique()).issubset({0, 1})


def test_is_holiday_values(merged_data_fixture):
    # Should be only 0 or 1
    assert set(merged_data_fixture['is_holiday'].unique()).issubset({0, 1})


def test_dropped_columns(merged_data_fixture):
    dropped = {'date_utc', 'other', 'other_renewable'}
    assert dropped.isdisjoint(set(merged_data_fixture.columns))
