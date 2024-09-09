import numpy as np
import copy
from ..utils.psychrometric_functions import (
    calculate_vaporization_enthalpy, calculate_temperature,
    calculate_relative_humidity
)


def solve(
        humidity_ratio_matrix, enthalpy_matrix, temperature_matrix,
        relative_humidity_matrix, specific_volume_matrix,
        channel_flow, mesh, temperatures, pressures,
        heat_res_tot, mas_res_tot, life_cycle_factor,
        max_iterations, convergence_threshold, relax_factor):
    """
    Performs the numerical solution for the FCH Performance Model.

    Parameters:
    - humidity_ratio_matrix: Initial humidity ratio matrix.
    - enthalpy_matrix: Initial enthalpy matrix.
    - temperature_matrix: Initial temperature matrix.
    - relative_humidity_matrix: Initial relative humidity matrix.
    - specific_volume_matrix: Specific volume matrix.
    - channel_flow: Flow characteristics for the channel.
    - mesh: Mesh configuration.
    - temperatures: Dictionary of temperature conditions.
    - pressures: Dictionary of pressure conditions.
    - heat_res_tot: Total heat resistance.
    - mas_res_tot: Total mass resistance.
    - life_cycle_factor: Factor considering the life cycle stage.
    - max_iterations: Maximum allowed iterations.
    - convergence_threshold: Convergence threshold.
    - relax_factor: Relaxation factor.

    Returns:
    - Updated matrices and the final convergence error.
    """

    iteration = 0
    convergence_error = float('inf')

    while convergence_error > convergence_threshold and iteration < max_iterations:
        iteration += 1

        # Calculate heat and mass transfer
        heat_transfer, mass_transfer = update_heat_mass_transfer(
            temperature_matrix, humidity_ratio_matrix, specific_volume_matrix,
            heat_res_tot, mas_res_tot, life_cycle_factor
        )

        # Copy matrices for updating
        humidity_ratio_update = copy.deepcopy(humidity_ratio_matrix)
        enthalpy_update = copy.deepcopy(enthalpy_matrix)

        # Dry side updates
        humidity_ratio_update, enthalpy_update = update_dry_side(
            humidity_ratio_update, humidity_ratio_matrix, enthalpy_update, enthalpy_matrix,
            mass_transfer, temperature_matrix, heat_transfer, channel_flow, mesh
        )

        # Wet side updates
        humidity_ratio_update, enthalpy_update = update_wet_side(
            humidity_ratio_update, humidity_ratio_matrix, enthalpy_update, enthalpy_matrix,
            mass_transfer, temperature_matrix, heat_transfer, channel_flow
        )

        # Calculate absolute changes and convergence error
        absolute_changes = calculate_absolute_changes(
            humidity_ratio_update, enthalpy_update, humidity_ratio_matrix, enthalpy_matrix
        )
        convergence_error = np.max(list(absolute_changes.values()))

        # Update domain property matrices
        (
            humidity_ratio_matrix, enthalpy_matrix, temperature_matrix,
            relative_humidity_matrix
        ) = update_condition_matrices(
            humidity_ratio_matrix, enthalpy_matrix, temperature_matrix,
            relative_humidity_matrix, humidity_ratio_update, enthalpy_update,
            relax_factor, pressures
        )
        if iteration%1000==0:
            print(f"Convergance error is {convergence_error} at iteration {iteration}")

        # Check for divergence
        if convergence_error > 10**6:
            raise ValueError(
                "Model diverged, check input parameter range or model parameters")
        
    if convergence_error > convergence_threshold:
        raise ValueError(
            "Model diverged, check input parameter range or model parameters")
    
    print("\nModel Successfully Converged!!!")
    print("-----------------------------------------")
    return (
        humidity_ratio_matrix, enthalpy_matrix, temperature_matrix,
        relative_humidity_matrix
    )


def update_heat_mass_transfer(
        temperature_matrix, humidity_ratio_matrix, specific_volume_matrix,
        heat_res_tot, mas_res_tot, life_cycle_factor):
    heat_transfer = (
        temperature_matrix['wet'] - temperature_matrix['dry']
    ) / heat_res_tot * life_cycle_factor
    mass_transfer = (
        humidity_ratio_matrix['wet'] / specific_volume_matrix['wet'] -
        humidity_ratio_matrix['dry'] / specific_volume_matrix['dry']
    ) / mas_res_tot * life_cycle_factor
    return heat_transfer, mass_transfer


