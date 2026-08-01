import streamlit as st

from report.pdf_generator import generate_pdf


def show_report():

    st.header("📄 Professional AI Report")

    st.caption(
        "Generate a professional business report containing AI insights, "
        "forecast results and dataset analytics."
    )

    st.markdown("---")

    # =====================================================
    # REPORT CONTENT
    # =====================================================

    st.subheader("📋 Report Contents")

    col1, col2 = st.columns(2)

    with col1:

        st.success("✅ Dataset Summary")

        st.success("✅ Data Cleaning Summary")

        st.success("✅ Dataset Detection")

        st.success("✅ AI Executive Summary")

    with col2:

        st.success("✅ Forecast Results")

        st.success("✅ AI Forecast Explanation")

        st.success("✅ Business Recommendations")

        st.success("✅ Professional Formatting")

    st.markdown("---")

    st.info(
        "The report is automatically generated using the latest "
        "analysis and AI-generated insights."
    )

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

    if st.button("📄 Generate PDF Report"):

        with st.spinner("Generating professional report..."):

            pdf = generate_pdf(
                summary,
                ai_story,
                forecast_text
            )

        with open(pdf, "rb") as file:

            st.download_button(
                label="⬇ Download PDF Report",
                data=file,
                file_name=pdf,
                mime="application/pdf"
            )

        st.success(
            "✅ Report generated successfully!"
        )