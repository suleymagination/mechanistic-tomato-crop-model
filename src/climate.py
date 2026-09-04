from pathlib import Path
import pandas as pd


class ClimateDataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath)
        df["time"] = pd.to_datetime(df["time"], utc=True)
        # Convert PPFD (umol/m2/s) to mol/m2/s
        df["par_mol_m2_s"] = df["par_ppfd"] * 1e-6
        return df

    def get_daily_summaries(self, df: pd.DataFrame) -> pd.DataFrame:
        df["date"] = df["time"].dt.date
        
        # Aggregate 5-minute time-series into daily physiological parameters
        agg_dict = {
            "temp_c": "mean",
            "rh_pct": "mean",
            "co2_ppm": "mean",
            "par_mol_m2_s": lambda x: x.sum() * 300,  # 300 seconds per 5-min interval
        }
        
        if "plant_density" in df.columns:
            agg_dict["plant_density"] = "mean"

        daily = df.groupby("date").agg(agg_dict).reset_index()
        daily.rename(columns={"par_mol_m2_s": "dli_mol_m2_day"}, inplace=True)
        return daily
