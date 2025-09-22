import base64
import os
import secrets
import string
import uuid
from datetime import datetime
from io import StringIO

import pandas as pd
import streamlit as st
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# --- Configuration ---
CREDENTIALS_FILE = "credentials.enc"
OPERATIONS_FILE = "operations.enc"
CASHFLOW_FILE = "cashflow.enc"


# --- Authentication & Security ---

def generate_key(password: str) -> bytes:
    """Generates a reproducible, URL-safe key from a master password."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode())
    return base64.urlsafe_b64encode(digest.finalize())

def check_authentication():
    """Redirects to the home page if the user is not authenticated."""
    if not st.session_state.get("authenticated"):
        st.error("Please login first on the Home page.")
        st.stop()
    return st.session_state.get("encryption_key")


# --- Data Handling (Generalized) ---

def encrypt_data(data: bytes, key: bytes) -> bytes:
    """Encrypts data using the provided Fernet key."""
    return Fernet(key).encrypt(data)

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypts data using the provided Fernet key."""
    return Fernet(key).decrypt(encrypted_data)

def load_data(filename: str, key: bytes, columns: list) -> pd.DataFrame:
    """Loads and decrypts data. Returns an empty DataFrame if file doesn't exist or key is wrong."""
    if not os.path.exists(filename):
        return pd.DataFrame(columns=columns)

    with open(filename, "rb") as f:
        encrypted_data = f.read()

    if not encrypted_data:
        return pd.DataFrame(columns=columns)

    try:
        decrypted_data = decrypt_data(encrypted_data, key).decode()
        df = pd.read_json(StringIO(decrypted_data), orient="split")
        return df
    except Exception:
        st.error("Invalid master password or corrupted data file. Please logout and try again.")
        return None

def save_data(df: pd.DataFrame, filename: str, key: bytes):
    """Encrypts and saves the DataFrame to the specified local file."""
    data_json = df.to_json(orient="split").encode()
    encrypted_data = encrypt_data(data_json, key)
    with open(filename, "wb") as f:
        f.write(encrypted_data)


# --- Generation Functions ---

def generate_secure_password(length=16, upper=True, lower=True, digits=True, punctuation=True):
    """Generates a cryptographically strong password with customizable character sets."""
    alphabet = ""
    if upper: alphabet += string.ascii_uppercase
    if lower: alphabet += string.ascii_lowercase
    if digits: alphabet += string.digits
    if punctuation: alphabet += string.punctuation

    if not alphabet:
        return "Error: At least one character set must be selected."

    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_uid():
    """Generates a Version 4 UUID."""
    return str(uuid.uuid4())