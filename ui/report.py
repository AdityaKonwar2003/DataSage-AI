import re
import streamlit as st

from report.pdf_generator import generate_pdf


def format_ai_story(text):
    """
    Convert AI markdown into clean bullet points.
    """

    icons = {
        "Executive Summary": "📋",
        "Key Findings": "📊",
        "Business Recommendations": "💡",
        "Risks": "⚠️",
        "Next Steps": "🚀",
    }

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = re.sub(r"^#+\s*", "", line)
        line = line.replace("**", "")

        if line in icons:
            lines.append(f"\n### {icons[line]} {line}\n")
        else:
            lines.append(f"• {line}")

    return "\n".join(lines)


def show_report():

    st.header("📄 Professional Report Dashboard")

    st.caption(
        "Generate a professional business report with AI-powered insights and forecasting."
    )

    st.markdown("---")

    # =====================================================
    # LOAD SESSION DATA
    # =====================================================

    summary = st.session_state.get(
        "dataset_summary",
        "Dataset summary not available."
    )

    ai_story = st.session_state.get(
        "ai_story",
        "Generate AI Insights first."
    )

    forecast_text = st.session_state.get(
        "forecast_explanation",
        "Generate Forecast first."
    )

    # =====================================================
    # PAGE LAYOUT
    # =====================================================

    menu, content = st.columns([1, 4])

    # =====================================================
    # LEFT MENU
    # =====================================================

    with menu:

        st.markdown("## 📑 Report")

        st.markdown("---")

        st.button(
            "✨ Executive Summary",
            use_container_width=True
        )

        st.button(
            "📊 Dataset Summary",
            use_container_width=True
        )

        st.button(
            "📈 Forecast",
            use_container_width=True
        )

        st.button(
            "📄 Download PDF",
            use_container_width=True
        )

    # =====================================================
    # RIGHT CONTENT
    # =====================================================

    with content:
        st.subheader("📊 Dashboard Overview")
        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.metric(
        "Rows",
        f"{st.session_state.get('row_count', '--')}"
    )

        with k2:
            st.metric(
        "Columns",
        f"{st.session_state.get('column_count', '--')}"
    )

        with k3:
            st.metric(
        "Missing Values",
        f"{st.session_state.get('missing_count', '--')}"
    )

        with k4:
            st.metric(
        "Duplicates",
        f"{st.session_state.get('duplicate_count', '--')}"
    )

        st.markdown("---")

        st.subheader("✨ AI Executive Summary")

        st.info(
            "Automatically generated business insights from your uploaded dataset."
        )

        st.markdown(
            f"""
<div style="
background:#111827;
padding:20px;
border-radius:12px;
border:1px solid #374151;
line-height:1.8;
font-size:16px;
">

{format_ai_story(ai_story)}

</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ---------------- DATASET SUMMARY ---------------- #

        st.subheader("📊 Dataset Summary")

        st.code(summary)

        st.markdown("---")

        # ---------------- FORECAST ---------------- #

        st.subheader("🔮 Forecast Analysis")

        st.info(forecast_text)

        st.markdown("---")

        # ---------------- PDF ---------------- #

        st.subheader("📄 Professional Report")

        if st.button(
            "⬇ Generate & Download PDF",
            use_container_width=True
        ):

            with st.spinner(
                "Generating professional report..."
            ):

                chart_paths = st.session_state.get("report_charts", [])
                pdf = generate_pdf(
                    summary,
                    ai_story,
                    forecast_text,
                    chart_paths
                )

            with open(pdf, "rb") as file:

                st.download_button(
                    label="⬇ Download Report",
                    data=file,
                    file_name=pdf,
                    mime="application/pdf",
                    use_container_width=True
                )

            st.success(
                "✅ Report generated successfully!"
            )