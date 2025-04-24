import os
import pandas as pd
import matplotlib.pyplot as plt
from src.prediction import predict_forecast

# Global variables for panel settings
PANEL_AREA = 10
EFFICIENCY = 0.18

def display_forecast_summary():
    if not os.path.exists('forecast_summary.csv'):
        print("⚠️ Forecast summary not found. Generating...")
        predict_forecast(7)
    forecast_data = pd.read_csv('forecast_summary.csv')
    forecast_data['adjusted_pv_output'] = forecast_data['predicted_pv_output'] * (PANEL_AREA / 1) * (EFFICIENCY / 0.2)

    # Plot forecast summary with two y-axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Time (Hours)')
    ax1.set_ylabel('Generated Watts', color='blue')
    ax1.plot(range(len(forecast_data)), forecast_data['adjusted_pv_output'], label='Generated Watts', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()  # Create a second y-axis
    ax2.set_ylabel('Price (zl/GWh)', color='red')
    ax2.plot(range(len(forecast_data)), forecast_data['predicted_fixing_price'], label='Price (zl/GWh)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title('Forecast Summary')
    fig.tight_layout()
    plt.show()

def make_decision():
    if not os.path.exists('forecast_summary.csv'):
        print("⚠️ Forecast summary not found. Generating...")
        predict_forecast(7)
    forecast_data = pd.read_csv('forecast_summary.csv')
    forecast_data['adjusted_pv_output'] = forecast_data['predicted_pv_output'] * (PANEL_AREA / 1) * (EFFICIENCY / 0.2)
    forecast_data['profit'] = forecast_data['adjusted_pv_output'] * forecast_data['predicted_fixing_price']

    # Decision logic: Scale profit to range [0.2, 1] based on thresholds
    max_profit = forecast_data['profit'].max()
    forecast_data['decision'] = (forecast_data['profit'] / max_profit).clip(upper=1).round(1)
    forecast_data['decision'] = (forecast_data['decision'] * 5).round() / 5  # Round to nearest 0.2
    print(forecast_data[['profit', 'decision']].head(24))  # Display first 24 hours

    # Plot decision over time
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Time (Hours)')
    ax1.set_ylabel('Decision (0.2 to 1)', color='green')
    ax1.plot(range(len(forecast_data)), forecast_data['decision'], label='Decision', color='green', drawstyle='steps-mid')
    ax1.tick_params(axis='y', labelcolor='green')

    ax2 = ax1.twinx()  # Integrate forecast summary into the decision plot
    ax2.set_ylabel('Generated Watts / Price (zl/GWh)', color='blue')
    ax2.plot(range(len(forecast_data)), forecast_data['adjusted_pv_output'], label='Generated Watts', color='blue')
    ax2.plot(range(len(forecast_data)), forecast_data['predicted_fixing_price'], label='Price (zl/GWh)', color='red')
    ax2.tick_params(axis='y', labelcolor='blue')

    plt.title('Decision to Sell and Forecast Summary')
    fig.tight_layout()
    plt.show()

def display_income_per_hour():
    if not os.path.exists('forecast_summary.csv'):
        print("⚠️ Forecast summary not found. Generating...")
        predict_forecast(7)
    forecast_data = pd.read_csv('forecast_summary.csv')
    forecast_data['adjusted_pv_output'] = forecast_data['predicted_pv_output'] * (PANEL_AREA / 1) * (EFFICIENCY / 0.2)

    # Adjust income per hour to W/zl/GWh
    forecast_data['income_per_hour'] = forecast_data['adjusted_pv_output'] / forecast_data['predicted_fixing_price']
    print(forecast_data[['date', 'income_per_hour']].head(24))

    # Plot income per hour
    plt.figure(figsize=(10, 6))
    plt.bar(forecast_data['date'], forecast_data['income_per_hour'], color='green')
    plt.xlabel('Date')
    plt.ylabel('Income per Hour (W/zl/GWh)')
    plt.title('Income Per Hour')
    plt.xticks(forecast_data['date'][::6], rotation=45)
    plt.tight_layout()
    plt.show()

def change_panel_settings():
    global PANEL_AREA, EFFICIENCY
    try:
        PANEL_AREA = float(input("Enter new panel area (m²): "))
        EFFICIENCY = float(input("Enter new efficiency (0-1): "))
        print(f"✅ Panel settings updated: Area = {PANEL_AREA} m², Efficiency = {EFFICIENCY}")
    except ValueError:
        print("❌ Invalid input. Please enter numeric values.")

def main_menu():
    while True:
        print("\n=== PV System Menu ===")
        print("1. Display Forecast Summary")
        print("2. Make Decision (Best Time to Sell)")
        print("3. Display Income Per Hour")
        print("4. Change Panel Settings")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            display_forecast_summary()
        elif choice == '2':
            make_decision()
        elif choice == '3':
            display_income_per_hour()
        elif choice == '4':
            change_panel_settings()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice. Please try again.")
