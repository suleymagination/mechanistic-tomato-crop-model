import pandas as pd
from src.physiology import calculate_canopy_transpiration, calculate_vpd


class TomatoCropModel:
    def __init__(self, plant_density: float = 39.7, lue_g_mol: float = 8.4):
        self.plant_density = plant_density  # pots/m2
        self.lue_g_mol = lue_g_mol          # Reference Light Use Efficiency (g FW/mol PAR)

    def run_simulation(self, daily_climate: pd.DataFrame) -> pd.DataFrame:
        results = []
        cumulative_biomass_dw_g_m2 = 0.0

        total_days = len(daily_climate)

        for idx, row in daily_climate.iterrows():
            dli = row["dli_mol_m2_day"]
            temp = row["temp_c"]
            rh = row["rh_pct"]
            
            # Use dynamic density if present in dataset, else default
            density = row.get("plant_density", self.plant_density)

            # Daily dry weight accumulation (g DW/m2/day)
            daily_dw_g_m2 = dli * (self.lue_g_mol * 0.07)
            cumulative_biomass_dw_g_m2 += daily_dw_g_m2

            # Generative allocation ratio increases as plants mature
            progress = (idx + 1) / total_days
            fruit_allocation = min(0.65, 0.05 + progress * 0.60)
            fruit_dw_g_m2 = cumulative_biomass_dw_g_m2 * fruit_allocation

            # Convert to fresh fruit weight per pot (assuming ~7% dry matter content)
            fruit_fw_g_pot = (fruit_dw_g_m2 / 0.07) / density

            vpd = calculate_vpd(temp, rh)
            water_use_l_m2 = calculate_canopy_transpiration(vpd, dli)

            results.append({
                "day": idx + 1,
                "date": row["date"],
                "biomass_dw_g_m2": round(cumulative_biomass_dw_g_m2, 2),
                "fruit_fw_g_pot": round(fruit_fw_g_pot, 2),
                "water_use_l_m2": round(water_use_l_m2, 2),
                "vpd_kpa": round(vpd, 2),
            })

        return pd.DataFrame(results)
