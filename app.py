
from ui.theme import load_css
import streamlit as st

from utils.helpers import load_data

from analysis.cleaner import clean_data
from analysis.detector import detect_dataset
from analysis.semantic_detector import detect_semantics

from analysis.statistics import (
    get_dataset_summary,
    get_column_types,
    get_descriptive_statistics,
    build_ai_summary
)

from ui.overview import show_overview
from ui.analysis import show_analysis
from ui.ai_insights import show_ai
from ui.forecast import show_forecast
from ui.report import show_report


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="DataSage AI",
    page_icon="📊",
    layout="wide"
)
load_css()

# ---------------- SESSION STATE ---------------- #


if "dataset_summary" not in st.session_state:
    st.session_state["dataset_summary"] = ""

if "ai_story" not in st.session_state:
    st.session_state["ai_story"] = ""

if "forecast_explanation" not in st.session_state:
    st.session_state["forecast_explanation"] = ""

if "dataset_summary" not in st.session_state:
    st.session_state["dataset_summary"] = ""

# ---------------- SIDEBAR ---------------- #

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("📊 DataSage AI")
    st.image(
    "https://raw.githubusercontent.com/streamlit/brand/master/logos/mark/streamlit-mark-color.png",
    width=80
)
    st.caption("AI-Powered Business Intelligence Platform")

    st.markdown("---")

    st.subheader("📌 Version")
    st.success("v1.0 Beta")

    st.markdown("---")

    st.subheader("👨‍💻 Developer")
    st.write("Aditya Konwar")

    st.markdown("---")

    st.subheader("🛠 Tech Stack")

    st.markdown("""
- Python
- Streamlit
- Pandas
- Plotly
- OpenAI GPT
- Scikit-Learn
""")

    st.markdown("---")

    st.subheader("📈 Modules")

    st.markdown("""
✅ Smart Analytics

✅ AI Insights

✅ Forecasting

✅ PDF Reports
""")

    st.markdown("---")

    st.caption("Built with ❤️ using Streamlit")

# ---------------- HEADER ---------------- #

st.markdown(
    """
# 📊 DataSage AI

### AI-Powered Business Intelligence Platform

Transform raw datasets into **interactive dashboards,
AI-generated business insights, machine learning forecasts,
and executive reports**.

---
"""
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("📊 Smart Analytics")

with col2:
    st.info("🤖 AI Insights")

with col3:
    st.info("📈 Forecasting")

with col4:
    st.info("📄 Reports")

st.markdown("---")
# ---------------- FILE UPLOAD ---------------- #

st.header("📂 Upload Your Dataset")
st.caption(
    "Supported formats: CSV, XLSX and XLS files"
)
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

# ---------------- MAIN APP ---------------- #

if uploaded_file is not None:

    # Load Dataset
    df = load_data(uploaded_file)

    # Clean Dataset
    df, cleaning_report = clean_data(df)

    # Detect Dataset
    dataset_info = detect_dataset(df)

    # Detect Semantics
    semantic_info = detect_semantics(df)

    st.success("✅ Dataset uploaded successfully. "
    "Explore the tabs above to analyze your data."
)

    # Build summary (used later by Report)
    summary = build_ai_summary(
        df,
        dataset_info,
        semantic_info
    )
    st.session_state["dataset_summary"] = summary

    # Temporary placeholders
    ai_story = """
Generate AI Insights first to include them in the report.
"""

    forecast_text = """
Generate Forecast first to include forecast results.
"""

    # ---------------- TABS ---------------- #

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Overview",
            "📈 Analysis",
            "🤖 AI Insights",
            "🔮 Forecast",
            "📄 Report"
        ]
    )

    # ---------------- OVERVIEW ---------------- #

    with tab1:

        show_overview(
            df,
            cleaning_report,
            dataset_info
        )

    # ---------------- ANALYSIS ---------------- #

    with tab2:

        show_analysis(
            df,
            dataset_info,
            semantic_info
        )

    # ---------------- AI ---------------- #

    with tab3:

        show_ai(
            df,
            dataset_info,
            semantic_info
        )

    # ---------------- FORECAST ---------------- #

    with tab4:

        show_forecast(
            df,
            semantic_info
        )

    # ---------------- REPORT ---------------- #

    with tab5:

        show_report()