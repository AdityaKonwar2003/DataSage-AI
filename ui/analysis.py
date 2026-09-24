import streamlit as st

from analysis.statistics import get_descriptive_statistics
from analysis.recommender import recommend_charts
from analysis.charts import generate_charts
from analysis.insights import (
    get_chart_insight,
    build_chart_context
)
from analysis.correlation import analyze_correlations
from analysis.anomaly import detect_anomalies
from analysis.root_cause import analyze_root_causes
from analysis.filters import get_filter_options, apply_filters
from llm.storyteller import explain_chart


def show_analysis(df, dataset_info, semantic_info):

    # ============================================================
    # OVERALL DATASET ANALYSIS
    # ============================================================

    st.header("📈 Descriptive Statistics")
    st.caption(
        "Statistical summary of all numeric columns in your dataset."
    )

    stats = get_descriptive_statistics(df)

    if not stats.empty:
        st.dataframe(stats, width="stretch")
    else:
        st.warning("No numeric columns found.")

    # ============================================================
    # SMART VISUALIZATIONS
    # ============================================================

    st.markdown("---")

    st.header("📊 Smart Visualizations")
    st.info(
        "DataSage automatically selects useful visualizations "
    "based on the structure and contents of your dataset."
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
        st.warning("No charts could be generated.")
    else:

        report_items = []

        for i, chart in enumerate(charts, start=1):

            recommendation = recommendations[i - 1]

            try:
                insight = get_chart_insight(
                    recommendation,
                    df
                )
            except Exception:
                insight = "Insight could not be generated."

            report_items.append({
                "path": f"report/charts/chart_{i}.png",
                "title": recommendation["title"],
                "insight": insight
            })

        st.session_state["report_items"] = report_items

        for i, chart in enumerate(charts, start=1):

            recommendation = recommendations[i - 1]

            st.markdown("---")

            st.subheader(
                f"📊 {recommendation['title']}"
            )

            st.plotly_chart(
                chart,
                width="stretch"
            )

            chart_insight = report_items[i - 1]["insight"]

            st.success(chart_insight)

            if st.button(
                f"🤖 Explain {recommendation['title']}",
                key=f"ai_{i}"
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

                st.info(explanation)

    # ============================================================
    # CORRELATION ANALYSIS
    # ============================================================

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

    else:

        positive = correlation_data["positive"]
        negative = correlation_data["negative"]

        if positive:

            st.success(
                f"""
### 🏆 Strongest Positive Correlation

**{positive['Column 1']} ↔ {positive['Column 2']}**

Correlation: **{positive['Correlation']}**

💡 These variables tend to increase together.
"""
            )

        if negative:

            st.warning(
                f"""
### ⚠ Strongest Negative Correlation

**{negative['Column 1']} ↔ {negative['Column 2']}**

Correlation: **{negative['Correlation']}**

💡 As one variable increases, the other tends to decrease.
"""
            )

        with st.expander(
            "📋 View Complete Correlation Matrix"
        ):

            st.dataframe(
                correlation_data["table"],
                width="stretch"
            )

    # ============================================================
    # ANOMALY DETECTION
    # ============================================================

    st.markdown("---")

    st.header("🚨 Anomaly Detection")

    st.caption(
        "Automatically identify unusual values in your numerical data using the IQR method."
    )

    anomaly_data, anomaly_summary = detect_anomalies(df)

    if not anomaly_summary:

        st.success(
            "✅ No significant anomalies detected in the numerical columns."
        )

    else:

        total_anomalies = len(anomaly_data)

        st.warning(
            f"⚠️ **{total_anomalies} rows** contain unusual values."
        )

        st.markdown("### 📊 Anomalies by Column")

        for item in anomaly_summary:

            st.write(
                f"**{item['Column']}** — "
                f"{item['Anomalies']} anomalies "
                f"(Normal range: "
                f"{item['Lower Bound']} → "
                f"{item['Upper Bound']})"
            )

        with st.expander(
            "🔎 View Anomalous Records"
        ):

            st.dataframe(
                anomaly_data,
                width="stretch"
            )

    # ============================================================
    # ROOT-CAUSE ANALYSIS
    # ============================================================

    st.markdown("---")

    st.header("🔍 Root-Cause Analysis")

    st.caption(
        "Identify categories and groups associated with unusually high or low values."
    )

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if not numeric_columns:

        st.warning(
            "No numerical columns are available for root-cause analysis."
        )

    else:

        target_column = st.selectbox(
            "🎯 Select a metric to analyze",
            numeric_columns,
            key="root_cause_target"
        )

        root_causes = analyze_root_causes(
            df,
            target_column
        )

        if not root_causes:

            st.info(
                "Not enough categorical information is available "
                "to perform root-cause analysis."
            )

        else:

            st.markdown(
                f"### 📊 Factors associated with `{target_column}`"
            )

            for result in root_causes[:5]:

                st.markdown(
                    f"""
**📌 {result['column']}**

🔼 **Highest:** {result['highest_group']}  
Average {target_column}: **{result['highest_mean']}**  
Difference from overall average:
**{result['highest_difference_percent']}%**

🔽 **Lowest:** {result['lowest_group']}  
Average {target_column}: **{result['lowest_mean']}**  
Difference from overall average:
**{result['lowest_difference_percent']}%**
"""
                )

                st.markdown("---")

    # ============================================================
    # INTERACTIVE DRILL-DOWN
    # ============================================================

    st.markdown("---")

    with st.expander(
        "🎛️ Explore Dataset Interactively",
        expanded=False
    ):

        st.caption(
            "Use filters to drill down into specific parts of your dataset."
        )

        filter_options = get_filter_options(df)

        filters = {}

        if filter_options:

            filter_columns = list(
                filter_options.keys()
            )

            filter_ui_columns = st.columns(
                min(len(filter_columns), 4)
            )

            for i, column in enumerate(
                filter_columns
            ):

                with filter_ui_columns[
                    i % 4
                ]:

                    selected_values = st.multiselect(
                        column,
                        options=filter_options[column],
                        default=[],
                        key=f"filter_{column}"
                    )

                    if selected_values:

                        filters[column] = selected_values

            filtered_df = apply_filters(
                df,
                filters
            )

            st.markdown("---")

            # Filter summary

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Original Rows",
                    f"{len(df):,}"
                )

            with col2:

                st.metric(
                    "Filtered Rows",
                    f"{len(filtered_df):,}"
                )

            with col3:

                if len(df) > 0:

                    percentage = (
                        len(filtered_df)
                        / len(df)
                    ) * 100

                else:

                    percentage = 0

                st.metric(
                    "Data Retained",
                    f"{percentage:.1f}%"
                )

            # ====================================================
            # FILTERED ANALYSIS
            # ====================================================

            if filtered_df.empty:

                st.warning(
                    "⚠️ No records match the selected filters."
                )

            elif not filters:

                st.info(
                    "Select one or more filters above to "
                    "perform a focused analysis."
                )

            else:

                st.markdown(
                    "### 📊 Filtered Dataset Summary"
                )

                filtered_stats = get_descriptive_statistics(
                    filtered_df
                )

                if not filtered_stats.empty:

                    st.dataframe(
                        filtered_stats,
                        width="stretch"
                    )

                # Filtered anomalies

                st.markdown(
                    "### 🚨 Filtered Anomalies"
                )

                filtered_anomaly_data, filtered_anomaly_summary = (
                    detect_anomalies(filtered_df)
                )

                if filtered_anomaly_summary:

                    st.warning(
                        f"⚠️ {len(filtered_anomaly_data)} "
                        "filtered rows contain unusual values."
                    )

                    with st.expander(
                        "🔎 View Filtered Anomalies"
                    ):

                        st.dataframe(
                            filtered_anomaly_data,
                            width="stretch"
                        )

                else:

                    st.success(
                        "✅ No significant anomalies detected "
                        "in the filtered data."
                    )

                # Filtered correlation

                st.markdown(
                    "### 🔥 Filtered Correlation"
                )

                filtered_correlation = analyze_correlations(
                    filtered_df
                )

                if filtered_correlation:

                    positive = filtered_correlation["positive"]
                    negative = filtered_correlation["negative"]

                    if positive:

                        st.write(
                            f"**Positive:** "
                            f"{positive['Column 1']} ↔ "
                            f"{positive['Column 2']} "
                            f"({positive['Correlation']})"
                        )

                    if negative:

                        st.write(
                            f"**Negative:** "
                            f"{negative['Column 1']} ↔ "
                            f"{negative['Column 2']} "
                            f"({negative['Correlation']})"
                        )

                # Filtered root cause

                st.markdown(
                    "### 🔍 Filtered Root-Cause Analysis"
                )

                filtered_numeric_columns = (
                    filtered_df
                    .select_dtypes(
                        include="number"
                    )
                    .columns
                    .tolist()
                )

                if filtered_numeric_columns:

                    filtered_target = st.selectbox(
                        "🎯 Select metric",
                        filtered_numeric_columns,
                        key="filtered_root_cause_target"
                    )

                    filtered_root_causes = (
                        analyze_root_causes(
                            filtered_df,
                            filtered_target
                        )
                    )

                    if filtered_root_causes:

                        for result in filtered_root_causes[:3]:

                            st.write(
                                f"**{result['column']}** — "
                                f"Highest: "
                                f"{result['highest_group']} "
                                f"({result['highest_mean']}) | "
                                f"Lowest: "
                                f"{result['lowest_group']} "
                                f"({result['lowest_mean']})"
                            )

                    else:

                        st.info(
                            "Not enough data for filtered "
                            "root-cause analysis."
                        )