def calculate_pressure_drop(
    flow_rate: float, 
    layers: int, 
    coefficients: dict
) -> float:
    """
    Calculate pressure drop in kPa.

    Parameters:
        flow_rate (float): Flow rate in m³/s.
        layers (int): Number of layers.
        coefficients (dict): Dictionary containing the coefficients for pressure drop calculation.

    Returns:
        float: Pressure drop in kPa.
    """
    poly_coefficient = coefficients['poly_coefficient']
    line_coefficient = coefficients['line_coefficient']

    flow_per_layer = flow_rate / layers
    flow_SLPM = flow_per_layer / 1.29 * 60000  # Convert to SLPM

    pressure_drop = poly_coefficient * (flow_SLPM) ** 2 + line_coefficient * flow_SLPM
    
    return round(pressure_drop, 1)
