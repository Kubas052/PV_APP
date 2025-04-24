import os
import joblib
from weather_forecast import get_forecast

def predict_forecast(days=7):
    forecast_data = get_forecast(days=7)
    try:

        pv_model = joblib.load('../models/pv_output_model.pkl')
        fixing_model = joblib.load('../models/fixing_ii_price_model.pkl')
        print("✅ Modele zostały załadowane z pliku.")
    except Exception as e:
        print("⚠️ Nie udało się załadować modeli. Trenuję od nowa...")
        os.system('../training/model_pv_output.py')
        os.system('../training/model_pv_output.py')
        pv_model = joblib.load('../models/pv_output_model.pkl')
        fixing_model = joblib.load('../models/fixing_ii_price_model.pkl')
        print("✅ Modele zostały przetrenowane i załadowane.")

    forecast_data = get_forecast(days=7)

    forecast_data['day'] = forecast_data['date'].dt.day  # wymagane przez model fixing
    forecast_data['weekday'] = forecast_data['date'].dt.weekday

    X_pv = forecast_data[list(pv_model.feature_names_in_)]
    X_fixing = forecast_data[list(fixing_model.feature_names_in_)]

    forecast_data['predicted_pv_output'] = pv_model.predict(X_pv)
    forecast_data['predicted_fixing_price'] = fixing_model.predict(X_fixing)

    print("\n📊 Prognoza (pierwsze 24h):")
    print(forecast_data[['date', 'predicted_pv_output', 'predicted_fixing_price']].head(24))

    forecast_data[['date', 'predicted_pv_output', 'predicted_fixing_price']].to_csv('forecast_summary.csv', index=False)
    print("\n✅ Wyniki zapisane do 'forecast_summary.csv'")