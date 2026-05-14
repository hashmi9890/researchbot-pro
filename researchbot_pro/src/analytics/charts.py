"""
Chart Engine
------------
Plotly se professional charts banata hai.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


class ChartEngine:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def correlation_heatmap(self):
        """Numeric columns ka correlation heatmap"""
        numeric_df = self.df.select_dtypes(include=[np.number])
        if numeric_df.empty or len(numeric_df.columns) < 2:
            return None

        corr = numeric_df.corr().round(2)
        fig  = px.imshow(
            corr,
            title    = "Correlation Heatmap",
            color_continuous_scale = "RdBu_r",
            aspect   = "auto",
        )
        return fig

    def missing_values_chart(self):
        """Missing values bar chart"""
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if missing.empty:
            return None

        fig = px.bar(
            x     = missing.index,
            y     = missing.values,
            title = "Missing Values by Column",
            labels = {"x": "Column", "y": "Missing Count"},
            color = missing.values,
            color_continuous_scale = "Reds",
        )
        return fig

    def distribution_chart(self, column: str):
        """Column ka distribution"""
        if column not in self.df.columns:
            return None

        if self.df[column].dtype in [np.float64, np.int64]:
            fig = px.histogram(
                self.df,
                x     = column,
                title = f"Distribution: {column}",
                nbins = 30,
                color_discrete_sequence = ["#7b2ff7"],
            )
        else:
            counts = self.df[column].value_counts().head(20)
            fig = px.bar(
                x     = counts.index,
                y     = counts.values,
                title = f"Top Values: {column}",
                labels = {"x": column, "y": "Count"},
                color_discrete_sequence = ["#00d2ff"],
            )
        return fig

    def trend_chart(self, x_col: str, y_col: str):
        """Trend line chart"""
        if x_col not in self.df.columns or y_col not in self.df.columns:
            return None

        fig = px.line(
            self.df,
            x     = x_col,
            y     = y_col,
            title = f"Trend: {y_col} over {x_col}",
            color_discrete_sequence = ["#00d2ff"],
        )
        return fig

    def kpi_summary_chart(self, numeric_cols: list):
        """KPI summary bar chart"""
        if not numeric_cols:
            return None

        means = self.df[numeric_cols].mean().round(2)
        fig   = px.bar(
            x     = means.index,
            y     = means.values,
            title = "KPI Averages",
            labels = {"x": "Metric", "y": "Average Value"},
            color = means.values,
            color_continuous_scale = "Viridis",
        )
        return fig