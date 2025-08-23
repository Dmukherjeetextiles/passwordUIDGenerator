import streamlit as st
from utils import generate_uid, display_generated_item

st.set_page_config(layout="wide")

if not st.session_state.get("authenticated"):
    st.error("Please login first on the main page.")
    st.stop()

st.title("🆔 Unique ID (UUID) Generator")

if st.button("Generate UID", type="primary"):
    uid = generate_uid()
    st.session_state["generated_item_uid"] = uid

if "generated_item_uid" in st.session_state and st.session_state["generated_item_uid"]:
    st.subheader("Generated UID")
    display_generated_item(st.session_state["generated_item_uid"], "UID")