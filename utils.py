import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import os
import secrets
import string
import uuid
from datetime import datetime
from io import StringIO # Import StringIO

# --- Configuration ---
ENCRYPTED_FILE = "credentials.enc"

# --- Cryptography Functions ---

def generate_key(password: str) -> bytes:
    """Generates a reproducible, URL-safe key from a master password."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    return base64.urlsafe_b64encode(digest.finalize())

def encrypt_data(data: bytes, key: bytes) -> bytes:
    """Encrypts data using the provided Fernet key."""
    return Fernet(key).encrypt(data)

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypts data using the provided Fernet key."""
    return Fernet(key).decrypt(encrypted_data)

# --- Data Handling Functions ---

def load_data(key: bytes) -> pd.DataFrame:
    """Loads and decrypts data. Returns an empty DataFrame if file doesn't exist or key is wrong."""
    if not os.path.exists(ENCRYPTED_FILE):
        return pd.DataFrame(columns=["Username", "Credential", "Type", "Timestamp"])
    
    with open(ENCRYPTED_FILE, "rb") as f:
        encrypted_data = f.read()
    
    if not encrypted_data:
        return pd.DataFrame(columns=["Username", "Credential", "Type", "Timestamp"])
        
    try:
        decrypted_data = decrypt_data(encrypted_data, key).decode()
        # FIX: Use StringIO to wrap the JSON string for pandas
        df = pd.read_json(StringIO(decrypted_data), orient="split")
        return df
    except Exception:
        st.error("Invalid master password or corrupted data file. Please restart the application and try again.")
        return None

def save_data(df: pd.DataFrame, key: bytes):
    """Encrypts and saves the DataFrame to the local file."""
    data_json = df.to_json(orient="split").encode()
    encrypted_data = encrypt_data(data_json, key)
    with open(ENCRYPTED_FILE, "wb") as f:
        f.write(encrypted_data)

# --- Generation Functions ---

def generate_secure_password(length=16, upper=True, lower=True, digits=True, punctuation=True):
    """Generates a cryptographically strong password with customizable character sets."""
    alphabet = ""
    if upper:
        alphabet += string.ascii_uppercase
    if lower:
        alphabet += string.ascii_lowercase
    if digits:
        alphabet += string.digits
    if punctuation:
        alphabet += string.punctuation
    
    if not alphabet:
        return "Error: At least one character set must be selected."
        
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def generate_uid():
    """Generates a Version 4 UUID."""
    return str(uuid.uuid4())

# --- UI Helper ---
def display_generated_item(item: str, item_type: str):
    """Displays the generated item and provides save functionality."""
    st.code(item, language="text")
    
    st.write("") # Spacer
    with st.form("save_form"):
        username = st.text_input("Username / Service Name (Required for saving)")
        save_button = st.form_submit_button(f"Save {item_type}")

        if save_button and username:
            key = st.session_state.get("encryption_key")
            if key:
                df = load_data(key)
                if df is not None:
                    # Prepare new entry
                    new_entry = {
                        "Username": username,
                        "Credential": item,
                        "Type": item_type,
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Check if username exists to update, otherwise append
                    if username in df["Username"].values:
                        df.loc[df["Username"] == username, ["Credential", "Type", "Timestamp"]] = [new_entry["Credential"], new_entry["Type"], new_entry["Timestamp"]]
                        st.success(f"Updated credential for '{username}' in the vault.")
                    else:
                        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
                        st.success(f"Saved new credential for '{username}' to the vault.")
                    
                    save_data(df, key)
            else:
                st.error("Authentication session expired. Please logout and login again.")
        elif save_button and not username:
            st.warning("Username/Service Name is required to save.")