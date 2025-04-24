def estimate_pv_output(row, panel_area=10, efficiency=0.18):
    irradiance = row['shortwave_radiation']
    temp = row['temperature_2m']
    temp_correction = 1 - 0.004 * (temp - 25)
    return irradiance * panel_area * efficiency * temp_correction
