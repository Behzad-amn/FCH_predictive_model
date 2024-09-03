import numpy as np
from ..utils.psychrometric_functions import (
    calculate_humidity_ratio, calculate_enthalpy,
    calculate_specific_volume
)

# Constants
DRY = 'dry'
WET = 'wet'

def initialize_domain_properties(
    mesh: dict, 
    temperatures: dict, 
    relative_humidities: dict, 
    pressures: dict
) -> tuple:
    """
    Initialize the domain properties such as humidity ratio, temperature,
    relative humidity, enthalpy, and specific volume.

    Parameters:
        mesh (dict): The mesh configuration for the model.
        temperatures (dict): Dictionary containing temperature values for 'dry' and 'wet' conditions.
        relative_humidities (dict): Dictionary containing relative humidity values for 'dry' and 'wet' conditions.
        pressures (dict): Dictionary containing pressure values for 'dry' and 'wet' conditions.

    Returns:
        tuple: Containing matrices for humidity ratio, temperature, relative humidity, 
               enthalpy, and specific volume for 'dry' and 'wet' conditions.
    """
    
    inlet_humidity = {}
    humidity_ratio_matrix = {}
    temperature_matrix = {}
    relative_humidity_matrix = {}
    enthalpy_matrix = {}
    specific_volume_matrix = {}

    for condition in [DRY, WET]:
        inlet_humidity_temp = calculate_humidity_ratio(
            temperatures[condition], relative_humidities[condition], pressures[condition]
        )
        inlet_humidity[condition] = inlet_humidity_temp

        humidity_ratio_matrix[condition] = np.ones(
            (mesh['model'], mesh['model'])
        ) * inlet_humidity[condition]

        temperature_matrix[condition] = np.ones(
            (mesh['model'], mesh['model'])
        ) * temperatures[condition]

        relative_humidity_matrix[condition] = np.ones(
            (mesh['model'], mesh['model'])
        ) * relative_humidities[condition]

        enthalpy_matrix[condition] = calculate_enthalpy(
            temperature_matrix[condition], humidity_ratio_matrix[condition]
        )

        specific_volume_matrix[condition] = calculate_specific_volume(
            temperatures[condition], inlet_humidity[condition], pressures[condition]
        )

    return (
        humidity_ratio_matrix, temperature_matrix,
        relative_humidity_matrix, enthalpy_matrix, specific_volume_matrix
    )
