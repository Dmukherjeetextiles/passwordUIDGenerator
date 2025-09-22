import streamlit as st
from utils import check_authentication, load_data, save_data, CREDENTIALS_FILE

st.set_page_config(page_title="Credential Vault", page_icon="🗄️", layout="wide")
key = check_authentication()

st.title("🗄️ Credential Vault")

df_creds = load_data(CREDENTIALS_FILE, key, ["Username", "Credential", "Type", "Timestamp"])

if df_creds is None or df_creds.empty:
    st.info("Your vault is empty. Generate or add a credential to see it here.")
else:
    st.write("Your stored credentials. Passwords are masked for security.")
    
    # Display logic (masking credentials)
    df_display = df_creds.copy()
    df_display['Credential'] = df_display.apply(
        lambda row: "••••••••" if "Password" in row["Type"] else row["Credential"], axis=1
    )
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.divider()

    # Delete logic
    with st.expander("🗑️ Delete a Credential"):
        usernames_list = df_creds["Username"].tolist()
        username_to_delete = st.selectbox(
            "Select a credential to delete",
            options=usernames_list,
            index=None,
            placeholder="Choose an option"
        )
        if st.button(f"Delete Credential for '{username_to_delete}'", type="primary", disabled=not username_to_delete):
            df_updated = df_creds[df_creds["Username"] != username_to_delete]
            save_data(df_updated, CREDENTIALS_FILE, key)
            st.success(f"Successfully deleted credential for '{username_to_delete}'.")
            st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("Refresh Vault"):
    st.rerun()