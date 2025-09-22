import streamlit as st
from utils import generate_key

st.set_page_config(
    page_title="Credentials Manager",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

def authenticate():
    """Handles the master password authentication."""
    st.header("🔒 Master Password Authentication")
    st.write("Please enter your master password to unlock the application.")

    with st.form("login_form"):
        master_password = st.text_input("Master Password", type="password")
        submitted = st.form_submit_button("Unlock")

        if submitted:
            if not master_password:
                st.error("Master password cannot be empty.")
            else:
                try:
                    # Store derived key and auth status in session state
                    st.session_state["encryption_key"] = generate_key(master_password)
                    st.session_state["authenticated"] = True
                    st.rerun() # Rerun to reflect authenticated state
                except Exception as e:
                    st.error(f"An error occurred during key generation: {e}")

def main_app():
    """Main application layout after authentication."""
    st.sidebar.success("Application Unlocked")
    st.sidebar.title("Navigation")

    # Use st.page_link for modern navigation
    st.page_link("pages/Password_Generator.py", label="Password Generator", icon="🔑")
    st.page_link("pages/UID_Generator.py", label="UID Generator", icon="🆔")
    st.page_link("pages/Vault.py", label="Credential Vault", icon="🗄️")

    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.title("Welcome to Your Secure Credentials Manager")
    st.write("Select an option from the sidebar to begin.")
    st.info("Your data is encrypted and saved locally. Remember your master password, as it is the only way to access your stored credentials.", icon="ℹ️")


if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if st.session_state["authenticated"]:
    main_app()
else:
    authenticate()