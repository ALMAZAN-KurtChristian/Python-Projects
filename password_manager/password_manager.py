from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QMessageBox,
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QDialog, QTextEdit, QFormLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sqlite3
from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AddPasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):  
        self.setWindowTitle('Add New Password')
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.title_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.website_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)

        layout.addRow('Title:', self.title_input)
        layout.addRow('Username:', self.username_input)
        layout.addRow('Password:', self.password_input)
        layout.addRow('Website:', self.website_input)
        layout.addRow('Notes:', self.notes_input)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addRow('', buttons_layout)

        self.setLayout(layout)

class CredentialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Add New Credential')
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.service_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)

        layout.addRow('Service:', self.service_input)
        layout.addRow('Username:', self.username_input)
        layout.addRow('Password:', self.password_input)
        layout.addRow('Notes:', self.notes_input)

        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancel')
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addRow('', buttons_layout)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
        self.load_passwords()
        self.setup_encryption()

    def setup_encryption(self):
        # Generate encryption key from master password
        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (self.username,))
        master_password = cursor.fetchone()[0]
        conn.close()

        # Derive key from master password
        salt = b'password_manager_salt'  # In production, use a unique salt per user
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        self.cipher_suite = Fernet(key)

    def init_ui(self):
        self.setWindowTitle(f'Password Manager - {self.username}')
        self.setMinimumSize(800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 5px;
                border: 1px solid #ccc;
                font-weight: bold;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel('My Passwords')
        title.setFont(QFont('Arial', 16, QFont.Weight.Bold))
        header_layout.addWidget(title)

        self.add_button = QPushButton('Add New Password')
        self.add_button.clicked.connect(self.add_password)
        header_layout.addWidget(self.add_button)

        self.add_credential_button = QPushButton('Add New Credential')
        self.add_credential_button.clicked.connect(self.add_credential)
        header_layout.addWidget(self.add_credential_button)

        layout.addLayout(header_layout)

        # Password table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Title', 'Username', 'Password', 'Website', 'Notes', 'Actions'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)

    def load_passwords(self):
        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, username, password, website, notes 
            FROM passwords 
            WHERE user_id = (SELECT id FROM users WHERE username = ?)
        ''', (self.username,))
        passwords = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(passwords))
        for row, password in enumerate(passwords):
            # Decrypt password
            try:
                decrypted_password = self.cipher_suite.decrypt(password[3].encode()).decode()
            except:
                decrypted_password = "***"

            # Add data to table
            self.table.setItem(row, 0, QTableWidgetItem(password[1]))  # Title
            self.table.setItem(row, 1, QTableWidgetItem(password[2]))  # Username
            self.table.setItem(row, 2, QTableWidgetItem(decrypted_password))  # Password
            self.table.setItem(row, 3, QTableWidgetItem(password[4] or ''))  # Website
            self.table.setItem(row, 4, QTableWidgetItem(password[5] or ''))  # Notes

            # Add action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)

            edit_button = QPushButton('Edit')
            edit_button.clicked.connect(lambda checked, r=row: self.edit_password(r))
            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(lambda checked, r=row: self.delete_password(r))
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
            """)

            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            self.table.setCellWidget(row, 5, actions_widget)

    def add_password(self):
        dialog = AddPasswordDialog(self)
        if dialog.exec():
            title = dialog.title_input.text()
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            website = dialog.website_input.text()
            notes = dialog.notes_input.toPlainText()

            if not title or not username or not password:
                QMessageBox.warning(self, 'Error', 'Please fill in all required fields')
                return

            # Encrypt password
            encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()

            conn = sqlite3.connect('password_manager.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (user_id, title, username, password, website, notes)
                VALUES ((SELECT id FROM users WHERE username = ?), ?, ?, ?, ?, ?)
            ''', (self.username, title, username, encrypted_password, website, notes))
            conn.commit()
            conn.close()

            self.load_passwords()

    def edit_password(self, row):
        title = self.table.item(row, 0).text()
        username = self.table.item(row, 1).text()
        password = self.table.item(row, 2).text()
        website = self.table.item(row, 3).text()
        notes = self.table.item(row, 4).text()

        dialog = AddPasswordDialog(self)
        dialog.title_input.setText(title)
        dialog.username_input.setText(username)
        dialog.password_input.setText(password)
        dialog.website_input.setText(website)
        dialog.notes_input.setText(notes)

        if dialog.exec():
            title = dialog.title_input.text()
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            website = dialog.website_input.text()
            notes = dialog.notes_input.toPlainText()

            if not title or not username or not password:
                QMessageBox.warning(self, 'Error', 'Please fill in all required fields')
                return

            encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()

            conn = sqlite3.connect('password_manager.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE passwords 
                SET title = ?, username = ?, password = ?, website = ?, notes = ?
                WHERE user_id = (SELECT id FROM users WHERE username = ?)
                AND title = ?
            ''', (title, username, encrypted_password, website, notes, self.username, title))
            conn.commit()
            conn.close()

            self.load_passwords()

    def delete_password(self, row):
        title = self.table.item(row, 0).text()
        reply = QMessageBox.question(self, 'Confirm Delete',
                                   f'Are you sure you want to delete the password for {title}?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('password_manager.db')
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM passwords 
                WHERE user_id = (SELECT id FROM users WHERE username = ?)
                AND title = ?
            ''', (self.username, title))
            conn.commit()
            conn.close()

            self.load_passwords()

    def add_credential(self):
        dialog = CredentialDialog(self)
        if dialog.exec():
            service = dialog.service_input.text()
            username = dialog.username_input.text()
            password = dialog.password_input.text()
            notes = dialog.notes_input.toPlainText()

            if not service or not username or not password:
                QMessageBox.warning(self, 'Error', 'Please fill in all required fields')
                return

            encrypted_password = self.cipher_suite.encrypt(password.encode()).decode()

            conn = sqlite3.connect('password_manager.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO credentials (user_id, service, username, password, notes)
                VALUES ((SELECT id FROM users WHERE username = ?), ?, ?, ?, ?)
            ''', (self.username, service, username, encrypted_password, notes))
            conn.commit()
            conn.close()

            self.load_passwords()
