import numpy as np
from ..utils.psychrometric_functions import (calculate_temperature,
                                             calculate_relative_humidity, calculate_dew_point
                                             )


def result_compiler(pressures, pressure_drop, enthalpy_matrix, humidity_ratio_matrix, flow_rate):
    # Pressure results
    pressure_results = {
        'dry': {
            'inlet': round(pressures['dry'], 1),
            'outlet': round(pressures['dry'] - pressure_drop['dry'], 1)
        },
        'wet': {
            'inlet': round(pressures['wet'], 1),
            'outlet': round(pressures['wet'] - pressure_drop['wet'], 1)
        }
    }

    # Enthalpy results
    enthalpy_results = {
        'dry': {
            'inlet': round(np.mean(enthalpy_matrix['dry'][:, 0]), 0),
            'outlet': round(np.mean(enthalpy_matrix['dry'][:, -1]), 0)
        },
        'wet': {
            'inlet': round(np.mean(enthalpy_matrix['wet'][0, :]), 1),
            'outlet': round(np.mean(enthalpy_matrix['wet'][-1, :]), 1)
        }
    }

    # Humidity ratio results
    humidity_ratio_results = {
        'dry': {
            'inlet': round(np.mean(humidity_ratio_matrix['dry'][:, 0]), 3),
            'outlet': round(np.mean(humidity_ratio_matrix['dry'][:, -1]), 3)
        },
        'wet': {
            'inlet': round(np.mean(humidity_ratio_matrix['wet'][0, :]), 3),
            'outlet': round(np.mean(humidity_ratio_matrix['wet'][-1, :]), 3)
        }
    }

    # Temperature results
    temperature_results = {
        'dry': {
            'inlet': round(calculate_temperature(
                enthalpy_results['dry']['inlet'], humidity_ratio_results['dry']['inlet']), 1
            ),
            'outlet': round(calculate_temperature(
                enthalpy_results['dry']['outlet'], humidity_ratio_results['dry']['outlet']), 1
            )
        },
        'wet': {
            'inlet': round(calculate_temperature(
                enthalpy_results['wet']['inlet'], humidity_ratio_results['wet']['inlet']), 1
            ),
            'outlet': round(calculate_temperature(
                enthalpy_results['wet']['outlet'], humidity_ratio_results['wet']['outlet']), 1
            )
        }
    }

    # Relative humidity results
    relative_humidity_results = {
        'dry': {
            'inlet': round(calculate_relative_humidity(
                temperature_results['dry']['inlet'], w=humidity_ratio_results['dry']['inlet'],
                P=pressure_results['dry']['inlet']), 1
            ),
            'outlet': round(calculate_relative_humidity(
                temperature_results['dry']['outlet'], w=humidity_ratio_results['dry']['outlet'],
                P=pressure_results['dry']['outlet']), 1
            )
        },
        'wet': {
            'inlet': round(calculate_relative_humidity(
                temperature_results['wet']['inlet'], w=humidity_ratio_results['wet']['inlet'],
                P=pressure_results['wet']['inlet']), 1
            ),
            'outlet': round(calculate_relative_humidity(
                temperature_results['wet']['outlet'], w=humidity_ratio_results['wet']['outlet'],
                P=pressure_results['wet']['outlet']), 1
            )
        }
    }

    # Dew point results
    dew_point_results = {
        'dry': {
            'inlet': round(calculate_dew_point(
                temperature_results['dry']['inlet'], relative_humidity_results['dry']['inlet']), 1
            ),
            'outlet': round(calculate_dew_point(
                temperature_results['dry']['outlet'], relative_humidity_results['dry']['outlet']), 1
            )
        },
        'wet': {
            'inlet': round(calculate_dew_point(
                temperature_results['wet']['inlet'], relative_humidity_results['wet']['inlet']), 1
            ),
            'outlet': round(calculate_dew_point(
                temperature_results['wet']['outlet'], relative_humidity_results['wet']['outlet']), 1
            )
        }
    }

    dewpoint_temperature_approach = round(dew_point_results['wet']['inlet'] -
                                          dew_point_results['dry']['outlet'], 1)

    vapor_transport = round(flow_rate['dry']*(humidity_ratio_results['dry']
                                              ['outlet']-humidity_ratio_results['dry']['inlet']), 1)

    water_recovery_ratio = round(
        (vapor_transport) /
        (flow_rate['wet']*(humidity_ratio_results['wet']['inlet']))*100, 1)

    max_differential = round(max(
        max(pressure_results['dry'].values()), max(
            pressure_results['wet'].values())
    ) - min(
        min(pressure_results['dry'].values()), min(
            pressure_results['wet'].values())
    ), 1)

    return {
        'flow_rate': flow_rate,
        'pressure': pressure_results,
        'enthalpy': enthalpy_results,
        'humidity_ratio': humidity_ratio_results,
        'temperature': temperature_results,
        'relative_humidity': relative_humidity_results,
        'dew_point': dew_point_results,
        'pressure_drop': pressure_drop,
        'DPAT': dewpoint_temperature_approach,
        'vapor_transport': vapor_transport,
        'water_recovery_ratio': water_recovery_ratio,
        'max__pressure_differential': max_differential
    }
