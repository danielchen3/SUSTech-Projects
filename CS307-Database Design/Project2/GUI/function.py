from datetime import datetime

from PyQt5.QtCore import QDate, Qt, QDateTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QHBoxLayout, \
    QApplication, QDateTimeEdit
import requests

from PyQt5.QtWidgets import QComboBox, QDateEdit, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QMessageBox

import chooser


class UIUtils:
    @staticmethod
    def add_label(layout, text, parent=None):
        label = QLabel(text, parent)
        label.setFont(QFont('Arial', 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return label

    @staticmethod
    def add_edit(layout, parent=None):
        line_edit = QLineEdit(parent)
        line_edit.setFont(QFont('Arial', 14))
        line_edit.setStyleSheet("padding: 10px;")
        layout.addWidget(line_edit)
        return line_edit

    @staticmethod
    def add_button(layout, text, callback, parent=None):
        button = QPushButton(text, parent)
        button.setFont(QFont('Arial', 14))
        button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border-radius: 5px;
                background-color: #5DADE2;
                color: white;
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
            QPushButton:pressed {
                background-color: #2E86C1;
            }
        """)
        button.clicked.connect(callback)
        layout.addWidget(button)
        return button

    @staticmethod
    def add_text_edit(layout, parent=None):
        text_edit = QTextEdit(parent)
        text_edit.setFont(QFont('Arial', 14))
        text_edit.setReadOnly(True)
        text_edit.setStyleSheet("padding: 10px;")
        layout.addWidget(text_edit)
        return text_edit

    @staticmethod
    def add_combo_box(layout, items, parent=None):
        combo_box = QComboBox(parent)
        combo_box.addItems(items)
        combo_box.setFont(QFont('Arial', 14))
        combo_box.setStyleSheet("padding: 10px;")
        layout.addWidget(combo_box)
        return combo_box

    @staticmethod
    def add_date_edit(layout, parent=None):
        date_edit = QDateEdit(parent)
        date_edit.setFont(QFont('Arial', 14))
        date_edit.setCalendarPopup(True)
        date_edit.setStyleSheet("padding: 10px;")
        layout.addWidget(date_edit)
        return date_edit

    @staticmethod
    def add_time_selectors(layout, parent=None):
        time_layout = QHBoxLayout()
        hours = QComboBox(parent)
        minutes = QComboBox(parent)
        seconds = QComboBox(parent)
        hours.addItems([f'{i:02d}' for i in range(24)])
        minutes.addItems([f'{i:02d}' for i in range(60)])
        seconds.addItems([f'{i:02d}' for i in range(60)])
        for combo in (hours, minutes, seconds):
            combo.setFont(QFont('Arial', 14))
            combo.setStyleSheet("padding: 10px;")
        time_layout.addWidget(hours)
        time_layout.addWidget(minutes)
        time_layout.addWidget(seconds)
        layout.addLayout(time_layout)
        return hours, minutes, seconds

    # @staticmethod
    # def add_date_time_selectors(layout, parent=None):
    #     time_layout = QHBoxLayout()
    #
    #     years = QComboBox(parent)
    #     months = QComboBox(parent)
    #     days = QComboBox(parent)
    #     hours = QComboBox(parent)
    #     minutes = QComboBox(parent)
    #     seconds = QComboBox(parent)
    #
    #     current_year = datetime.now().year
    #     years.addItems([str(year) for year in range(current_year - 10, current_year + 11)])
    #     months.addItems([f'{i:02d}' for i in range(1, 13)])
    #     days.addItems([f'{i:02d}' for i in range(1, 32)])
    #     hours.addItems([f'{i:02d}' for i in range(24)])
    #     minutes.addItems([f'{i:02d}' for i in range(60)])
    #     seconds.addItems([f'{i:02d}' for i in range(60)])
    #
    #     for combo in (years, months, days, hours, minutes, seconds):
    #         combo.setFont(QFont('Arial', 14))
    #         combo.setStyleSheet("padding: 10px;")
    #
    #     time_layout.addWidget(years)
    #     time_layout.addWidget(months)
    #     time_layout.addWidget(days)
    #     time_layout.addWidget(hours)
    #     time_layout.addWidget(minutes)
    #     time_layout.addWidget(seconds)
    #
    #     layout.addLayout(time_layout)
    #     return years, months, days, hours, minutes, seconds

    @staticmethod
    def add_date_time_selectors(layout, parent=None):
        datetime_selector = QDateTimeEdit(parent)
        datetime_selector.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        datetime_selector.setDateTime(QDateTime(0, 1, 1, 0, 0, 0))  # 默认值设为 0
        layout.addWidget(datetime_selector)
        return datetime_selector


class findline(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Line finder')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Line Name:', self)
        self.line_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Find Line', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        line_name = self.line_edit.text()
        if not line_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a line name.')
            return
        try:
            response = requests.get(f'http://127.0.0.1:5000/find_line/{line_name}')
            if response.status_code == 200:
                data = response.json()
                result = data['result']
                formatted_text = f"url: {result}\n"
                self.result_text.setText(formatted_text)
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Line {line_name} not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class AddLine(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Line')
        self.setGeometry(100, 100, 500, 700)

        layout = QVBoxLayout()

        # Add back button
        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label_name = UIUtils.add_label(layout, 'Line Name:', self)
        self.line_name_edit = UIUtils.add_edit(layout, self)

        self.label_start_time = UIUtils.add_label(layout, 'Start Time(HH:MM:SS):', self)
        self.start_time_selectors = UIUtils.add_time_selectors(layout, self)

        self.label_end_time = UIUtils.add_label(layout, 'End Time(HH:MM:SS):', self)
        self.end_time_selectors = UIUtils.add_time_selectors(layout, self)

        self.label_intro = UIUtils.add_label(layout, 'Introduction:', self)
        self.intro_edit = UIUtils.add_edit(layout, self)

        self.label_mileage = UIUtils.add_label(layout, 'Mileage (km):', self)
        self.mileage_edit = UIUtils.add_edit(layout, self)

        self.label_color = UIUtils.add_label(layout, 'Color:', self)
        self.color_edit = UIUtils.add_edit(layout, self)

        self.label_first_opening = UIUtils.add_label(layout, 'First Opening Date:', self)
        self.first_opening_edit = UIUtils.add_date_edit(layout, self)

        self.label_url = UIUtils.add_label(layout, 'URL:', self)
        self.url_edit = UIUtils.add_edit(layout, self)

        self.add_button = UIUtils.add_button(layout, 'Add Line', self.add_line, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def add_line(self):
        line_name = self.line_name_edit.text()
        start_time = f"{self.start_time_selectors[0].currentText()}:{self.start_time_selectors[1].currentText()}:{self.start_time_selectors[2].currentText()}"
        end_time = f"{self.end_time_selectors[0].currentText()}:{self.end_time_selectors[1].currentText()}:{self.end_time_selectors[2].currentText()}"
        intro = self.intro_edit.text()
        mileage = self.mileage_edit.text()
        color = self.color_edit.text()
        first_opening = self.first_opening_edit.date().toString('yyyy-MM-dd')
        url = self.url_edit.text()

        if not all([line_name, start_time, end_time, intro, mileage, color, first_opening, url]):
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        data = {
            'line_name': line_name,
            'start_time': start_time,
            'end_time': end_time,
            'intro': intro,
            'mileage': mileage,
            'color': color,
            'first_opening': first_opening,
            'url': url
        }

        try:
            response = requests.post('http://127.0.0.1:5000/add_line', json=data)
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Line added successfully.')
                self.clear_fields()
            else:
                QMessageBox.warning(self, 'Error', f"Failed to add line: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_fields(self):
        self.line_name_edit.clear()
        self.start_time_selectors[0].setCurrentIndex(0)
        self.start_time_selectors[1].setCurrentIndex(0)
        self.start_time_selectors[2].setCurrentIndex(0)
        self.end_time_selectors[0].setCurrentIndex(0)
        self.end_time_selectors[1].setCurrentIndex(0)
        self.end_time_selectors[2].setCurrentIndex(0)
        self.intro_edit.clear()
        self.mileage_edit.clear()
        self.color_edit.clear()
        self.first_opening_edit.setDate(QDate.currentDate())
        self.url_edit.clear()


class DeleteLine(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Delete Line')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Line Name:', self)
        self.line_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Delete Line', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        line_name = self.line_edit.text()
        print(f"在function中{line_name}")
        if not line_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a line name.')
            return

        try:
            response = requests.delete(f'http://127.0.0.1:5000/delete_line/{line_name}')
            print(response)
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Line Deleted successfully.')
                self.line_edit.clear()
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Line {line_name} not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class ModifyLine(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Modify Line')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        # Add back button
        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label_name = UIUtils.add_label(layout, 'Line Name:', self)
        self.line_name_edit = UIUtils.add_edit(layout, self)

        self.label_start_time = UIUtils.add_label(layout, 'Start Time(HH:MM:SS):', self)
        self.start_time_selectors = UIUtils.add_time_selectors(layout, self)

        self.label_end_time = UIUtils.add_label(layout, 'End Time(HH:MM:SS):', self)
        self.end_time_selectors = UIUtils.add_time_selectors(layout, self)

        self.label_intro = UIUtils.add_label(layout, 'Introduction:', self)
        self.intro_edit = UIUtils.add_edit(layout, self)

        self.label_mileage = UIUtils.add_label(layout, 'Mileage (km):', self)
        self.mileage_edit = UIUtils.add_edit(layout, self)

        self.label_color = UIUtils.add_label(layout, 'Color:', self)
        self.color_edit = UIUtils.add_edit(layout, self)

        self.label_first_opening = UIUtils.add_label(layout, 'First Opening Date:', self)
        self.first_opening_edit = UIUtils.add_date_edit(layout, self)

        self.label_url = UIUtils.add_label(layout, 'URL:', self)
        self.url_edit = UIUtils.add_edit(layout, self)

        self.add_button = UIUtils.add_button(layout, 'Modify Line', self.modify_line, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def get_selected_time(self, selectors):
        return f"{selectors[0].currentText()}:{selectors[1].currentText()}:{selectors[2].currentText()}"

    def modify_line(self):
        line_name = self.line_name_edit.text()
        start_time = f"{self.start_time_selectors[0].currentText()}:{self.start_time_selectors[1].currentText()}:{self.start_time_selectors[2].currentText()}"
        end_time = self.get_selected_time(self.end_time_selectors)
        intro = self.intro_edit.text()
        mileage = self.mileage_edit.text()
        color = self.color_edit.text()
        first_opening = self.first_opening_edit.date().toString('yyyy-MM-dd')
        url = self.url_edit.text()

        default_start_time = "00:00:00"
        default_end_time = "00:00:00"
        defaut_first_opening = "2000-01-01"

        data = {
            'line_name': line_name,
            'start_time': start_time if start_time != default_start_time else '/',
            'end_time': end_time if end_time != default_end_time else '/',
            'intro': intro if intro != '' else '/',
            'mileage': mileage if mileage != '' else '/',
            'color': color if color != '' else '/',
            'first_opening': first_opening if first_opening != defaut_first_opening else '/',
            'url': url if url != '' else '/'
        }

        if not line_name:
            QMessageBox.warning(self, 'Input Error', 'Line Name is required.')
            return

        try:
            response = requests.post('http://127.0.0.1:5000/modify_line', json=data)
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Line Modify successfully.')
                self.clear_fields()
            else:
                QMessageBox.warning(self, 'Error', f"Failed to Modify Line: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_fields(self):
        self.line_name_edit.clear()
        self.start_time_selectors[0].setCurrentIndex(0)
        self.start_time_selectors[1].setCurrentIndex(0)
        self.start_time_selectors[2].setCurrentIndex(0)
        self.end_time_selectors[0].setCurrentIndex(0)
        self.end_time_selectors[1].setCurrentIndex(0)
        self.end_time_selectors[2].setCurrentIndex(0)
        self.intro_edit.clear()
        self.mileage_edit.clear()
        self.color_edit.clear()
        self.first_opening_edit.setDate(QDate.currentDate())
        self.url_edit.clear()


class AddStation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Add Station')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        # Add back button
        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label_name = UIUtils.add_label(layout, 'Station Name:', self)
        self.station_name_edit = UIUtils.add_edit(layout, self)

        self.label_start_time = UIUtils.add_label(layout, 'district', self)
        self.district_edit = UIUtils.add_edit(layout, self)

        self.label_end_time = UIUtils.add_label(layout, 'intro', self)
        self.intro_edit = UIUtils.add_edit(layout, self)

        self.label_intro = UIUtils.add_label(layout, 'Chinese name', self)
        self.chinese_name_edit = UIUtils.add_edit(layout, self)

        self.add_button = UIUtils.add_button(layout, 'Add Station', self.add_station, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        # print("Back Button Clicked!")

    def add_station(self):
        station_name = self.station_name_edit.text()
        district = self.district_edit.text()
        intro = self.intro_edit.text()
        chinese_name = self.chinese_name_edit.text()

        if not all([station_name, district, intro, chinese_name]):
            QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
            return

        data = {
            'station_name': station_name,
            'district': district,
            'intro': intro,
            'chinese_name': chinese_name
        }

        try:
            response = requests.post('http://127.0.0.1:5000/add_station', json=data)
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Station added successfully.')
                self.clear_fields()
            else:
                QMessageBox.warning(self, 'Error', f"Failed to add Station: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_fields(self):
        self.station_name_edit.clear()
        self.district_edit.clear()
        self.chinese_name_edit.clear()
        self.intro_edit.clear()


class DeleteStation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Delete Station')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Station Name:', self)
        self.station_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Delete Station', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        station_name = self.station_edit.text()
        print(f"在function中{station_name}")
        if not station_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a line name.')
            return

        try:
            response = requests.delete(f'http://127.0.0.1:5000/delete_station/{station_name}')
            print(response)
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Station Deleted successfully.')
                self.station_edit.clear()
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station {station_name} not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class ModifyStation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Modify Station')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        # Add back button
        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label_name = UIUtils.add_label(layout, 'Station Name:', self)
        self.station_name_edit = UIUtils.add_edit(layout, self)

        self.label_start_time = UIUtils.add_label(layout, 'district', self)
        self.district_edit = UIUtils.add_edit(layout, self)

        self.label_end_time = UIUtils.add_label(layout, 'intro', self)
        self.intro_edit = UIUtils.add_edit(layout, self)

        self.label_intro = UIUtils.add_label(layout, 'Chinese name', self)
        self.chinese_name_edit = UIUtils.add_edit(layout, self)

        self.add_button = UIUtils.add_button(layout, 'Modify Station', self.modify_station, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        # print("Back Button Clicked!")

    def modify_station(self):
        station_name = self.station_name_edit.text()
        district = self.district_edit.text()
        intro = self.intro_edit.text()
        chinese_name = self.chinese_name_edit.text()

        # if not all([station_name, district, intro, chinese_name]):
        #     QMessageBox.warning(self, 'Input Error', 'Please fill in all fields.')
        #     return

        data = {
            'station_name': station_name if station_name != '' else '/',
            'district': district if district != '' else '/',
            'intro': intro if intro != '' else '/',
            'chinese_name': chinese_name if chinese_name != '' else '/',
        }

        if not station_name:
            QMessageBox.warning(self, 'Input Error', 'Station Name is required.')
            return

        try:
            response = requests.post('http://127.0.0.1:5000/modify_station', json=data)
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Station modified successfully.')
                self.clear_fields()
            else:
                QMessageBox.warning(self, 'Error', f"Failed to Modify Station: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_fields(self):
        self.station_name_edit.clear()
        self.district_edit.clear()
        self.chinese_name_edit.clear()
        self.intro_edit.clear()


class insert_station_before(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Insert_Station_before')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Line Name:', self)
        self.line_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Before Station Name:', self)
        self.before_station_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Station Name:', self)
        self.station_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Insert Station', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        line_name = self.line_edit.text()
        before_station_name = self.before_station_edit.text()
        station_name = self.station_edit.text()
        # print(f"在function中{station_name}")
        if not line_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a line name.')
            return

        data = {'line_name': line_name, 'before_station_name': before_station_name, 'station_name': station_name}

        try:
            response = requests.post(f'http://127.0.0.1:5000/insert_station_before', json=data,
                                     headers={'Content-Type': 'application/json'})
            print(response)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, 'Success', 'Station Inserted successfully.')
                self.station_edit.clear()
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station not found!.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class insert_mul_station_before(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Insert_Multiple_Station_before')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Line Name1:', self)
        self.line1_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Before Station Name1:', self)
        self.before_station1_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Station Name1:', self)
        self.station1_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Line Name2:', self)
        self.line2_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Before Station Name2:', self)
        self.before_station2_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Station Name2:', self)
        self.station2_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Line Name3:', self)
        self.line3_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Before Station Name3:', self)
        self.before_station3_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Station Name3:', self)
        self.station3_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Insert Station', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        line_name1 = self.line1_edit.text()
        before_station_name1 = self.before_station1_edit.text()
        station_name1 = self.station1_edit.text()
        line_name2 = self.line2_edit.text()
        before_station_name2 = self.before_station2_edit.text()
        station_name2 = self.station2_edit.text()
        line_name3 = self.line3_edit.text()
        before_station_name3 = self.before_station3_edit.text()
        station_name3 = self.station3_edit.text()
        # print(f"在function中{station_name}")
        # if not line_name:
        #     QMessageBox.warning(self, 'Input Error', 'Please enter a line name.')
        #     return

        data = {
            'line_name1': line_name1,
            'before_station_name1': before_station_name1,
            'station_name1': station_name1,
            'line_name2': line_name2 if line_name2 != '' else '/',
            'before_station_name2': before_station_name2 if line_name2 != '' else '/',
            'station_name2': station_name2 if line_name2 != '' else '/',
            'line_name3': line_name3 if line_name3 != '' else '/',
            'before_station_name3': before_station_name3 if line_name3 != '' else '/',
            'station_name3': station_name3 if line_name3 != '' else '/',
        }

        try:
            response = requests.post(f'http://127.0.0.1:5000/insert_mul_station_before', json=data,
                                     headers={'Content-Type': 'application/json'})
            print(response)
            if response.status_code == 200:
                QMessageBox.information(self, 'Success', 'Station Inserted successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station not found!.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class remove_station_from_line(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Remove_Station_From_line')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Line Name:', self)
        self.line_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Station Name(to be deleted):', self)
        self.station_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Delete Station', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        line_name = self.line_edit.text()
        station_name = self.station_edit.text()
        # print(f"在function中{station_name}")
        if not line_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a line name.')
            return

        data = {'line_name': line_name, 'station_name': station_name}
        print(f"function{data}")

        try:
            response = requests.delete(f'http://127.0.0.1:5000/remove_station_from_line', json=data)
            print(response)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, 'Success', 'Station Deleted successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class find_n_stations(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('find_n_stations')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Line Name:', self)
        self.line_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Station Name:', self)
        self.station_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter is_forwarding:', self)
        self.is_forwarding_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'n_number:', self)
        self.n_number_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Find Station', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        line_name = self.line_edit.text()
        station_name = self.station_edit.text()
        is_forward = self.is_forwarding_edit.text()
        n = self.n_number_edit.text()
        # print(f"在function中{station_name}")
        if not line_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a line name.')
            return

        data = {
            'line_name': line_name,
            'station_name': station_name,
            'is_forward': is_forward,
            'n': n
        }

        print(data)
        try:
            response = requests.post('http://127.0.0.1:5000/find_n_stations', json=data,
                                     headers={'Content-Type': 'application/json'})
            if response.status_code == 200:
                data = response.json()
                result = data['result']
                formatted_text = f"Station_name: {result['station_name']}\n"
                self.result_text.setText(formatted_text)
                QMessageBox.information(self, 'Success', 'Station Found successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"station not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class passenger_board(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Passenger Board')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Entity number:', self)
        self.entity_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter Start_station_name:', self)
        self.Start_station_name_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'On Board!', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        entity_id = self.entity_edit.text()
        start_station_name = self.Start_station_name_edit.text()
        # print(f"在function中{station_name}")
        if not entity_id:
            QMessageBox.warning(self, 'Input Error', 'Please enter a entity name.')
            return

        data = {'entity_id': entity_id, 'start_station_name': start_station_name}

        try:
            response = requests.post(f'http://127.0.0.1:5000/passenger_board', json=data,
                                     headers={'Content-Type': 'application/json'})
            print(response)
            if response.status_code == 200:
                # data = response.json()
                QMessageBox.information(self, 'Success', 'Record Inserted successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station {start_station_name} not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class passenger_alight(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Passenger off Board')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter Entity number:', self)
        self.entity_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter End_station_name:', self)
        self.station_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Off Board', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        entity_id = self.entity_edit.text()
        end_station_name = self.station_edit.text()
        # print(f"在function中{station_name}")
        if not entity_id:
            QMessageBox.warning(self, 'Input Error', 'Please enter a entity name.')
            return

        data = {'entity_id': entity_id, 'end_station_name': end_station_name}

        try:
            response = requests.post(f'http://127.0.0.1:5000/passenger_alight', json=data,
                                     headers={'Content-Type': 'application/json'})
            print(response)
            if response.status_code == 200:
                data = response.json()
                QMessageBox.information(self, 'Success', 'Record Inserted successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Record Not Found! Off board fail!")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class FindPassengerNow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Find Current Passengers')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.button = UIUtils.add_button(layout, 'Find Current Passengers', self.find_passengers, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def find_passengers(self):
        try:
            response = requests.get('http://127.0.0.1:5000/find_passenger_now')
            if response.status_code == 200:
                data = response.json()
                result = data['ongoing_rides']
                formatted_text = "\n".join([
                    f"Ride ID: {ride['ride_id']}, Passenger ID: {ride['passenger_id']}, Start Station: {ride['start_station']}, Start Time: {ride['start_time']}"
                    for ride in result])
                self.result_text.setText(formatted_text)
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', "No current passengers found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class FindCardNow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Find Current Cards')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.button = UIUtils.add_button(layout, 'Find Current Cards', self.find_cards, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def find_cards(self):
        try:
            response = requests.get('http://127.0.0.1:5000/find_card_now')
            if response.status_code == 200:
                data = response.json()
                result = data['ongoing_rides']
                formatted_text = "\n".join([
                    f"Ride ID: {ride['ride_id']}, Card ID: {ride['card_id']}, Start Station: {ride['start_station']}, Start Time: {ride['start_time']}"
                    for ride in result])
                self.result_text.setText(formatted_text)
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', "No current cards found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class Find_Path(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Passenger Board')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter start_station name:', self)
        self.start_station_edit = UIUtils.add_edit(layout, self)
        self.label = UIUtils.add_label(layout, 'Enter end_station name:', self)
        self.end_station_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Find Path', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        start_station = self.start_station_edit.text()
        end_station = self.end_station_edit.text()
        # print(f"在function中{station_name}")
        if not start_station:
            QMessageBox.warning(self, 'Input Error', 'Please enter a real station.')
            return

        data = {'start_station': start_station, 'end_station': end_station}

        try:
            response = requests.get(f'http://127.0.0.1:5000/find_path', json=data,
                                    headers={'Content-Type': 'application/json'})
            print(response)
            if response.status_code == 200:
                data = response.json()
                result = data['result']
                formatted_text = f"routes: {result}\n"
                self.result_text.setText(formatted_text)
                QMessageBox.information(self, 'Success', 'Path Found successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class Find_station_by_busline(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Find station by busline')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter bus_line name', self)
        self.bus_line_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Find station', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        bus_line = self.bus_line_edit.text()
        if not bus_line:
            QMessageBox.warning(self, 'Input Error', 'Please enter a real station.')
            return

        data = {'bus_line': bus_line}

        try:
            response = requests.get(f'http://127.0.0.1:5000/find_stations_by_bus_line', json=data,
                                    headers={'Content-Type': 'application/json'})
            print(response)
            if response.status_code == 200:
                data = response.json()
                formatted_text = f"Bus stations: {data['result']}\n"
                self.result_text.setText(formatted_text)
                QMessageBox.information(self, 'Success', 'Stations Found successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class Find_nearby_stations_by_metro_station(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Find bus station by metro station')
        self.setGeometry(100, 100, 700, 500)

        layout = QVBoxLayout()

        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label = UIUtils.add_label(layout, 'Enter metro_station name', self)
        self.station_edit = UIUtils.add_edit(layout, self)
        self.button = UIUtils.add_button(layout, 'Find Bus station', self.solve, self)
        self.result_text = UIUtils.add_text_edit(layout, self)

        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def solve(self):
        station_name = self.station_edit.text()
        if not station_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a station name.')
            return

        data = {'station_name': station_name}

        try:
            response = requests.get(f'http://127.0.0.1:5000/find_nearby_stations_by_metro_station', json=data,
                                    headers={'Content-Type': 'application/json'})
            print(response)
            if response.status_code == 200:
                data = response.json()
                print("daole")
                print(data)
                formatted_text = f"Bus stations: {data['result']}\n"
                self.result_text.setText(formatted_text)
                QMessageBox.information(self, 'Success', 'Stations Found successfully.')
            else:
                self.result_text.setText('')
                QMessageBox.warning(self, 'Not Found', f"Station not found.")
        except requests.exceptions.RequestException as e:
            self.result_text.setText('')
            QMessageBox.critical(self, 'Error', str(e))


class search_rides(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Search rides')
        self.setGeometry(100, 100, 800, 1000)

        layout = QVBoxLayout()

        # Add back button
        self.back_button = QPushButton('< Back', self)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.label_name = UIUtils.add_label(layout, 'Ride id:', self)
        self.ride_id_edit = UIUtils.add_edit(layout, self)

        self.label_color = UIUtils.add_label(layout, 'Entity id', self)
        self.Entity_edit = UIUtils.add_edit(layout, self)

        self.label_intro = UIUtils.add_label(layout, 'start station:', self)
        self.start_edit = UIUtils.add_edit(layout, self)

        self.label_end_station = UIUtils.add_label(layout, 'end station:', self)
        self.end_edit = UIUtils.add_edit(layout, self)

        self.label_start_time_from = UIUtils.add_label(layout, 'Start Time from:', self)
        self.start_time_from_selectors = UIUtils.add_date_time_selectors(layout, self)

        self.label_start_time_to = UIUtils.add_label(layout, 'Start Time to:', self)
        self.start_time_to_selectors = UIUtils.add_date_time_selectors(layout, self)

        self.label_end_time_from = UIUtils.add_label(layout, 'End Time from:', self)
        self.end_time_from_selectors = UIUtils.add_date_time_selectors(layout, self)

        self.label_end_time_to = UIUtils.add_label(layout, 'End Time to:', self)
        self.end_time_to_selectors = UIUtils.add_date_time_selectors(layout, self)

        self.add_button = UIUtils.add_button(layout, 'Search ride', self.search_rides, self)
        self.result_text = UIUtils.add_text_edit(layout, self)
        self.setLayout(layout)
        self.center()

    def center(self):
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        # 将窗口水平居中，垂直位置为屏幕高度的四分之一
        x = (screen.width() - size.width()) // 2
        y = screen.height() // 4
        self.move(x, y)

    def go_back(self):
        self.main_window = chooser.MainWindow()
        self.main_window.show()
        self.close()
        print("Back Button Clicked!")

    def get_selected_datetime(self, selector):
        dt = selector.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        default_dt = "2000-01-01 00:00:00"
        return dt if dt != default_dt else "/"

    def search_rides(self):
        ride_id = self.ride_id_edit.text()
        entity_id = self.Entity_edit.text()
        start_station = self.start_edit.text()
        end_station = self.end_edit.text()
        start_time_from = self.get_selected_datetime(self.start_time_from_selectors)
        start_time_to = self.get_selected_datetime(self.start_time_to_selectors)
        end_time_from = self.get_selected_datetime(self.end_time_from_selectors)
        end_time_to = self.get_selected_datetime(self.end_time_to_selectors)

        data = {
            'ride_id': ride_id if ride_id != '' else '/',
            'entity_id': entity_id if entity_id != '' else '/',
            'start_station': start_station if start_station != '' else '/',
            'end_station': end_station if end_station != '' else '/',
            'start_time_from': start_time_from,
            'start_time_to': start_time_to,
            'end_time_from': end_time_from,
            'end_time_to': end_time_to,
        }

        print(f"data: {data}")

        # 将时间解析为 datetime 对象
        # try:
        #     if data['start_time_from'] != '/':
        #         data['start_time_from'] = datetime.strptime(data['start_time_from'], '%Y-%m-%d %H:%M:%S')
        #     if data['start_time_to'] != '/':
        #         data['start_time_to'] = datetime.strptime(data['start_time_to'], '%Y-%m-%d %H:%M:%S')
        #     if data['end_time_from'] != '/':
        #         data['end_time_from'] = datetime.strptime(data['end_time_from'], '%Y-%m-%d %H:%M:%S')
        #     if data['end_time_to'] != '/':
        #         data['end_time_to'] = datetime.strptime(data['end_time_to'], '%Y-%m-%d %H:%M:%S')
        # except ValueError as e:
        #     print(f"Time format error: {e}")
        #     return

        print(f"data_final:{data}")

        try:
            response = requests.get('http://127.0.0.1:5000/search_rides', json=data)
            if response.status_code == 200:
                self.clear_fields()
                data = response.json()
                formatted_text = f"Records Passenger: {data['passenger_rides']}\n Records Cards:{data['card_rides']}"
                self.result_text.setText(formatted_text)
                QMessageBox.information(self, 'Success', 'search rides successfully.')
                self.clear_fields()
            else:
                QMessageBox.warning(self, 'Error', f"Failed to Search rides: {response.text}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', str(e))

    def clear_fields(self):
        self.ride_id_edit.clear()
        self.Entity_edit.clear()
        self.start_edit.clear()
        self.end_edit.clear()
        self.start_time_from_selectors.setDateTime(QDateTime(0, 1, 1, 0, 0, 0))
        self.start_time_to_selectors.setDateTime(QDateTime(0, 1, 1, 0, 0, 0))
        self.end_time_from_selectors.setDateTime(QDateTime(0, 1, 1, 0, 0, 0))
        self.end_time_to_selectors.setDateTime(QDateTime(0, 1, 1, 0, 0, 0))
