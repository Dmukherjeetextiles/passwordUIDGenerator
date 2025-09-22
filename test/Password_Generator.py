import streamlit as st
from utils import generate_secure_password, display_generated_item

st.set_page_config(layout="wide")

if not st.session_state.get("authenticated"):
    st.error("Please login first on the main page.")
    st.stop()

st.title("🔑 Secure Password Generator")

with st.expander("Customize Password Options", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        length = st.slider("Password Length", min_value=8, max_value=64, value=16)
    with col2:
        st.write("") # Alignment
        st.write("") # Alignment
        upper = st.checkbox("Include Uppercase (A-Z)", value=True)
        lower = st.checkbox("Include Lowercase (a-z)", value=True)
        digits = st.checkbox("Include Numbers (0-9)", value=True)
        punctuation = st.checkbox("Include Symbols (!@#$)", value=True)

if st.button("Generate Password", type="primary"):
    password = generate_secure_password(length, upper, lower, digits, punctuation)
    st.session_state["generated_item"] = password

if "generated_item" in st.session_state and st.session_state["generated_item"]:
    st.subheader("Generated Password")
    display_generated_item(st.session_state["generated_item"], "Password")