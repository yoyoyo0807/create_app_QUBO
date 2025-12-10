import streamlit as st

def show_data_missing(msg: str, tried_paths=None):
    st.error(msg)
    if tried_paths:
        with st.expander("試したパス"):
            for p in tried_paths:
                st.code(p)
    st.stop()

def section(title: str, emoji: str = ""):
    st.markdown("")
    st.markdown(f"## {emoji} {title}" if emoji else f"## {title}")
