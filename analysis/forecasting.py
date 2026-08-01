import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor

import plotly.graph_objects as go


# =====================================================
# PREPARE DATA
# =====================================================

def prepare_forecast_data(df, semantic_info):
    """
    Prepare the dataset for forecasting.

    Returns:
        (forecast_df, date_column, target_column)

    If forecasting is not possible:
        (None, None, None)
    """

    date_column = semantic_info.get("date")
    kpis = semantic_info.get("kpi", [])

    if date_column is None:
        return None, None, None

    if len(kpis) == 0:
        return None, None, None

    target_column = kpis[0]

    forecast_df = df[[date_column, target_column]].copy()

    forecast_df[date_column] = pd.to_datetime(
        forecast_df[date_column],
        errors="coerce"
    )

    forecast_df[target_column] = pd.to_numeric(
        forecast_df[target_column],
        errors="coerce"
    )

    forecast_df = forecast_df.dropna()

    forecast_df = forecast_df.sort_values(date_column)

    return forecast_df, date_column, target_column


# =====================================================
# FORECAST
# =====================================================

def forecast_values(
    forecast_df,
    date_column,
    target_column,
    periods=30
):
    """
    Forecast future values using Random Forest Regression.
    """

    df = forecast_df.copy()

    df["Day_Number"] = (
        df[date_column] - df[date_column].min()
    ).dt.days

    X = df[["Day_Number"]]
    y = df[target_column]

    # -----------------------------
    # Random Forest Model
    # -----------------------------

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=10,
        random_state=42
    )

    model.fit(X, y)

    # -----------------------------
    # Future Days
    # -----------------------------

    last_day = df["Day_Number"].max()

    future_days = np.arange(
        last_day + 1,
        last_day + periods + 1
    )

    future_X = pd.DataFrame({
        "Day_Number": future_days
    })

    future_predictions = model.predict(future_X)

    # -----------------------------
    # Future Dates
    # -----------------------------

    frequency = pd.infer_freq(df[date_column])

    if frequency is None:
        frequency = "D"

    future_dates = pd.date_range(
        start=df[date_column].max(),
        periods=periods + 1,
        freq=frequency
    )[1:]

    forecast = pd.DataFrame({
        date_column: future_dates,
        "Prediction": future_predictions
    })

    return forecast


# =====================================================
# FORECAST CHART
# =====================================================

def create_forecast_chart(
    historical_df,
    forecast_df,
    date_column,
    target_column
):
    """
    Create an interactive forecast chart.
    """

    fig = go.Figure()

    # Historical

    fig.add_trace(
        go.Scatter(
            x=historical_df[date_column],
            y=historical_df[target_column],
            mode="lines+markers",
            name="Historical",
            line=dict(
                color="royalblue",
                width=3
            )
        )
    )

    # Forecast

    fig.add_trace(
        go.Scatter(
            x=forecast_df[date_column],
            y=forecast_df["Prediction"],
            mode="lines+markers",
            name="Forecast",
            line=dict(
                color="tomato",
                width=3,
                dash="dash"
            )
        )
    )

    fig.update_layout(

        title=f"{target_column} Forecast",

        template="plotly_white",

        hovermode="x unified",

        xaxis_title="Date",

        yaxis_title=target_column,

        legend=dict(
            orientation="h",
            y=1.08,
            x=0.75
        ),

        height=600
    )

    return fig