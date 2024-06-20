import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, \
    QMessageBox, QApplication
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
import requests
from function import findline, AddLine, DeleteLine, DeleteStation, AddStation, insert_station_before, find_n_stations, \
    passenger_board, passenger_alight, FindPassengerNow, FindCardNow, remove_station_from_line, ModifyLine, \
    ModifyStation, Find_Path, Find_station_by_busline, Find_nearby_stations_by_metro_station, search_rides, \
    insert_mul_station_before


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Operation Chooser')
        self.setGeometry(100, 100, 600, 400)

        # 设置背景图片
        self.set_background_image('src/background.png')

        layout = QGridLayout()

        buttons = [
            ('Find Line', self.find_line),
            ('Add Line', self.add_line_operator),
            ('Delete Line', self.delete_line_operator),
            ('Modify Line', self.modify_line_operator),
            ('Add Station', self.add_station_operator),
            ('Delete Station', self.delete_station_operator),
            ('Modify Station', self.modify_station_operator),
            ('Insert Station Before', self.Insert_station_before),
            ('Insert Multiple Station Before', self.Insert_mul_station_before),
            ('Remove Station From Line', self.remove_station_from_line),
            ('Find N Stations', self.find_n_stations),
            ('Passenger Board', self.passenger_board),
            ('Passenger Alight', self.passenger_alight),
            ('Find Passenger Now', self.find_passenger_now),
            ('Find Card Now', self.find_card_now),
            ('Find_Path', self.find_path),
            ('Find station by bus_line', self.Find_station_by_busline),
            ('find nearby stations by metro station', self.Find_nearby_stations_by_metro_station),
            ('search_rides', self.search_rides)
        ]

        row = 0
        col = 0
        for text, func in buttons:
            button = QPushButton(text, self)
            button.setFont(QFont("Arial", 12))
            button.clicked.connect(func)
            layout.addWidget(button, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        # 添加Logout按钮
        logout_button = QPushButton('Logout', self)
        logout_button.setFont(QFont("Arial", 12))
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button, row + 1, 0, 1, 2)

        self.setLayout(layout)

        # 设置样式表
        self.setStyleSheet("""
            QWidget {
                font-size: 16px;
                color: black;
            }
            QPushButton {
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                background-color: white;
                color: black;
                border: 1px solid #4CAF50;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
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

    def logout(self):
        from login_window import LoginWindow  # 延迟导入
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def find_line(self):
        self.operator_chooser = findline()
        self.operator_chooser.show()
        self.close()

    def add_line_operator(self):
        self.operator_chooser = AddLine()
        self.operator_chooser.show()
        self.close()

    def delete_line_operator(self):
        self.operator_chooser = DeleteLine()
        self.operator_chooser.show()
        self.close()

    def modify_line_operator(self):
        self.operator_chooser = ModifyLine()
        self.operator_chooser.show()
        self.close()

    def add_station_operator(self):
        self.operator_chooser = AddStation()
        self.operator_chooser.show()
        self.close()

    def delete_station_operator(self):
        self.operator_chooser = DeleteStation()
        self.operator_chooser.show()
        self.close()

    def modify_station_operator(self):
        self.operator_chooser = ModifyStation()
        self.operator_chooser.show()
        self.close()

    def Insert_station_before(self):
        self.operator_chooser = insert_station_before()
        self.operator_chooser.show()
        self.close()

    def Insert_mul_station_before(self):
        self.operator_chooser = insert_mul_station_before()
        self.operator_chooser.show()
        self.close()

    def remove_station_from_line(self):
        self.operator_chooser = remove_station_from_line()
        self.operator_chooser.show()
        self.close()

    def find_n_stations(self):
        self.operator_chooser = find_n_stations()
        self.operator_chooser.show()
        self.close()

    def passenger_board(self):
        self.operator_chooser = passenger_board()
        self.operator_chooser.show()
        self.close()

    def passenger_alight(self):
        self.operator_chooser = passenger_alight()
        self.operator_chooser.show()
        self.close()

    def find_passenger_now(self):
        self.operator_chooser = FindPassengerNow()
        self.operator_chooser.show()
        self.close()

    def find_card_now(self):
        self.operator_chooser = FindCardNow()
        self.operator_chooser.show()
        self.close()

    def find_path(self):
        self.operator_chooser = Find_Path()
        self.operator_chooser.show()
        self.close()

    def Find_station_by_busline(self):
        self.operator_chooser = Find_station_by_busline()
        self.operator_chooser.show()
        self.close()

    def Find_nearby_stations_by_metro_station(self):
        self.operator_chooser = Find_nearby_stations_by_metro_station()
        self.operator_chooser.show()
        self.close()

    def search_rides(self):
        self.operator_chooser = search_rides()
        self.operator_chooser.show()
        self.close()
