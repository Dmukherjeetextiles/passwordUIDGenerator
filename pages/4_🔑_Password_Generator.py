import streamlit as st
from utils import check_authentication, generate_secure_password, load_data, save_data, CREDENTIALS_FILE
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Password Generator", page_icon="🔑", layout="wide")
key = check_authentication()

st.title("🔑 Secure Password Generator")

with st.expander("Customize Password Options", expanded=True):
    length = st.slider("Password Length", min_value=8, max_value=64, value=16)
    col1, col2 = st.columns(2)
    with col1:
        upper = st.checkbox("Include Uppercase (A-Z)", value=True)
        lower = st.checkbox("Include Lowercase (a-z)", value=True)
    with col2:
        digits = st.checkbox("Include Numbers (0-9)", value=True)
        punctuation = st.checkbox("Include Symbols (!@#$)", value=True)

if st.button("Generate Password", type="primary"):
    password = generate_secure_password(length, upper, lower, digits, punctuation)
    st.session_state["generated_item"] = password

if "generated_item" in st.session_state and st.session_state["generated_item"]:
    st.subheader("Generated Password")
    st.code(st.session_state["generated_item"], language="text")

    with st.form("save_form"):
        username = st.text_input("Username / Service Name (Required for saving)")
        save_button = st.form_submit_button("Save Password to Vault")

        if save_button and username:
            df_creds = load_data(CREDENTIALS_FILE, key, ["Username", "Credential", "Type", "Timestamp"])
            new_entry = {
                "Username": username,
                "Credential": st.session_state["generated_item"],
                "Type": "Password",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            if username in df_creds["Username"].values:
                df_creds.loc[df_creds["Username"] == username] = list(new_entry.values())
                st.success(f"Updated credential for '{username}' in the vault.")
            else:
                df_creds = pd.concat([df_creds, pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"Saved new credential for '{username}' to the vault.")
            save_data(df_creds, CREDENTIALS_FILE, key)
        elif save_button and not username:
            st.warning("Username is required to save.")