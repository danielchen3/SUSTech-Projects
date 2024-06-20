import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QApplication, \
    QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
import requests

import chooser


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 700, 500)  # Increase window size

        # 设置背景图片
        self.set_background_image('src/background.png')

        layout = QVBoxLayout()

        # 添加间隔以调整布局
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.label_username = QLabel('Username:', self)
        self.label_username.setFont(QFont("Arial", 20))  # Increase font size
        layout.addWidget(self.label_username)

        self.username_edit = QLineEdit(self)
        self.username_edit.setFont(QFont("Arial", 18))  # Increase font size
        layout.addWidget(self.username_edit)

        # 添加间隔以调整布局
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.label_password = QLabel('Password:', self)
        self.label_password.setFont(QFont("Arial", 20))  # Increase font size
        layout.addWidget(self.label_password)

        self.password_edit = QLineEdit(self)
        self.password_edit.setFont(QFont("Arial", 18))  # Increase font size
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_edit)

        # 添加间隔以调整布局
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.button = QPushButton('Login', self)
        self.button.setFont(QFont("Arial", 20))  # Increase font size
        self.button.clicked.connect(self.login)
        layout.addWidget(self.button)

        self.setLayout(layout)

        # 设置样式表
        self.setStyleSheet("""
            QWidget {
                font-size: 20px;
                color: white;
            }
            QLineEdit, QPushButton {
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.8);
                color: black;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.center()

    def set_background_image(self, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if not username or not password:
            QMessageBox.warning(self, 'Input Error', 'Please enter both username and password.')
            return

        try:
            response = requests.post('http://127.0.0.1:5000/login', json={'username': username, 'password': password})
            if response.status_code == 200:
                self.main_window = chooser.MainWindow()
                print("MainWindow chosen")
                self.main_window.show()
                self.close()
            else:
                self.show_warning_message('Login Failed', 'Invalid username or password.')
                self.username_edit.clear()
                self.password_edit.clear()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            QMessageBox.critical(self, 'Error', str(e))

    def show_warning_message(self, title, message):
        msg_box = QMessageBox(QMessageBox.Warning, title, message, QMessageBox.Ok, self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2c2c2c;
                color: white;
                font-size: 18px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        msg_box.exec_()

    def show_critical_message(self, title, message):
        msg_box = QMessageBox(QMessageBox.Critical, title, message, QMessageBox.Ok, self)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2c2c2c;
                color: white;
                font-size: 18px;
            }
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        msg_box.exec_()
