import sqlite3
import hashlib
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication


class LoginW(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(300, 150)

        # Подключение к базе данных
        self.con = sqlite3.connect('my/store_database.db')

        # Элементы интерфейса
        self.label_username = QLabel("Имя пользователя:")
        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("Введите имя пользователя")

        self.label_password = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Введите пароль")
        self.input_password.setEchoMode(QLineEdit.Password)

        self.button_login = QPushButton("Войти")
        self.button_login.clicked.connect(self.login)

        # Вертикальный макет
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        self.setLayout(layout)

    def login(self):
        """Проверка логина и пароля"""
        username = self.input_username.text()
        password = self.input_password.text()
        hash_password = hashlib.md5(password.encode()).hexdigest()
        print(hash_password)
        with self.con:
            user = self.con.execute("SELECT * FROM Employees WHERE first_name=? AND password=?", (username,
                                                                                        hash_password)).fetchall()
            if user:
                QMessageBox.information(self, "Поздравляю", "Вход выполнен!")
                self.open_main()
            else:

                QMessageBox.information(self, "Попробуй снова","Неверный логин или пароль")


    def open_main(self):
        """Если прологинился то открывает главное окно"""
        # self.main_window = Ui_MainWindow()
        # self.main_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = LoginW()
    ui.show()
    sys.exit(app.exec_())
    #52dfwf33