def update_dry_side(
        humidity_ratio_update, humidity_ratio_matrix, enthalpy_update,
        enthalpy_matrix, mass_transfer, temperature_matrix, heat_transfer,
        channel_flow, mesh):
    # Update humidity ratio for the dry side
    humidity_ratio_update['dry'][:, 1:] = (
        2 * mass_transfer[:, :-1] /
        (channel_flow['dry'] / (mesh['model'] / mesh['dry']))
    ) + humidity_ratio_matrix['dry'][:, :-1]

    # Calculate vapor enthalpy for the dry side
    vapor_enthalpy_dry = calculate_vaporization_enthalpy(
        (temperature_matrix['wet'][:, :-1] +
         temperature_matrix['dry'][:, :-1]) / 2
    )

    # Update enthalpy for the dry side
    enthalpy_update['dry'][:, 1:] = (
        2 * (mass_transfer[:, :-1] * vapor_enthalpy_dry + heat_transfer[:, :-1]) /
        (channel_flow['dry'] / (mesh['model'] / mesh['dry']))
    ) + enthalpy_matrix['dry'][:, :-1]

    return humidity_ratio_update, enthalpy_update


def update_wet_side(
        humidity_ratio_update, humidity_ratio_matrix, enthalpy_update,
        enthalpy_matrix, mass_transfer, temperature_matrix, heat_transfer,
        channel_flow):
    # Update humidity ratio for the wet side
    humidity_ratio_update['wet'][1:, :] = (
        -2 * mass_transfer[:-1, :] / channel_flow['wet']
    ) + humidity_ratio_matrix['wet'][:-1, :]

    # Calculate vapor enthalpy for the wet side
    vapor_enthalpy_wet = calculate_vaporization_enthalpy(
        (temperature_matrix['wet'][:-1, :] +
         temperature_matrix['dry'][:-1, :]) / 2
    )

    # Update enthalpy for the wet side
    enthalpy_update['wet'][1:, :] = (
        -2 * (mass_transfer[:-1, :] * vapor_enthalpy_wet + heat_transfer[:-1, :]) /
        channel_flow['wet']
    ) + enthalpy_matrix['wet'][:-1, :]

    return humidity_ratio_update, enthalpy_update


def calculate_absolute_changes(
        humidity_ratio_update, enthalpy_update,
        humidity_ratio_matrix, enthalpy_matrix):
    return {
        'dry_Humidity': abs(humidity_ratio_update['dry'] - humidity_ratio_matrix['dry']),
        'wet_Humidity': abs(humidity_ratio_update['wet'] - humidity_ratio_matrix['wet']),
        'dry_Enthalpy': abs(enthalpy_update['dry'] - enthalpy_matrix['dry']),
        'wet_Enthalpy': abs(enthalpy_update['wet'] - enthalpy_matrix['wet']),
    }


def update_condition_matrices(
        humidity_ratio_matrix, enthalpy_matrix, temperature_matrix,
        relative_humidity_matrix, humidity_ratio_update, enthalpy_update,
        relax_factor, pressures):
    for condition in ['dry', 'wet']:
        # Update humidity ratio
        humidity_ratio_matrix[condition] += relax_factor * (
            humidity_ratio_update[condition] - humidity_ratio_matrix[condition]
        )

        # Update enthalpy
        enthalpy_matrix[condition] += relax_factor * (
            enthalpy_update[condition] - enthalpy_matrix[condition]
        )

        # Recalculate temperature
        temperature_matrix[condition] = calculate_temperature(
            enthalpy_matrix[condition], humidity_ratio_matrix[condition]
        )

        # Recalculate relative humidity
        relative_humidity_matrix[condition] = calculate_relative_humidity(
            temperature_matrix[condition], w=humidity_ratio_matrix[condition],
            P=pressures[condition]
        )

    return (
        humidity_ratio_matrix, enthalpy_matrix, temperature_matrix,
        relative_humidity_matrix
    )
