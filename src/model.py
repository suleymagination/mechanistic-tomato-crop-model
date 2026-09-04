import numpy as np
import pandas as pd
from src.physiology import calculate_canopy_transpiration, calculate_vpd


class TomatoCropModel:
    def __init__(self, plant_density: float = 25.3, lue_g_mol: float = 8.4, dm_content: float = 0.066):
        self.plant_density = plant_density  # Default fallback density (pots/m2)
        self.lue_g_mol = lue_g_mol          # Light Use Efficiency (g FW/mol PAR)
        self.dm_content = dm_content        # Fruit dry matter content (WUR 3.06 = 6.6%)

    def run_simulation(self, daily_climate: pd.DataFrame) -> pd.DataFrame:
        results = []
        cumulative_dw_g_m2 = 0.0
        total_days = len(daily_climate)

        for idx, row in daily_climate.iterrows():
            dli = row["dli_mol_m2_day"]
            temp = row["temp_c"]
            rh = row["rh_pct"]

            # Dynamic plant density from climate dataset (56 -> 42 -> 30 -> 20)
            density = row.get("plant_density", self.plant_density)

            # Daily dry matter accumulation (g DW/m2/day)
            daily_dw_g_m2 = dli * (self.lue_g_mol * 0.07)
            cumulative_dw_g_m2 += daily_dw_g_m2

            # Generative carbon allocation (onset after initial vegetative phase)
            progress = (idx + 1) / total_days
            fruit_allocation = min(0.65, max(0.0, (progress - 0.20) * 0.80))
            fruit_dw_g_m2 = cumulative_dw_g_m2 * fruit_allocation

            # Fruit ripening S-curve transition (green to red fruit maturation)
            ripeness_fraction = 1.0 / (1.0 + np.exp(-0.30 * (idx - 62)))
            red_fruit_dw_g_m2 = fruit_dw_g_m2 * ripeness_fraction

            # Convert to red fruit fresh weight per pot (g FW/pot)
            fruit_fw_g_pot = (red_fruit_dw_g_m2 / self.dm_content) / density

            vpd = calculate_vpd(temp, rh)
            water_use_l_m2 = calculate_canopy_transpiration(vpd, dli)

            results.append({
                "day": idx + 1,
                "date": row["date"],
                "biomass_dw_g_m2": round(cumulative_dw_g_m2, 2),
                "fruit_fw_g_pot": round(fruit_fw_g_pot, 2),
                "water_use_l_m2": round(water_use_l_m2, 2),
                "vpd_kpa": round(vpd, 2),
            })

        return pd.DataFrame(results)
