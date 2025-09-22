# 📈 All-in-One Business & Security Dashboard

A professional, secure, and multi-page Streamlit application that serves as a central hub for business intelligence and personal security. This tool provides modules for tracking cash flow, logging operational updates, and managing encrypted credentials, all protected by a master password.

## ✨ Key Features

-   **Secure Authentication**: The entire application is locked behind a master password. All data is inaccessible without it and is stored encrypted on your local machine.
-   **Multi-Page Interface**: A clean, organized user experience with separate pages for different business and security tasks.
-   **Data Encryption**: All data you enter (financial, operational, credentials) is saved to local `.enc` files, encrypted using the industry-standard Fernet (AES-128-CBC) symmetric encryption scheme.

### Included Modules

1.  **💸 Cash Flow Tracker**:
    -   Log income and expenses with dates and descriptions.
    -   An interactive dashboard visualizes daily and monthly cash flow patterns.

2.  **📈 Business Operations Tracker**:
    -   Log real-time updates for various business operations with categories and priority levels.
    -   An interactive table allows for direct editing of status and priority.
    -   Dynamic charts display key metrics and progress.

3.  **🔐 Credentials Management**:
    -   **Add Credentials**: Manually add and save sensitive credentials like IDs and passwords.
    -   **Password Generator**: Create cryptographically strong, customizable passwords.
    -   **UID Generator**: Generate Version 4 UUIDs for unique identification.
    -   **Credential Vault**: A secure vault to view and delete all stored credentials. Passwords are masked for security.

## 🚀 How to Run

1.  **Prerequisites**
    -   Python 3.8+
    -   An environment manager like `venv` or `conda`.

2.  **Clone the repository**
    ```bash
    git clone https://github.com/Dmukherjeetextiles/passwordUIDGenerator.git
    cd passwordUIDGenerator
    ```

3.  **Set up a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

4.  **Install the requirements**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the app**
    ```bash
    streamlit run Home.py
    ```

## 🔐 Security Model

-   **Master Password**: The application uses your master password to derive a 256-bit encryption key. **This password is never stored**.
-   **Encryption Key**: The derived key is used to encrypt and decrypt the local data files (`cashflow.enc`, `operations.enc`, `credentials.enc`).
-   **Local Storage**: Your encrypted data never leaves your computer.
-   **Session Management**: The application state is cleared upon logout or closing the browser tab.

**⚠️ Important**: If you forget your master password, there is **no way** to recover your encrypted data. Store your master password securely.

## 📄 License

This project is licensed under the MIT License.