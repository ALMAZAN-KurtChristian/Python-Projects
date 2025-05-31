# Password Manager Desktop Application

A secure desktop application for managing your passwords, built with Python and PyQt6.

## Features

- User registration and login system
- Secure password storage with encryption
- Add, edit, and delete password entries
- Store additional information like website URLs and notes
- Modern and user-friendly interface
- Local database storage

## Security Features

- Passwords are encrypted using Fernet (symmetric encryption)
- Master passwords are hashed using bcrypt
- All sensitive data is encrypted at rest
- No data is transmitted over the network (local storage only)

## Requirements

- Python 3.8 or higher
- PyQt6
- bcrypt
- cryptography
- SQLite3

## Installation

1. Clone this repository or download the source code
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Register a new account:
   - Click the "Register" button
   - Enter your desired username and password
   - Click "Register" to create your account

3. Login:
   - Enter your username and password
   - Click "Login" to access your password manager

4. Managing Passwords:
   - Click "Add New Password" to store a new password
   - Fill in the required information (Title, Username, Password)
   - Optionally add a website URL and notes
   - Click "Save" to store the password
   - Use the "Edit" and "Delete" buttons to manage existing passwords

## Security Notes

- Keep your master password secure and never share it
- The application stores all data locally in a SQLite database
- Your master password is used to derive the encryption key
- All stored passwords are encrypted using this key
- The database file (`password_manager.db`) should be kept secure

## Development

The application is structured into two main files:
- `main.py`: Contains the login window and application entry point
- `password_manager.py`: Contains the main window and password management functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details. 