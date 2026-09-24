import streamlit as st

from llm.storyteller import generate_story, ask_dataset
from analysis.query_engine import analyze_question


def show_ai(df, dataset_info, semantic_info):

    st.header("🤖 AI Data Storyteller")

    # =====================================================
    # BUILD DATASET SUMMARY
    # =====================================================

    summary = st.session_state.get(
        "dataset_summary",
        ""
    )

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

        st.markdown(
            st.session_state["ai_story"]
        )

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

    st.caption(
        "Ask questions about your dataset. "
        "Your conversation will remain visible."
    )

    # =====================================================
    # INITIALIZE CHAT HISTORY
    # =====================================================

    if "chat_history" not in st.session_state:

        st.session_state["chat_history"] = []

    # =====================================================
    # DISPLAY PREVIOUS MESSAGES
    # =====================================================

    for message in st.session_state["chat_history"]:

        with st.chat_message(message["role"]):

            st.markdown(
                message["content"]
            )

    # =====================================================
    # CHAT INPUT
    # =====================================================

    question = st.chat_input(
        "Ask something about your dataset..."
    )

    # =====================================================
    # PROCESS QUESTION
    # =====================================================

    if question:

        # ---------------------------------------------
        # DISPLAY USER QUESTION
        # ---------------------------------------------

        with st.chat_message("user"):

            st.markdown(question)

        # Save user question

        st.session_state["chat_history"].append(
            {
                "role": "user",
                "content": question
            }
        )

        # ---------------------------------------------
        # GENERATE ANSWER
        # ---------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing your dataset..."
            ):

                data_context = analyze_question(
                    df,
                    question
                )

                answer = ask_dataset(
                    summary,
                    question,
                    data_context
                )

            st.markdown(answer)

        # Save AI answer

        st.session_state["chat_history"].append(
            {
                "role": "assistant",
                "content": answer
            }
        )