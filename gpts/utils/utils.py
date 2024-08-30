import streamlit as st

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def set_page_config(title):
    return {
        "page_title": {title},
        "page_icon": "🤖",
        "layout": "wide"
    }