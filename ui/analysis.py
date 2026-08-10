import os
import streamlit as st

from analysis.statistics import get_descriptive_statistics
from analysis.recommender import recommend_charts
from analysis.charts import generate_charts
from analysis.insights import (
    get_chart_insight,
    build_chart_context
)
from analysis.correlation import analyze_correlations

from llm.storyteller import explain_chart


def show_analysis(df, dataset_info, semantic_info):

    # =====================================================
    # DESCRIPTIVE STATISTICS
    # =====================================================

    st.header("📈 Descriptive Statistics")

    st.caption(
        "Statistical summary of all numeric columns in your dataset."
    )

    stats = get_descriptive_statistics(df)

    if not stats.empty:

        st.dataframe(
            stats,
            width="stretch"
        )

    else:

        st.warning(
            "No numeric columns found."
        )

    # =====================================================
    # SMART VISUALIZATIONS
    # =====================================================

    st.markdown("---")

    st.header("📊 Smart Visualizations")

    st.info(
        "The charts below were automatically selected based on your dataset."
    )

    recommendations = recommend_charts(
        df,
        dataset_info,
        semantic_info
    )

    charts = generate_charts(
        df,
        recommendations
    )

    if not charts:

        st.warning(
            "No charts could be generated."
        )

        return

    # =====================================================
    # GET GENERATED PDF CHART PATHS
    # =====================================================

    os.makedirs(
        "report/charts",
        exist_ok=True
    )

    chart_paths = []

    for i in range(1, len(charts) + 1):

        chart_path = (
            f"report/charts/chart_{i}.png"
        )

        if os.path.exists(chart_path):

            chart_paths.append(
                chart_path
            )

    # Save paths for PDF Report
    st.session_state["report_charts"] = chart_paths

    # =====================================================
    # CHARTS
    # =====================================================

    for recommendation, chart in zip(
        recommendations,
        charts
    ):

        st.markdown("---")

        st.subheader(
            f"📊 {recommendation['title']}"
        )

        # Interactive Plotly chart
        st.plotly_chart(
            chart,
            width="stretch"
        )

        # =================================================
        # CHART INSIGHT
        # =================================================

        st.success(
            get_chart_insight(
                recommendation,
                df
            )
        )

        # =================================================
        # AI EXPLANATION
        # =================================================

        if st.button(
            f"🤖 Explain {recommendation['title']}",
            key=f"ai_{recommendation['title']}"
        ):

            context = build_chart_context(
                recommendation,
                df
            )

            with st.spinner(
                "Generating AI explanation..."
            ):

                explanation = explain_chart(
                    context
                )

            st.info(
                explanation
            )

    # =====================================================
    # CORRELATION ANALYSIS
    # =====================================================

    st.markdown("---")

    st.header("🔥 Correlation Analysis")

    st.caption(
        "Discover the strongest relationships between numeric variables."
    )

    correlation_data = analyze_correlations(df)

    if correlation_data is None:

        st.warning(
            "Not enough numeric columns available."
        )

        return

    positive = correlation_data["positive"]
    negative = correlation_data["negative"]

    # =====================================================
    # POSITIVE CORRELATION
    # =====================================================

    if positive:

        st.success(
            f"""
### 🏆 Strongest Positive Correlation

**{positive['Column 1']} ↔ {positive['Column 2']}**

Correlation: **{positive['Correlation']}**

💡 These variables tend to increase together.
"""
        )

    # =====================================================
    # NEGATIVE CORRELATION
    # =====================================================

    if negative:

        st.warning(
            f"""
### ⚠ Strongest Negative Correlation

**{negative['Column 1']} ↔ {negative['Column 2']}**

Correlation: **{negative['Correlation']}**

💡 As one variable increases, the other tends to decrease.
"""
        )

    # =====================================================
    # COMPLETE CORRELATION MATRIX
    # =====================================================

    with st.expander(
        "📋 View Complete Correlation Matrix"
    ):

        st.dataframe(
            correlation_data["table"],
            width="stretch"
        )