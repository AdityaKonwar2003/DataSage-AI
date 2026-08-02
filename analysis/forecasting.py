import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from prophet import Prophet
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
    Forecast using Facebook Prophet.
    """

    df = forecast_df.rename(
        columns={
            date_column: "ds",
            target_column: "y"
        }
    )

    model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.15,
    interval_width=0.95
)

    model.fit(df)

    future = model.make_future_dataframe(
        periods=periods
    )

    forecast = model.predict(future)

    forecast = forecast.tail(periods)

    forecast = forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ]

    forecast.columns = [
        date_column,
        "Prediction",
        "Lower",
        "Upper"
    ]

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
    Professional Business Forecast Chart
    """

    fig = go.Figure()

    # =====================================================
    # Historical Data
    # =====================================================

    fig.add_trace(
        go.Scatter(
    x=historical_df[date_column],
    y=historical_df[target_column],
    mode="lines+markers",
    name="Historical",
    line=dict(
        color="royalblue",
        width=3
    ),
    marker=dict(size=5),

    hovertemplate=
        "<b>Date:</b> %{x}<br>"
        "<b>Actual:</b> %{y:.2f}"
        "<extra></extra>"
)
    )

    # =====================================================
    # Confidence Interval
    # =====================================================

    fig.add_trace(
        go.Scatter(
            x=pd.concat([
                forecast_df[date_column],
                forecast_df[date_column][::-1]
            ]),
            y=pd.concat([
                forecast_df["Upper"],
                forecast_df["Lower"][::-1]
            ]),
            fill="toself",
            fillcolor="rgba(255,99,71,0.20)",
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=True,
            name="Confidence Interval"
        )
    )

    # =====================================================
    # Forecast
    # =====================================================

    fig.add_trace(
        go.Scatter(
            x=forecast_df[date_column],
            y=forecast_df["Prediction"],
            mode="lines",
            name="Forecast",
            line=dict(
        color="tomato",
        width=4,
        dash="dash"
    ),

    hovertemplate=
        "<b>Date:</b> %{x}<br>"
        "<b>Forecast:</b> %{y:.2f}"
        "<extra></extra>"
)
    )
    # =====================================================
    # Forecast Start Line
    # =====================================================

    forecast_start = forecast_df[date_column].iloc[0]
    fig.add_vrect(
    x0=forecast_start,
    x1=forecast_df[date_column].iloc[-1],
    fillcolor="rgba(255,165,0,0.08)",
    layer="below",
    line_width=0
)
    fig.add_vline(
        x=forecast_start,
        line_width=2,
        line_dash="dot",
        line_color="green",
        annotation_text="Forecast Starts",
        annotation_position="top"
    )

    # =====================================================
    # Layout
    # =====================================================

    fig.update_layout(

    title={
        "text": f"📈 {target_column} Forecast using Prophet",
        "x": 0.5,
        "xanchor": "center"
    },

    template="plotly_dark",

    hovermode="x unified",

    dragmode="zoom",

    xaxis=dict(
        title="Date",
        rangeslider=dict(
            visible=True
        )
    ),

    yaxis_title=target_column,

    legend=dict(
        orientation="h",
        y=1.10,
        x=0.5,
        xanchor="center"
    ),

    height=650
)
    return fig
    