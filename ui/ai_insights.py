import streamlit as st

from analysis.statistics import build_ai_summary
from llm.storyteller import generate_story, ask_dataset


def show_ai(df, dataset_info, semantic_info):

    st.header("🤖 AI Data Storyteller")

    # =====================================================
    # BUILD DATASET SUMMARY
    # =====================================================

    summary = build_ai_summary(
        df,
        dataset_info,
        semantic_info
    )

    # Save summary for Report Page
    st.session_state["dataset_summary"] = summary

    # =====================================================
    # AI REPORT
    # =====================================================

    if st.button("✨ Generate AI Insights"):

        with st.spinner("Analyzing your dataset..."):

            story = generate_story(summary)

        if story:

            st.session_state["ai_story"] = story

            st.success("✅ Analysis Complete")

        else:

            st.error("Failed to generate AI insights.")

    # =====================================================
    # ALWAYS SHOW SAVED AI STORY
    # =====================================================

    if st.session_state.get("ai_story"):

        st.markdown(st.session_state["ai_story"])

        st.download_button(
            label="📥 Download AI Summary",
            data=st.session_state["ai_story"],
            file_name="AI_Summary.txt",
            mime="text/plain"
        )

    # =====================================================
    # DATASET CHAT
    # =====================================================

    st.markdown("---")

    st.header("💬 Ask DataSage AI")

    question = st.text_input(
        "Ask a question about your dataset"
    )

    if st.button("🚀 Ask AI"):

        if question.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Thinking..."):

                answer = ask_dataset(
                    summary,
                    question
                )

            st.success(answer)