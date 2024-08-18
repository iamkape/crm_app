#name: Sergey unotuno
#social: tg-> @unotuno
#date: 18.09.2024 23:40


from PyQt5 import QtCore, QtWidgets
import sqlite3
import hashlib
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLabel, QLineEdit, QMessageBox


class Ui_Authorization(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('/home/unotuno/python/pet_projects/crm_app/My/store_database.db')
        self.setObjectName("Authorization")
        self.resize(400, 150)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 20, 581, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(20,20,20,20)
        self.gridLayout.setObjectName("gridLayout")

        self.buttonBox = QtWidgets.QDialogButtonBox(self.gridLayoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")

        self.alert_msg = QMessageBox()
        self.alert_msg.setWindowTitle('Information')

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.createManager)
        self.buttonBox.rejected.connect(self.cancel_dial)


    def retranslateUi(self)->None:
        """Создаёт динамически Label, Lineedit, buttonBox. Поле id неактивно"""
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Add new Manager"))
        self.lineedit_data = []
        with self.con:
            row_col = self.con.execute('Pragma table_info ("Employees")').fetchall()
            self.name_of_col = [i[1] for i in row_col]
            for i in range(len(self.name_of_col)):
                if i == 0 :
                    lineedit = QLineEdit(self)
                    lineedit.setPlaceholderText("Autofill, don't worry")
                    lineedit.setEnabled(False)
                elif i == 1 or i == 2:
                    lineedit = QLineEdit(self)
                    validator  = QRegExpValidator(QRegExp('[a-zA-Z]+'))
                    lineedit.setValidator(validator)
                else:
                    lineedit = QLineEdit(self)
                label_name = f'label_{i}'
                label = QLabel(f'{self.name_of_col[i]}')
                lineedit_name = f'lineedit_{i}'
                setattr(self,label_name,label)
                setattr(self,lineedit_name,lineedit)
                self.gridLayout.addWidget(lineedit, i, 0, 1, 1)
                self.gridLayout.addWidget(label, i, 1, 1, 1)
                self.lineedit_data.append(lineedit)
                self.gridLayout.setSpacing(20)
                self.setLayout(self.gridLayout)
            self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 1)


    def createManager(self)->None:
        """Записывает данные регистрации в БД, в таблицу Employees"""
        with self.con:
            line_text = []
            for i in range(1,len(self.lineedit_data)):
                if i == 4:
                    encode_pass = hashlib.md5(self.lineedit_data[i].text().encode()).hexdigest()
                    line_text.append(encode_pass)
                else: line_text.append(self.lineedit_data[i].text())
            print(line_text)
            val = ', '.join('?' * len(line_text))
            column = ', '.join(self.name_of_col[1:])
            try:
                query_database = (f"""INSERT INTO Employees ({column}) VALUES ({val})""")
                self.con.execute(query_database,line_text)
                self.alert_msg.setText('New manager is created')
                self.alert_msg.setStandardButtons(QMessageBox.Ok)
                self.alert_msg.exec_()
                QtWidgets.QDialog.close(self)
            except Exception as er:
                print(er)
                self.alert_msg.setText('Error, new manager is not created')
                self.alert_msg.setStandardButtons(QMessageBox.Ok)
                self.alert_msg.exec_()


    def cancel_dial(self)->None:
        """Закрывает Диалоговое окно"""
        QtWidgets.QDialog.close(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Authorization()
    ui.show()
    sys.exit(app.exec_())
