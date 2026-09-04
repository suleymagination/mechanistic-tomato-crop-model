import pandas as pd

class ClimateDataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath)
        df['time'] = pd.to_datetime(df['time'])
        # Compute daily integrals (DLI: Daily Light Integral in mol/m2/day)
        df['par_mol_m2_s'] = df['par_ppfd'] * 1e-6
        return df

    def get_daily_summaries(self, df: pd.DataFrame) -> pd.DataFrame:
        df['date'] = df['time'].dt.date
        daily = df.groupby('date').agg({
            'temp_c': 'mean',
            'rh_pct': 'mean',
            'co2_ppm': 'mean',
            'par_mol_m2_s': lambda x: x.sum() * 3600  # 1-hour interval aggregation
        }).reset_index()
        daily.rename(columns={'par_mol_m2_s': 'dli_mol_m2_day'}, inplace=True)
        return daily
