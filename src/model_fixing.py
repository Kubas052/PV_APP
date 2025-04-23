import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from preprocessing import *
#loads data from preprocessing
merged_data = load_and_process_data()
#selects features and target
features = ['year', 'month', 'hour', 'temperature_2m', 'wind_speed_10m', 'day', 'weekday']
target = 'fixing_ii_price'

X = merged_data[features]
y = merged_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
#makes the predictions and error rate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae}")
print(f"MSE: {mse}")
print(f"R²: {r2}")
#importances (how valuable is a feature)

importances = model.feature_importances_
feature_importance = pd.Series(importances, index=features)
feature_importance = feature_importance.sort_values(ascending=False)

print("Feature Importances:")
print(feature_importance)

joblib.dump(model, '../models/fixing_ii_price_model.pkl')
