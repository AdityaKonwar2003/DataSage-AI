
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

st.markdown("""
<div style="
padding:35px;
border-radius:18px;
background:linear-gradient(135deg,#2563eb,#172A45);
color:white;
">

<h1 style="margin-bottom:5px;">
📊 DataSage AI
</h1>

<h3 style="margin-top:0;">
AI-Powered Business Intelligence Platform
</h3>

<p style="font-size:18px;">
Transform raw datasets into interactive dashboards,
AI-generated business insights,
Machine Learning forecasts,
and professional executive reports.
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# NAVIGATION
# =====================================================

page = st.radio(
      "Navigation",
    [
        "📂 Upload",
        "📊 Analytics",
        "🤖 AI Insights",
        "🔮 Forecast",
        "📄 Report"
    ],
    horizontal=True,
    label_visibility="collapsed"

)

st.markdown("---")

# ---------------- MAIN APP ---------------- #

# =====================================================
# UPLOAD PAGE
# =====================================================

if page == "📂 Upload":

    st.header("📂 Upload Your Dataset")

    st.info(
"""
Supported formats

• CSV

• XLSX

• XLS
"""
)

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        df = load_data(uploaded_file)

        df, cleaning_report = clean_data(df)

        dataset_info = detect_dataset(df)

        semantic_info = detect_semantics(df)

        st.session_state["df"] = df
        st.session_state["cleaning_report"] = cleaning_report
        st.session_state["dataset_info"] = dataset_info
        st.session_state["semantic_info"] = semantic_info

        st.session_state["dataset_summary"] = build_ai_summary(
            df,
            dataset_info,
            semantic_info
        )

        st.session_state["row_count"] = df.shape[0]
        st.session_state["column_count"] = df.shape[1]
        st.session_state["missing_count"] = int(df.isna().sum().sum())
        st.session_state["duplicate_count"] = int(df.duplicated().sum())

        st.success("✅ Dataset uploaded successfully!")

        # =====================================================
# CHECK DATASET
# =====================================================

if "df" in st.session_state:

    df = st.session_state["df"]

    cleaning_report = st.session_state["cleaning_report"]

    dataset_info = st.session_state["dataset_info"]

    semantic_info = st.session_state["semantic_info"]

    if page == "📊 Analytics":

        show_overview(
            df,
            cleaning_report,
            dataset_info
        )

        st.markdown("---")

        show_analysis(
            df,
            dataset_info,
            semantic_info
        )

    elif page == "🤖 AI Insights":

        show_ai(
            df,
            dataset_info,
            semantic_info
        )

    elif page == "🔮 Forecast":

        show_forecast(
            df,
            semantic_info
        )

    elif page == "📄 Report":

        show_report()

else:

    if page != "📂 Upload":

        st.warning(
            "⚠ Please upload a dataset first."
        )