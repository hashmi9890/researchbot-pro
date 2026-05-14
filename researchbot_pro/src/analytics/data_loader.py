"""
Data Loader
-----------
CSV / Excel files load karta hai aur basic profiling karta hai.
"""

import pandas as pd
import numpy as np
from pathlib import Path


class DataLoader:

    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.df        = None

    def load(self) -> pd.DataFrame:
        """File load karo"""
        suffix = self.file_path.suffix.lower()
        if suffix == ".csv":
            self.df = pd.read_csv(self.file_path)
        elif suffix in [".xlsx", ".xls"]:
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Unsupported file: {suffix}")
        return self.df

    def profile(self) -> dict:
        """Basic data profile"""
        if self.df is None:
            self.load()

        df = self.df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        profile = {
            "rows"          : len(df),
            "columns"       : len(df.columns),
            "column_names"  : df.columns.tolist(),
            "numeric_cols"  : numeric_cols,
            "categorical_cols": df.select_dtypes(include=["object"]).columns.tolist(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_pct"   : (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
            "dtypes"        : df.dtypes.astype(str).to_dict(),
            "duplicates"    : int(df.duplicated().sum()),
        }

        if numeric_cols:
            profile["summary_stats"] = df[numeric_cols].describe().round(2).to_dict()

        return profile

    def get_kpis(self) -> dict:
        """Numeric columns ke basic KPIs"""
        if self.df is None:
            self.load()

        df = self.df
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        kpis = {}

        for col in numeric_cols:
            kpis[col] = {
                "total"  : round(float(df[col].sum()), 2),
                "mean"   : round(float(df[col].mean()), 2),
                "median" : round(float(df[col].median()), 2),
                "max"    : round(float(df[col].max()), 2),
                "min"    : round(float(df[col].min()), 2),
                "std"    : round(float(df[col].std()), 2),
            }

        return kpis