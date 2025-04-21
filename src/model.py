import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocessing import load_and_process_data
from forecast import get_forecast
import joblib
import matplotlib.pyplot as plt


merged_data = load_and_process_data()

features = ['year','month','day','hour','temperature_2m', 'cloud_cover',
'wind_speed_10m','relative_humidity_2m','weekday','is_holiday'] #do fixing ii price dodac is_holiday
target = 'fixing_ii_price'

X = merged_data[features]
y = merged_data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)

model.fit(X_train, y_train)

# Predykcje na zbiorze testowym
y_pred = model.predict(X_test)

# Ocena modelu
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"R²: {r2}")


forecast_data = get_forecast(days=14)

forecast_data['predicted_price'] = model.predict(forecast_data[features])


print(forecast_data[['date', 'predicted_price']])
# Przykład prognozy na 7 dni

# plt.figure(figsize=(10, 4))
# plt.plot(y_test.values[:100], label='True')
# plt.plot(y_pred[:100], label='Predicted')
# plt.legend()
# plt.title("Fixing II Price: True vs Predicted")
# plt.show()

joblib.dump(model, '../models/random_forest_model.pkl')
