import streamlit as st
import pandas as pd
from datetime import datetime
from utils import check_authentication, generate_uid, load_data, save_data, CREDENTIALS_FILE

st.set_page_config(page_title="UID Generator", page_icon="🆔", layout="wide")
key = check_authentication()

st.title("🆔 Unique ID (UUID) Generator")

if st.button("Generate UID", type="primary"):
    st.session_state["generated_item_uid"] = generate_uid()

if "generated_item_uid" in st.session_state and st.session_state["generated_item_uid"]:
    st.subheader("Generated UID")
    st.code(st.session_state["generated_item_uid"], language="text")

    with st.form("save_uid_form"):
        username = st.text_input("Username / Service Name (Required for saving)")
        save_button = st.form_submit_button("Save UID to Vault")

        if save_button and username:
            df_creds = load_data(CREDENTIALS_FILE, key, ["Username", "Credential", "Type", "Timestamp"])
            new_entry = {
                "Username": username,
                "Credential": st.session_state["generated_item_uid"],
                "Type": "UID",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            if username in df_creds["Username"].values:
                df_creds.loc[df_creds["Username"] == username] = list(new_entry.values())
                st.success(f"Updated UID for '{username}' in the vault.")
            else:
                df_creds = pd.concat([df_creds, pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"Saved new UID for '{username}' to the vault.")
            save_data(df_creds, CREDENTIALS_FILE, key)
        elif save_button and not username:
            st.warning("Username is required to save.")