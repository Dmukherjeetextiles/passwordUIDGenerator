import streamlit as st
import pandas as pd
from utils import load_data, save_data

st.set_page_config(layout="wide")

# Authentication check
if not st.session_state.get("authenticated"):
    st.error("Please login first on the main page.")
    st.stop()

st.title("🗄️ Credential Vault")

# Key check
key = st.session_state.get("encryption_key")
if key is None:
    st.warning("Session key not found. Please log out and log in again.")
    st.stop()

# Load data
df = load_data(key)

if df is None:
    st.stop()

if df.empty:
    st.info("Your vault is empty. Generate and save a credential to see it here.")
else:
    st.write("Your stored credentials.")
    
    # --- Display Logic (Read-Only) ---
    # Create a copy for display and mask the passwords
    df_display = df.copy()
    df_display["Credential"] = "••••••••"
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---") # Visual separator

    # --- Delete Logic ---
    with st.expander("🗑️ Delete a Credential"):
        if not df.empty:
            # Create a list of usernames for the dropdown
            usernames_list = df["Username"].tolist()
            username_to_delete = st.selectbox(
                "Select a credential to delete",
                options=usernames_list,
                index=None, # No default selection
                placeholder="Choose an option"
            )

            if username_to_delete:
                if st.button(f"Delete Credential for '{username_to_delete}'", type="primary"):
                    # Keep all rows where the username is NOT the one selected for deletion
                    df_updated = df[df["Username"] != username_to_delete]
                    
                    # Save the updated dataframe
                    save_data(df_updated, key)
                    st.success(f"Successfully deleted credential for '{username_to_delete}'.")
                    st.rerun() # Refresh the page to show the updated vault
        else:
            st.write("Your vault is empty.")


# Sidebar refresh button
st.sidebar.markdown("---")
if st.sidebar.button("Refresh Vault"):
    st.rerun()