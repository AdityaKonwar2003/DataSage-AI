import re
import streamlit as st

from report.pdf_generator import generate_pdf


# =====================================================
# FORMAT AI STORY
# =====================================================

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

            lines.append(
                f"\n### {icons[line]} {line}\n"
            )

        else:

            lines.append(
                f"• {line}"
            )

    return "\n".join(lines)


# =====================================================
# SHOW REPORT
# =====================================================

def show_report():

    st.header("📄 Professional Report Dashboard")

    st.caption(
        "Generate a professional business report with AI-powered "
        "insights and forecasting."
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
    # LOAD GENERATED CHARTS
    # =====================================================

    report_items = st.session_state.get(
        "report_items",
        []
    )

    chart_paths = [
        item["path"]
        for item in report_items
        if "path" in item
    ]


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
            width="stretch"
        )

        st.button(
            "📊 Dataset Summary",
            width="stretch"
        )

        st.button(
            "📈 Forecast",
            width="stretch"
        )

        st.button(
            "📊 Visual Analytics",
            width="stretch"
        )

        st.button(
            "📄 Download PDF",
            width="stretch"
        )


    # =====================================================
    # RIGHT CONTENT
    # =====================================================

    with content:


        # =================================================
        # DASHBOARD OVERVIEW
        # =================================================

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


        # =================================================
        # AI EXECUTIVE SUMMARY
        # =================================================

        st.subheader("✨ AI Executive Summary")

        st.info(
            "Automatically generated business insights from your "
            "uploaded dataset."
        )

        st.markdown(
            format_ai_story(ai_story)
        )


        st.markdown("---")


        # =================================================
        # DATASET SUMMARY
        # =================================================

        st.subheader("📊 Dataset Summary")

        st.code(summary)


        st.markdown("---")


        # =================================================
        # VISUAL ANALYTICS
        # =================================================

        st.subheader("📈 Visual Analytics")

        if report_items:

            st.success(
                f"✅ {len(report_items)} visualization(s) "
                "included in the report."
            )

            for item in report_items:

                chart_path = item.get("path")
                chart_title = item.get(
                    "title",
                    "Visualization"
                )
                chart_insight = item.get(
                    "insight",
                    ""
                )

                st.markdown(
                    f"### 📊 {chart_title}"
                )

                if chart_path:

                    try:

                        st.image(
                            chart_path,
                            width="stretch"
                        )

                    except Exception:

                        pass

                if chart_insight:

                    st.success(
                        f"💡 {chart_insight}"
                    )

        else:

            st.info(
                "No visualization charts are currently available."
            )


        st.markdown("---")


        # =================================================
        # FORECAST
        # =================================================

        st.subheader("🔮 Forecast Analysis")

        st.info(
            forecast_text
        )


        st.markdown("---")


        # =================================================
        # PDF
        # =================================================

        st.subheader("📄 Professional Report")

        if st.button(
            "⬇ Generate & Download PDF",
            width="stretch"
        ):

            with st.spinner(
                "Generating professional report..."
            ):

                # Get latest report items
                report_items = st.session_state.get(
                    "report_items",
                    []
                )

                pdf = generate_pdf(
                    summary,
                    ai_story,
                    forecast_text,
                    report_items
                )


            with open(pdf, "rb") as file:

                st.download_button(
                    label="⬇ Download Report",
                    data=file,
                    file_name=pdf,
                    mime="application/pdf",
                    width="stretch"
                )


            st.success(
                "✅ Report generated successfully "
                "with analytics charts and insights!"
            )