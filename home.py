import streamlit as st
from utils import generate_key

st.set_page_config(
    page_title="Business & Security Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

def authenticate():
    """Handles the master password authentication."""
    st.header("🔒 Master Password Authentication")
    st.write("Please enter your master password to unlock the application and access your encrypted data.")

    with st.form("login_form"):
        master_password = st.text_input("Master Password", type="password")
        submitted = st.form_submit_button("Unlock")

        if submitted:
            if not master_password:
                st.error("Master password cannot be empty.")
            else:
                try:
                    st.session_state["encryption_key"] = generate_key(master_password)
                    st.session_state["authenticated"] = True
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred during key generation: {e}")

def main_app():
    """Main application layout after authentication."""
    st.sidebar.success("Application Unlocked")
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.title("Welcome to Your All-in-One Dashboard")
    st.write("Select a module from the sidebar to begin.")
    st.info(
        "Your data is encrypted and saved locally. Remember your master password, "
        "as it is the only way to access your stored credentials.", icon="ℹ️"
    )

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    main_app()
else:
    authenticate()