import sys
import sqlite3
import bcrypt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QStackedWidget, QTableWidget, QTableWidgetItem, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect('password_manager.db')   
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                website TEXT,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        conn.close()

    def init_ui(self):
        self.setWindowTitle('Password Manager - Login')
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial;
            }
            QLineEdit {
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
            QLabel {
                font-size: 14px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title = QLabel('Password Manager')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont('Arial', 20, QFont.Weight.Bold))
        layout.addWidget(title)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)

        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.register)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
            self.main_window = MainWindow(username, result[0])
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please fill in all fields')
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = sqlite3.connect('password_manager.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password.decode('utf-8')))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Success', 'Registration successful!')
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Error', 'Username already exists')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Registration failed: {str(e)}')

class MainWindow(QMainWindow):
    def __init__(self, username, user_id):
        super().__init__()
        self.username = username
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Password Manager - {self.username}')
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add Password Button
        add_button = QPushButton('Add Password')
        add_button.clicked.connect(self.show_add_password_dialog)
        layout.addWidget(add_button)

        # Password Table
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(5)
        self.password_table.setHorizontalHeaderLabels(['Title', 'Username', 'Password', 'Website', 'Notes'])
        layout.addWidget(self.password_table)

        self.load_passwords()

    def load_passwords(self):
        conn = sqlite3.connect('password_manager.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title, username, password, website, notes 
            FROM passwords 
            WHERE user_id = ?
        ''', (self.user_id,))
        passwords = cursor.fetchall()
        conn.close()

        self.password_table.setRowCount(len(passwords))
        for row, password in enumerate(passwords):
            for col, value in enumerate(password):
                self.password_table.setItem(row, col, QTableWidgetItem(str(value)))

    def show_add_password_dialog(self):
        dialog = AddPasswordDialog(self.user_id, self)
        if dialog.exec():  # Now this works correctly
            self.load_passwords()


class AddPasswordDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle('Add Password')
        self.setFixedSize(300, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel("Title:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('e.g. Gmail')
        layout.addWidget(self.title_input)

        # Username
        layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Your username')
        layout.addWidget(self.username_input)

        # Password
        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Your password')
        layout.addWidget(self.password_input)

        # Website
        layout.addWidget(QLabel("Website:"))
        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText('e.g. https://gmail.com')
        layout.addWidget(self.website_input)

        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText('Additional notes')
        layout.addWidget(self.notes_input)

        # Save button
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_password)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_password(self):
        title = self.title_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        website = self.website_input.text().strip()
        notes = self.notes_input.text().strip()

        if not title or not username or not password:
            QMessageBox.warning(self, 'Error', 'Title, Username, and Password are required.')
            return

        try:
            conn = sqlite3.connect('password_manager.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (user_id, title, username, password, website, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.user_id, title, username, password, website, notes))
            conn.commit()
            conn.close()

            QMessageBox.information(self, 'Success', 'Password saved successfully!')
            self.accept()  # Return success to the parent dialog
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Database error: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()