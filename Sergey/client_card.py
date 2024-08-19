from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtWidgets import QLineEdit, QLabel, QMessageBox


class Ui_Client_Add(QtWidgets.QDialog):
    def __init__(self,data):
        super().__init__()
        self.data = data
        self.alert_msg = QtWidgets.QMessageBox()
        self.alert_msg.setWindowTitle('Information')
        self.con = sqlite3.connect('My/store_database.db')
        self.setObjectName("Client card")
        self.resize(958, 497)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 901, 461))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 4, 0, 1, 7)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 5, 4, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 5, 5, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 5, 6, 1, 1)
        self.alert_msg.setWindowTitle('Information')
        self.pushButton_4.clicked.connect(self.closeDialog)
        self.pushButton_2.clicked.connect(self.deleteClient)
        self.retranslateUi()


    def retranslateUi(self)->None:
        """В зависимости от того было ли двойное нажатие или нажатие кнопки
        формирует диалоговое окно"""
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Client card"))
        self.pushButton.setText(_translate("Dialog", "upload document"))
        self.pushButton_2.setText(_translate("Dialog", "Delete client"))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_4.setText(_translate("Dialog", "cancel"))
        self.lineedit_data = []
        with self.con:
            row_col = self.con.execute('Pragma table_info ("Customers")').fetchall()
            self.name_of_col = [i[1] for i in row_col]
            for i in range(len(self.name_of_col)):
                if i == 0 :
                    lineedit = QLineEdit(self)
                    lineedit.setEnabled(False)
                    lineedit.setPlaceholderText('Autofill')
                    if self.data is False:
                        lineedit.setText('')
                        self.pushButton_2.setEnabled(False)
                else: lineedit = QLineEdit(self)
                label_name = f'label_{i}'
                label = QLabel(f'{self.name_of_col[i]}')
                lineedit_name = f'lineedit_{i}'
                if self.data is False: lineedit.setText('')
                else :
                    lineedit.setText(self.data[i])
                    self.pushButton_2.setEnabled(True)
                setattr(self, label_name, label)
                setattr(self, lineedit_name, lineedit)
                self.gridLayout.addWidget(lineedit, i+1, 0, 1, 1)
                self.gridLayout.addWidget(label, i+1, 1, 1, 1)
                if 2 <= i <= 3 :
                    self.gridLayout.addWidget(lineedit, i-1, 3, 1, 1)
                    self.gridLayout.addWidget(label, i-1, 4, 1, 1)
                if 4 <= i <= 5:
                    self.gridLayout.addWidget(lineedit, i - 3, 5, 1, 1)
                    self.gridLayout.addWidget(label, i - 3, 6, 1, 1)
                self.setLayout(self.gridLayout)

    def deleteClient(self):
        with self.con:
            try:
                database_query = (f"DELETE FROM Customers WHERE id={self.data[0]}")
                self.alert_msg.setText('Are you sure you want to delete this client?')
                self.alert_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                self.alert_msg.exec_()
                self.alert_msg.accepted(self.con.execute(database_query))
                QtWidgets.QDialog.close(self)
                self.alert_msg.rejected(self.alert_msg.close())
            except Exception as er:
                print(er)

    def saveClient(self):
        pass

    def uploadDoc(self):
        pass

    def closeDialog(self)->None:
        QtWidgets.QDialog.close(self)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Client_Add()
    ui.show()
    sys.exit(app.exec_())
