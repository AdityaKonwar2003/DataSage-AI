import streamlit as st

from analysis.statistics import (
    get_dataset_summary,
    get_column_types
)


def show_overview(df, cleaning_report, dataset_info):

    # =====================================================
    # DATASET PREVIEW
    # =====================================================

    st.header("📂 Dataset Preview")
    st.dataframe(df.head(), width="stretch")

    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    st.markdown("---")

    st.header("📈 Dataset Overview")

    summary = get_dataset_summary(df)

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "📄 Rows",
            f"{summary['Rows']:,}"
        )

    with c2:
        st.metric(
            "📊 Columns",
            summary["Columns"]
        )

    with c3:
        st.metric(
            "❗ Missing",
            summary["Missing Values"]
        )

    with c4:
        st.metric(
            "📋 Duplicates",
            summary["Duplicate Rows"]
        )

    with c5:
        memory = round(summary["Memory Usage (KB)"] / 1024, 2)

        st.metric(
            "💾 Memory",
            f"{memory} MB"
        )

    # =====================================================
    # DATASET HEALTH
    # =====================================================

    st.markdown("---")

    st.header("🩺 Dataset Health")

    h1, h2, h3 = st.columns(3)

    with h1:

        if summary["Missing Values"] == 0:
            st.success("✅ No Missing Values")
        else:
            st.warning(
                f"⚠ {summary['Missing Values']} Missing Values"
            )

    with h2:

        if summary["Duplicate Rows"] == 0:
            st.success("✅ No Duplicate Rows")
        else:
            st.warning(
                f"⚠ {summary['Duplicate Rows']} Duplicate Rows"
            )

    with h3:

        if len(dataset_info["numeric"]) >= 2:
            st.success("✅ Suitable for Analysis")
        else:
            st.warning(
                "⚠ Limited Numeric Features"
            )

    # =====================================================
    # DATA CLEANING
    # =====================================================

    st.markdown("---")

    st.header("🧹 Data Cleaning Summary")

    if cleaning_report:

        for item in cleaning_report:
            st.success(item)

    else:
        st.info("No cleaning operations were required.")

    # =====================================================
    # DATASET DETECTION
    # =====================================================

    st.markdown("---")

    st.header("🧠 Dataset Detection")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.metric(
            "🔢 Numeric",
            len(dataset_info["numeric"])
        )

    with d2:
        st.metric(
            "📝 Categorical",
            len(dataset_info["categorical"])
        )

    with d3:
        st.metric(
            "📅 Date",
            len(dataset_info["datetime"])
        )

    with st.expander("🔢 Numeric Columns"):

        if dataset_info["numeric"]:
            st.write(dataset_info["numeric"])
        else:
            st.info("No numeric columns detected.")

    with st.expander("📝 Categorical Columns"):

        if dataset_info["categorical"]:
            st.write(dataset_info["categorical"])
        else:
            st.info("No categorical columns detected.")

    with st.expander("📅 Date Columns"):

        if dataset_info["datetime"]:
            st.write(dataset_info["datetime"])
        else:
            st.info("No date columns detected.")

    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    st.markdown("---")

    st.header("📑 Column Information")

    st.dataframe(
        get_column_types(df),
        width="stretch"
    )