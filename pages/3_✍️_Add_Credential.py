import streamlit as st
import pandas as pd
from datetime import datetime
from utils import check_authentication, load_data, save_data, CREDENTIALS_FILE

st.set_page_config(page_title="Add Credential", page_icon="✍️", layout="wide")
key = check_authentication()

st.title("✍️ Add a Credential Manually")
st.write("Use this form to save an existing username and password/key to your vault.")

CREDENTIALS_COLUMNS = ["Username", "Credential", "Type", "Timestamp"]
df_creds = load_data(CREDENTIALS_FILE, key, CREDENTIALS_COLUMNS)

with st.form("add_credential_form"):
    username = st.text_input("Username / Service Name")
    credential = st.text_input("Password / Credential", type="password")
    submitted = st.form_submit_button("Save to Vault")

    if submitted:
        if not username or not credential:
            st.warning("Both Username and Credential fields are required.")
        else:
            new_entry = {
                "Username": username,
                "Credential": credential,
                "Type": "Password (Manual)",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if username in df_creds["Username"].values:
                # Update existing entry
                df_creds.loc[df_creds["Username"] == username, ["Credential", "Type", "Timestamp"]] = [new_entry["Credential"], new_entry["Type"], new_entry["Timestamp"]]
                st.success(f"Updated credential for '{username}' in the vault.")
            else:
                # Add new entry
                df_creds = pd.concat([df_creds, pd.DataFrame([new_entry])], ignore_index=True)
                st.success(f"Saved new credential for '{username}' to the vault.")
            
            save_data(df_creds, CREDENTIALS_FILE, key)