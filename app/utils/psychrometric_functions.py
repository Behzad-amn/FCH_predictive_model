import math
import numpy as np

def calculate_enthalpy(T: float, w: float) -> float:
    """
    Calculate enthalpy in J/kg_d.

    Parameters:
    T  : Temperature in degrees Celsius
    w  : Humidity ratio in kg/kg_d

    Returns:
    e  : Enthalpy in J/kg_d
    """
    C0 = 1.006
    C1 = 2501
    C2 = 1.86
    return (C0 * T + w * (C1 + C2 * T)) * 1000  # Conversion to J/kg_d


def calculate_specific_volume(T: float, w: float, P: float) -> float:
    """
    Calculate specific volume in m3/kg_d.

    Parameters:
    T  : Temperature in degrees Celsius
    w  : Humidity ratio in kg/kg_d
    P  : Pressure in kPa

    Returns:
    v  : Specific volume in m3/kg_d
    """
    C0 = 287
    return C0 * (273.15 + T) * (1 + w / 0.622) / (P * 1000)


def calculate_saturated_vapor_pressure(T: float) -> float:
    """
    Calculate saturation vapor pressure in kPa.

    Parameters:
    T  : Temperature in degrees Celsius

    Returns:
    Pg : Saturation vapor pressure in kPa
    """
    C0 = 0.61121
    C1 = 18.678
    C2 = 234.5
    C3 = 257.14
    return C0 * np.exp((C1 - T / C2) * (T / (C3 + T)))


def calculate_humidity_ratio(T: float, RH: float, P: float) -> float:
    """
    Calculate humidity ratio in kg_h2o/kg_dry.

    Parameters:
    T  : Temperature in degrees Celsius
    RH : Relative humidity in percent
    P  : Pressure in kPa

    Returns:
    w  : Humidity ratio in kg_h2o/kg_dry
    """
    C0 = 0.622
    Pg = calculate_saturated_vapor_pressure(T)
    return C0 * RH * Pg / 100 / (P - Pg * RH / 100)


def calculate_viscosity(T: float) -> float:
    """
    Calculate dynamic viscosity in kg/m.s.

    Parameters:
    T  : Temperature in degrees Celsius

    Returns:
    mu : Dynamic viscosity in kg/m.s
    """
    return 2.8E-7 * (T + 273.15) ** 0.735476


def calculate_Nusselt(Pitch: float, Width: float, L: float, Dh: float, Reynolds: float) -> float:
    """
    Calculate Nusselt number (Nu).

    Parameters:
    Pitch : Pitch of the channel
    Width : Width of the channel
    L  : Length in meters
    Dh : Hydraulic diameter in meters
    Reynolds : Reynolds number

    Returns:
    Nu : Nusselt number
    """
    ar = Pitch / Width  # Aspect ratio

    term1 = (8.234 * (1 - 2.0421 * ar + 3.0853 * ar**2 - 2.4765 * ar**3 +
                   1.0578 * ar**4 - 0.01861 * ar**5))**2
    term2 = (1.615 * Reynolds * 0.7 * Dh / L)**2
    return (term1 + term2) ** 0.5


def calculate_vaporization_enthalpy(T: float) -> float:
    """
    Calculate enthalpy of vaporization (hf) in J/kg.

    Parameters:
    T  : Temperature in degrees Celsius

    Returns:
    hf : Enthalpy of vaporization in J/kg
    """

    C0 = 2501
    C1 = 1.86
    return (C0 + C1 * T) * 1000


def calculate_temperature(e: float, w: float) -> float:
    """
    Calculate temperature in degrees Celsius from enthalpy and humidity ratio.

    Parameters:
    e  : Enthalpy in J/kg_d
    w  : Humidity ratio in kg/kg_d

    Returns:
    T  : Temperature in degrees Celsius
    """

    C0 = 1000
    C1 = 2501
    C2 = 1.006
    C3 = 1.86
    return (e / C0 - C1 * w) / (C2 +  C3* w)


def calculate_relative_humidity(T, w=None, P=None, TD=None):
    """
    Calculate relative humidity (RH) in percent.

    Parameters:
    T  : Temperature in degrees Celsius (required)
    w  : Humidity ratio in kg_h2o/kg_dry (optional, required if P is provided)
    P  : Pressure in kPa (optional, required if w is provided)
    TD : Dew Point in degrees Celsius (optional, alternative to w and P)

    Returns:
    RH : Relative humidity in percent
    """
    if w is not None and P is not None:
        C0 = 0.622
        Pg = calculate_saturated_vapor_pressure(T)
        return (w * P / (C0 + w) / Pg) * 100
    elif TD is not None:
        return 100 * (math.exp((17.625 * TD) / (243.04 + TD)) / math.exp((17.625 * T) / (243.04 + T)))
    else:
        raise ValueError("Invalid input: Provide either (T, w, P) or (T, TD)")


def calculate_dew_point(T: float, RH: float) -> float:
    """
    Calculate dew point temperature (DP) in degrees Celsius.

    Parameters:
    T  : Temperature in degrees Celsius
    RH : Relative humidity in percent

    Returns:
    DP : Dew point temperature in degrees Celsius
    """
    C0 = 243.12
    C1 = 17.62
    term1 = math.log(RH / 100) + (C1 * T) / (C0 + T)
    return C0 * term1 / (C1 - term1)


def calculate_Reynolds(Mass_flow: float, Hydraulic_diameter: float, Area: float, Viscosity: float) -> float:
    """
    Calculate the Reynolds Number.

    Parameters:
    Mass_flow          : Mass flow rate in kg/s
    Hydraulic_diameter : Hydraulic diameter in meters
    Area               : Cross-sectional area in square meters
    Viscosity          : Dynamic viscosity in kg/m.s

    Returns:
    Re : Reynolds Number
    """
    return Mass_flow * Hydraulic_diameter / Area / Viscosity
