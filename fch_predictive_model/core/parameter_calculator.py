import math
from ..utils.psychrometric_functions import (
    calculate_viscosity,
    calculate_Reynolds,
    calculate_Nusselt
)

# Constants
DRY = 'dry'
WET = 'wet'

def calculate_channel_parameter(
    channel_properties: dict, 
    mass_flow_rates: dict, 
    layer_count: int, 
    mesh: dict
) -> tuple:
    """
    Calculate hydraulic diameter, area, and flow rate for each channel.

    Parameters:
        channel_properties (dict): Dictionary containing the channel properties.
        mass_flow_rates (dict): Mass flow rates for 'dry' and 'wet' conditions.
        layer_count (int): Number of layers in the model.
        mesh (dict): Mesh discretization for 'dry' and 'wet' conditions.

    Returns:
        tuple: Containing dictionaries for hydraulic diameter, area, and flow rates.
    """
    hyd_dia = {}
    area = {}
    channel_flow = {}

    for side in [DRY, WET]:
        channel = channel_properties[side]
        channel_area = channel['pitch'] * channel['width']
        channel_hyd_dia = 2 * channel['pitch'] * channel['width'] / (
            channel['pitch'] + channel['width']
        )

        hyd_dia[side] = channel_hyd_dia
        area[side] = channel_area

        flow = mass_flow_rates[side] / layer_count / mesh[side]
        channel_flow[side] = flow

    return hyd_dia, area, channel_flow


def calculate_model_parameter(channel_properties: dict) -> tuple:
    """
    Calculate the model discretization parameter.

    Parameters:
        channel_properties (dict): Dictionary containing channel properties.

    Returns:
        tuple: Containing the discretization parameters for the model and the transfer area.
    """
    dry_channel = channel_properties[DRY]
    wet_channel = channel_properties[WET]

    # Calculate the number of dry channels per layer
    dry_channel_count = math.floor(
        dry_channel['length'] / dry_channel['width']
    )

    # Calculate the effective length of the wet channel
    effective_wet_length = (
        wet_channel['length']
        - 2 * wet_channel['edge_thickness']
        + wet_channel['wall_thickness']
    )

    # Calculate the number of wet channels per layer
    wet_channel_count = math.floor(
        effective_wet_length
        / (wet_channel['width'] + wet_channel['wall_thickness'])
    )

    # Calculate the discretization parameter
    discretization_param = round(
        wet_channel_count / dry_channel_count
    ) * dry_channel_count

    transfer_area = wet_channel['width'] ** 2

    return {
        DRY: dry_channel_count,
        WET: wet_channel_count,
        'model': discretization_param
    }, transfer_area


def calculate_solver_parameters(
    temperatures: dict, 
    hyd_dia: dict, 
    area: dict, 
    channel_flow: dict, 
    channel_properties: dict,
    air_properties: dict, 
    membrane_properties: dict, 
    transfer_area: float,
    specific_volume_matrix: dict
) -> tuple:
    """
    Calculate the solver parameters such as heat and mass resistance.

    Parameters:
        temperatures (dict): Temperatures for 'dry' and 'wet' conditions.
        hyd_dia (dict): Hydraulic diameters for 'dry' and 'wet' conditions.
        area (dict): Areas for 'dry' and 'wet' conditions.
        channel_flow (dict): Flow rates for 'dry' and 'wet' conditions.
        channel_properties (dict): Dictionary containing channel properties.
        air_properties (dict): Dictionary containing air properties.
        membrane_properties (dict): Dictionary containing membrane properties.
        transfer_area (float): Transfer area for the model.
        specific_volume_matrix (dict): Specific volume matrix for 'dry' and 'wet' conditions.

    Returns:
        tuple: Containing total heat resistance and total mass resistance.
    """
    reynolds = {}
    nusselt = {}
    heat_conv_coeff = {}
    mass_conv_coeff = {}
    air_conductivity = air_properties['thermal_conductivity']
    air_heat_capacity = air_properties['heat_capacity']
    lewis_number = air_properties['Lewis_number']
    membrane_thickness = membrane_properties['thickness']
    membrane_conductivity = membrane_properties['thermal_conductivity']
    membrane_mass_resistance = membrane_properties['mass_transfer_resistance']

    for condition in [DRY, WET]:
        viscosity_temp = calculate_viscosity(temperatures[condition])
        reynolds[condition] = calculate_Reynolds(
            channel_flow[condition], hyd_dia[condition], area[condition], viscosity_temp
        )

        channel_spec = channel_properties[condition]
        nusselt[condition] = calculate_Nusselt(
            channel_spec['pitch'], channel_spec['width'],
            channel_spec['length'], hyd_dia[condition], reynolds[condition]
        )

        heat_conv_coeff[condition] = nusselt[condition] * \
            air_conductivity / hyd_dia[condition]

        mass_conv_coeff[condition] = (
            heat_conv_coeff[condition] * specific_volume_matrix[condition]
            / air_heat_capacity * lewis_number ** (-2 / 3)
        )

    flow_heat_resistance = 1 / \
        heat_conv_coeff[DRY] + 1 / heat_conv_coeff[WET]
    membrane_heat_resistance = membrane_thickness / membrane_conductivity
    heat_res_tot = (
        (flow_heat_resistance + membrane_heat_resistance)
        / transfer_area
    )

    flow_mass_resistance = 1 / \
        mass_conv_coeff[DRY] + 1 / mass_conv_coeff[WET]
    mas_res_tot = (
        (flow_mass_resistance + membrane_mass_resistance)
        / transfer_area
    )

    return heat_res_tot, mas_res_tot
