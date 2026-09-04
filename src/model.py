import pandas as pd
from src.physiology import calculate_gross_photosynthesis, calculate_vpd, calculate_canopy_transpiration

class TomatoCropModel:
    def __init__(self, plant_density: float = 39.7, lue_g_mol: float = 9.5):
        self.plant_density = plant_density  # pots/m2
        self.lue_g_mol = lue_g_mol          # Light Use Efficiency (g DW/mol PAR)
        
    def run_simulation(self, daily_climate: pd.DataFrame) -> pd.DataFrame:
        results = []
        cumulative_biomass_g_m2 = 0.0
        
        for idx, row in daily_climate.iterrows():
            dli = row['dli_mol_m2_day']
            temp = row['temp_c']
            rh = row['rh_pct']
            
            # Daily dry matter production via LUE
            daily_dw_g_m2 = dli * (self.lue_g_mol * 0.40) # Dry weight conversion factor
            cumulative_biomass_g_m2 += daily_dw_g_m2
            
            # Carbon allocation to fruits increases with plant maturity
            fruit_allocation = min(0.65, 0.10 + (idx / len(daily_climate)) * 0.55)
            fruit_dw_g_m2 = cumulative_biomass_g_m2 * fruit_allocation
            
            # Fresh weight estimate (assuming ~7% dry matter content)
            fruit_fw_g_pot = (fruit_dw_g_m2 / 0.07) / self.plant_density
            
            vpd = calculate_vpd(temp, rh)
            water_use_l_m2 = calculate_canopy_transpiration(vpd, dli)
            
            results.append({
                'day': idx + 1,
                'date': row['date'],
                'biomass_dw_g_m2': cumulative_biomass_g_m2,
                'fruit_fw_g_pot': fruit_fw_g_pot,
                'water_use_l_m2': water_use_l_m2
            })
            
        return pd.DataFrame(results)
