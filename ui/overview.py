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

    st.dataframe(
        df.head(),
        width="stretch"
    )

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

        memory = round(
            summary["Memory Usage (KB)"] / 1024,
            2
        )

        st.metric(
            "💾 Memory",
            f"{memory} MB"
        )

    # =====================================================
    # DATASET HEALTH
    # =====================================================

    st.markdown("---")

    st.header("🩺 Dataset Health")

    health_cards = ""

    # Missing values
    if summary["Missing Values"] == 0:

        health_cards += """
        <div class="health-card">
            <span class="health-icon">✓</span>
            <div>
                <div class="health-title">
                    No Missing Values
                </div>
                <div class="health-description">
                    Dataset is complete
                </div>
            </div>
        </div>
        """

    else:

        health_cards += f"""
        <div class="health-card warning-card">
            <span class="health-icon warning-icon">!</span>
            <div>
                <div class="health-title">
                    {summary["Missing Values"]:,} Missing Values
                </div>
                <div class="health-description">
                    Missing data detected
                </div>
            </div>
        </div>
        """

    # Duplicate rows
    if summary["Duplicate Rows"] == 0:

        health_cards += """
        <div class="health-card">
            <span class="health-icon">✓</span>
            <div>
                <div class="health-title">
                    No Duplicate Rows
                </div>
                <div class="health-description">
                    No duplicate records detected
                </div>
            </div>
        </div>
        """

    else:

        health_cards += f"""
        <div class="health-card warning-card">
            <span class="health-icon warning-icon">!</span>
            <div>
                <div class="health-title">
                    {summary["Duplicate Rows"]:,} Duplicate Rows
                </div>
                <div class="health-description">
                    Duplicate records detected
                </div>
            </div>
        </div>
        """

    # Numeric features
    if len(dataset_info["numeric"]) >= 2:

        health_cards += """
        <div class="health-card">
            <span class="health-icon">✓</span>
            <div>
                <div class="health-title">
                    Suitable for Analysis
                </div>
                <div class="health-description">
                    Sufficient numeric features detected
                </div>
            </div>
        </div>
        """

    else:

        health_cards += """
        <div class="health-card warning-card">
            <span class="health-icon warning-icon">!</span>
            <div>
                <div class="health-title">
                    Limited Numeric Features
                </div>
                <div class="health-description">
                    Limited numerical data available
                </div>
            </div>
        </div>
        """

    st.markdown(
        f"""
        <style>

        .health-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 16px;
            margin-top: 15px;
            margin-bottom: 20px;
        }}

        .health-card {{
            display: flex;
            align-items: center;
            gap: 14px;

            padding: 16px 18px;

            border: 1px solid rgba(128, 128, 128, 0.35);
            border-radius: 12px;

            background: transparent;

            min-height: 72px;

            box-sizing: border-box;
        }}

        .health-icon {{
            display: flex;
            align-items: center;
            justify-content: center;

            width: 28px;
            height: 28px;

            border-radius: 50%;

            background: rgba(34, 197, 94, 0.15);

            color: #22c55e;

            font-size: 17px;
            font-weight: 700;

            flex-shrink: 0;
        }}

        .health-title {{
            font-size: 16px;
            font-weight: 600;
        }}

        .health-description {{
            margin-top: 3px;
            font-size: 13px;
            opacity: 0.65;
        }}

        .warning-card {{
            border-color: rgba(245, 158, 11, 0.45);
        }}

        .warning-icon {{
            background: rgba(245, 158, 11, 0.15);
            color: #f59e0b;
        }}

        @media (max-width: 900px) {{
            .health-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        </style>

        <div class="health-grid">
            {health_cards}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # DATA CLEANING
    # =====================================================

    st.markdown("---")

    st.header("🧹 Data Cleaning Summary")

    if cleaning_report:

        cleaning_cards = ""

        for item in cleaning_report:

            cleaning_cards += f"""
            <div class="cleaning-card">
                <span class="cleaning-icon">✓</span>
                <span>{item}</span>
            </div>
            """

        st.markdown(
            f"""
            <style>

            .cleaning-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 14px;

                margin-top: 15px;
                margin-bottom: 20px;
            }}

            .cleaning-card {{
                display: flex;
                align-items: center;

                gap: 12px;

                padding: 15px 18px;

                border: 1px solid rgba(128, 128, 128, 0.35);
                border-radius: 10px;

                background: transparent;

                font-size: 15px;

                min-height: 52px;

                box-sizing: border-box;
            }}

            .cleaning-icon {{
                display: flex;
                align-items: center;
                justify-content: center;

                width: 24px;
                height: 24px;

                border-radius: 50%;

                background: rgba(34, 197, 94, 0.15);

                color: #22c55e;

                font-weight: 700;

                flex-shrink: 0;
            }}

            @media (max-width: 700px) {{
                .cleaning-grid {{
                    grid-template-columns: 1fr;
                }}
            }}

            </style>

            <div class="cleaning-grid">
                {cleaning_cards}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No data cleaning actions were required."
        )

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
            st.write(
                dataset_info["numeric"]
            )
        else:
            st.info(
                "No numeric columns detected."
            )

    with st.expander("📝 Categorical Columns"):

        if dataset_info["categorical"]:
            st.write(
                dataset_info["categorical"]
            )
        else:
            st.info(
                "No categorical columns detected."
            )

    with st.expander("📅 Date Columns"):

        if dataset_info["datetime"]:
            st.write(
                dataset_info["datetime"]
            )
        else:
            st.info(
                "No date columns detected."
            )

    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    st.markdown("---")

    st.header("📑 Column Information")

    st.dataframe(
        get_column_types(df),
        width="stretch"
    )