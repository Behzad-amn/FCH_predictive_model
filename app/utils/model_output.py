import pandas as pd

def write_to_excel(results: dict, filename: str) -> None:
    """
    Writes the compiled results to an Excel file.

    Parameters:
    - results (dict): Dictionary containing the compiled results from the model.
    - filename (str): Name of the Excel file to write the results to.
    """
    # Prepare the data for the DataFrame
    data = {
        'Mass Flow Dry Inlet (kg/s)': [results['flow_rate']['dry']],
        'Temperature Dry Inlet (°C)': [results['temperature']['dry']['inlet']],
        'Pressure Dry Inlet (kPa)': [results['pressure']['dry']['inlet']],
        'Relative Humidity Dry Inlet (%)': [results['relative_humidity']['dry']['inlet']],
        'Absolute Humidity Dry Inlet (kg/kg_dry)': [results['humidity_ratio']['dry']['inlet']],
        'Dew Point Dry Inlet (°C)': [results['dew_point']['dry']['inlet']],

        'Temperature Dry Outlet (°C)': [results['temperature']['dry']['outlet']],
        'Pressure Dry Outlet (kPa)': [results['pressure']['dry']['outlet']],
        'Relative Humidity Dry Outlet (%)': [results['relative_humidity']['dry']['outlet']],
        'Absolute Humidity Dry Outlet (kg/kg_dry)': [results['humidity_ratio']['dry']['outlet']],
        'Dew Point Dry Outlet (°C)': [results['dew_point']['dry']['outlet']],

        'Mass Flow Wet Inlet (kg/s)': [results['flow_rate']['wet']],
        'Temperature Wet Inlet (°C)': [results['temperature']['wet']['inlet']],
        'Pressure Wet Inlet (kPa)': [results['pressure']['wet']['inlet']],
        'Relative Humidity Wet Inlet (%)': [results['relative_humidity']['wet']['inlet']],
        'Absolute Humidity Wet Inlet (kg/kg_dry)': [results['humidity_ratio']['wet']['inlet']],
        'Dew Point Wet Inlet (°C)': [results['dew_point']['wet']['inlet']],

        'Temperature Wet Outlet (°C)': [results['temperature']['wet']['outlet']],
        'Pressure Wet Outlet (kPa)': [results['pressure']['wet']['outlet']],
        'Relative Humidity Wet Outlet (%)': [results['relative_humidity']['wet']['outlet']],
        'Absolute Humidity Wet Outlet (kg/kg_dry)': [results['humidity_ratio']['wet']['outlet']],
        'Dew Point Wet Outlet (°C)': [results['dew_point']['wet']['outlet']],

        'Pressure Drop Dry (kPa)': [results['pressure_drop']['dry']],
        'Pressure Drop Wet (kPa)': [results['pressure_drop']['wet']],
        'DPAT (°C)': [results['DPAT']],
        'Vapor Transport (kg/s)': [results['vapor_transport']],
        'Water Recovery Ratio (%)': [results['water_recovery_ratio']],
        'Max Pressure Differential (kPa)': [results['max__pressure_differential']],
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Write the DataFrame to an Excel file
    try:
        df.to_excel(filename, index=False)
        print(f"Results have been successfully written to {filename}")
    except Exception as e:
        print(f"Failed to write results to {filename}: {e}")
