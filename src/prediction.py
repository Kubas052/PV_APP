import os
import joblib
from weather_forecast import get_forecast

PANEL_AREA = 1  # Define the panel area
EFFICIENCY = 0.2  # Define the efficiency

def predict_forecast(days=7):
    forecast_data = get_forecast(days=7)
    try:
        pv_model = joblib.load('../models/pv_output_model.pkl')
        fixing_model = joblib.load('../models/fixing_ii_price_model.pkl')
        print("✅ Models loaded successfully.")
    except FileNotFoundError as e:
        print(f"⚠️ Models not found: {e}. Training new models...")
        os.system('python ../training/model_pv_output.py')
        os.system('python ../training/model_fixing.py')
        pv_model = joblib.load('../models/pv_output_model.pkl')
        fixing_model = joblib.load('../models/fixing_ii_price_model.pkl')
        print("✅ Models trained and loaded.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return

    forecast_data['day'] = forecast_data['date'].dt.day  # Required by fixing model
    forecast_data['weekday'] = forecast_data['date'].dt.weekday

    X_pv = forecast_data[list(pv_model.feature_names_in_)]
    X_fixing = forecast_data[list(fixing_model.feature_names_in_)]

    forecast_data['predicted_pv_output'] = pv_model.predict(X_pv)
    forecast_data['predicted_fixing_price'] = fixing_model.predict(X_fixing)

    # Adjust predicted PV output based on panel area and efficiency
    forecast_data['predicted_pv_output'] *= (PANEL_AREA / 1) * (EFFICIENCY / 0.2)

    # Adjust price to zl/GWh (if needed)
    forecast_data['predicted_fixing_price'] *= 1000  # Assuming original price is in zl/MWh

    print("\n📊 Forecast (first 24h):")
    print(forecast_data[['date', 'predicted_pv_output', 'predicted_fixing_price']].head(24))

    forecast_data[['date', 'predicted_pv_output', 'predicted_fixing_price']].to_csv('forecast_summary.csv', index=False)
    print("\n✅ Results saved to 'forecast_summary.csv'")
