# Professional Streamlit Credentials Manager

A secure, multi-page Streamlit application for generating, managing, and locally storing encrypted passwords and UIDs.

This application provides a professional-grade interface and robust security features, including session-based authentication and strong local encryption.


## ✨ Key Features

-   **Secure Authentication**: The application is locked behind a master password. All data is inaccessible without it.
-   **Multi-Page Interface**: A clean, organized user experience with separate pages for different tasks.
-   **Advanced Password Generation**: Customize password length and included character sets (uppercase, lowercase, numbers, symbols).
-   **Encrypted Local Storage**: All credentials are saved to a local `credentials.enc` file, encrypted using the industry-standard Fernet (AES-128-CBC) symmetric encryption scheme.
-   **Full Credential Management (CRUD)**:
    -   **Create**: Generate and save new credentials.
    -   **Read**: View all stored credentials in a secure vault.
    -   **Update**: Overwrite an existing entry by saving a new credential with the same username.
    -   **Delete**: Remove credentials directly from the vault interface.
-   **Modular and Maintainable Code**: Backend logic is separated from the UI for clarity and scalability.

## 🚀 How to Run

1.  **Clone the Repository**:
    Ensure you have the following file structure:
    ```bash
    git clone https://github.com/Dmukherjeetextiles/passwordUIDGenerator.git
    ```

2.  **Install Dependencies**:
    Navigate to the project directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    streamlit run main_app.py
    ```

4.  **Access in Browser**:
    Open the local URL provided by Streamlit in your web browser.

## 🔐 Security Model

-   **Master Password**: The application uses your master password to derive a 256-bit encryption key via SHA-256 hashing. **This master password is never stored**. It is only held in your browser's memory for the duration of the session.
-   **Encryption Key**: The derived key is used to encrypt and decrypt the `credentials.enc` file.
-   **Local Storage**: Your encrypted data never leaves your computer.
-   **Session Management**: The application state is cleared upon logout or closing the browser tab, ensuring no residual access.

**⚠️ Important**: If you forget your master password, there is **no way** to recover the data in your `credentials.enc` file. Store your master password securely.

## 📦 Dependencies
-   **Streamlit**: For the web application framework.
-   **Pandas**: For structured data management.
-   **Cryptography**: For robust, high-level cryptographic functions.
