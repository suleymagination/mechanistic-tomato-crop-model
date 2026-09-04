import numpy as np

def calculate_gross_photosynthesis(par_ppfd: float, co2_ppm: float, p_max: float = 30.0, alpha: float = 0.045) -> float:
    """
    Calculates gross photosynthetic rate (umol CO2/m2/s) using a non-rectangular hyperbola
    light response curve modulated by CO2 concentration.
    """
    co2_factor = co2_ppm / (co2_ppm + 250.0)
    p_gross = (p_max * co2_factor) * (1.0 - np.exp(-alpha * par_ppfd / (p_max * co2_factor)))
    return max(0.0, p_gross)

def calculate_vpd(temp_c: float, rh_pct: float) -> float:
    """Calculates Vapor Pressure Deficit (VPD in kPa)."""
    vpsat = 0.61078 * np.exp((17.27 * temp_c) / (temp_c + 237.3))
    vpack = vpsat * (rh_pct / 100.0)
    return vpsat - vpack

def calculate_canopy_transpiration(vpd_kpa: float, dli_mol_m2_day: float) -> float:
    """Estimates daily transpiration (L/m2/day) based on VPD and light load."""
    transpiration = (0.15 * vpd_kpa + 0.02 * dli_mol_m2_day)
    return max(0.0, transpiration)
