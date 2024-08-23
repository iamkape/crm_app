import sqlite3
import hashlib


from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication
from Ruslan.main_dialog import MainDialog

class LoginW(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(300, 150)

        # Подключение к базе данных
        self.con = sqlite3.connect('My/store_database.db')

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

    def login(self)->None:
        """Проверка логина и пароля"""
        username = self.input_username.text()
        password = self.input_password.text()
        hash_password = hashlib.md5(password.encode()).hexdigest()
        print(hash_password)
        with self.con:
            user = self.con.execute("SELECT * FROM Employees WHERE login=? AND password=?", (username,
                                                                   hash_password)).fetchall()
            access = self.con.execute('SELECT super_admin FROM Employees WHERE login=? AND password=?', (username,
                                                                                                         hash_password)).fetchall()
            id = self.con.execute('SELECT id FROM Employees WHERE login=? AND password=?', (username,

                                                                                            hash_password)).fetchone()
            if user:
                QMessageBox.information(self, "Поздравляю", "Вход выполнен!")
                self.open_main(access,id)
            else:
                QMessageBox.information(self, "Попробуй снова","Неверный логин или пароль")

    def get_names(self, table):
        col_names = []
        with self.con:
            names = self.con.execute(f'PRAGMA table_info ("{table}") ').fetchall()
            for i in names:
                if 'id' in i[1]:
                    continue
                else: col_names.append(i[1])
        return col_names


    def open_main(self, rights:list, id:list)->None:
        """Если прологинился то открывает главное окно"""
        access_rights = (', '.join(*rights))
        manager_id = [str(i) for i in id]
        pattern_doc = {
                         'Customers' : self.get_names('Customers'),
                         'Employees' : self.get_names('Employees'),
                         'Products' : self.get_names('Products'),
                         'Stock' : self.get_names('Stock'),
                         'Transactions_history' : self.get_names('Transactions_history'),
                         'Warehouses' : self.get_names('Warehouses')
                      }
        print(pattern_doc)
        # from docx import Document
        # doc = Document()
        # doc.add_heading("Вот доступные поля для создания шаблона", level=1)
        # for k, v in pattern_doc.items():
        #     doc.add_paragraph('')
        #     doc.add_paragraph(f'{k}  -- {", ".join(v)}')
        #     doc.add_paragraph('')
        # doc.save('My/shablon.docx')
        self.main_window = MainDialog(access_rights, *manager_id, pattern_doc)
        self.main_window.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = LoginW()
    ui.show()
    sys.exit(app.exec_())
    #52dfwf33