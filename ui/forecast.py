import streamlit as st

from llm.storyteller import explain_forecast

from analysis.forecasting import (
    prepare_forecast_data,
    forecast_values,
    create_forecast_chart
)

def show_forecast(df, semantic_info):

    # =====================================================
    # HEADER
    # =====================================================

    st.header("🔮 Forecast Dashboard")

    st.caption(
        "Predict future trends using Machine Learning and receive "
        "AI-powered business explanations."
    )

    # =====================================================
    # PREPARE FORECAST DATA
    # =====================================================

    forecast_df, date_col, target = prepare_forecast_data(
        df,
        semantic_info
    )

    if forecast_df is None:

        st.warning(
            "Forecasting is not available for this dataset."
        )

        return

    st.success("✅ Forecast-ready dataset detected!")

    # =====================================================
    # FORECAST CONFIGURATION
    # =====================================================

    st.markdown("---")

    st.subheader("⚙️ Forecast Configuration")

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            f"📅 **Date Column**\n\n{date_col}"
        )

    with c2:

        st.info(
            f"🎯 **Target KPI**\n\n{target}"
        )

    # =====================================================
    # DATA PREVIEW
    # =====================================================

    st.markdown("---")

    st.subheader("📋 Forecast Dataset Preview")

    st.dataframe(
        forecast_df.head(),
        width="stretch"
    )

    # =====================================================
    # SETTINGS
    # =====================================================

    st.markdown("---")

    st.subheader("📅 Forecast Settings")

    forecast_option = st.selectbox(
    "Forecast Period",
    [
        "1 Month",
        "3 Months",
        "6 Months",
        "1 Year"
    ],
    index=1
)

    forecast_map = {
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365
}

    forecast_days = forecast_map[forecast_option]
    st.session_state["forecast_period_label"] = forecast_option

    # =====================================================
    # GENERATE FORECAST
    # =====================================================

    if st.button("📈 Generate Forecast"):

        with st.spinner("Training forecasting model..."):

            forecast = forecast_values(
                forecast_df,
                date_col,
                target,
                forecast_days
            )

            chart = create_forecast_chart(
                forecast_df,
                forecast,
                date_col,
                target
            )

            first_prediction = forecast["Prediction"].iloc[0]
            last_prediction = forecast["Prediction"].iloc[-1]

            growth = (
                (last_prediction - first_prediction)
                / first_prediction
            ) * 100

            explanation = explain_forecast(
                target,
                growth,
                forecast_days
            )

        # ============================================
        # SAVE EVERYTHING
        # ============================================

        st.session_state["forecast"] = forecast
        st.session_state["forecast_chart"] = chart
        st.session_state["forecast_growth"] = growth
        st.session_state["forecast_days"] = forecast_days
        st.session_state["forecast_target"] = target
        st.session_state["forecast_explanation"] = explanation

        st.success("✅ Forecast Generated Successfully!")

    # =====================================================
    # DISPLAY SAVED FORECAST
    # =====================================================

    if "forecast" not in st.session_state:

        return

    forecast = st.session_state["forecast"]
    chart = st.session_state["forecast_chart"]
    growth = st.session_state["forecast_growth"]
    forecast_days = st.session_state["forecast_days"]
    target = st.session_state["forecast_target"]
    explanation = st.session_state["forecast_explanation"]

    
       # =====================================================
    # FORECAST SUMMARY
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Forecast Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "📅 Forecast Period",
             st.session_state.get(
            "forecast_period_label",
            f"{forecast_days} Days"
        )
        )

    with c2:
        st.metric(
            "📈 Predicted Growth",
            f"{growth:.2f}%"
        )

    with c3:
        st.metric(
            "🎯 Target KPI",
            target
        )

    st.info(
        """
🤖 **Forecast Model**

This forecast is generated using the **Facebook Prophet** time-series forecasting model.

Prophet automatically identifies historical trends and seasonal patterns to predict future values. The forecast also includes a **95% confidence interval**, providing a realistic range of possible future outcomes.

This model is widely used for business forecasting applications such as sales, demand, revenue, and KPI prediction.

"""
    )

    # =====================================================
    # FORECAST VISUALIZATION
    # =====================================================

    st.markdown("---")

    st.subheader("📈 Forecast Visualization")

    st.plotly_chart(
        chart,
        width="stretch"
    )

    # =====================================================
    # FORECAST TABLE
    # =====================================================

    st.markdown("---")

    st.subheader("📋 Forecast Results")

    st.caption(
        "Predicted values generated by the forecasting model."
    )

    st.dataframe(
        forecast,
        width="stretch"
    )

    # =====================================================
    # AI FORECAST EXPLANATION
    # =====================================================

    st.markdown("---")

    st.subheader("🤖 AI Forecast Explanation")

    st.info(
        "AI interprets the forecast and provides business-focused recommendations."
    )

    st.markdown(explanation)