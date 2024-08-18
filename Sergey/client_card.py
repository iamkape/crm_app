from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtWidgets import QLineEdit, QLabel


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('/home/unotuno/python/pet_projects/crm_app/My/store_database.db')
        self.setObjectName("Client card")
        self.resize(958, 497)
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 20, 901, 461))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 6, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 1, 5, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 4, 0, 1, 7)
        # self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        # self.lineEdit.setObjectName("lineEdit")
        # self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        # self.lineEdit_4 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        # self.lineEdit_4.setObjectName("lineEdit_4")
        # self.gridLayout.addWidget(self.lineEdit_4, 2, 3, 1, 1)
        # self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        # self.label_4.setObjectName("label_4")
        # self.gridLayout.addWidget(self.label_4, 2, 4, 1, 1)
        # self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        # self.lineEdit_2.setObjectName("lineEdit_2")
        # self.gridLayout.addWidget(self.lineEdit_2, 2, 0, 1, 1)
        # self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        # self.label_3.setObjectName("label_3")
        # self.gridLayout.addWidget(self.label_3, 1, 4, 1, 1)
        # self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton.setObjectName("pushButton")
        # self.gridLayout.addWidget(self.pushButton, 5, 0, 1, 1)
        # self.lineEdit_6 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        # self.lineEdit_6.setObjectName("lineEdit_6")
        # self.gridLayout.addWidget(self.lineEdit_6, 2, 5, 1, 1)
        # self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        # self.label.setObjectName("label")
        # self.gridLayout.addWidget(self.label, 1, 2, 1, 1)
        # self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        # self.label_6.setObjectName("label_6")
        # self.gridLayout.addWidget(self.label_6, 2, 6, 1, 1)
        # self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton_2.setObjectName("pushButton_2")
        # self.gridLayout.addWidget(self.pushButton_2, 5, 4, 1, 1)
        # self.pushButton_3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton_3.setObjectName("pushButton_3")
        # self.gridLayout.addWidget(self.pushButton_3, 5, 5, 1, 1)
        # self.pushButton_4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        # self.pushButton_4.setObjectName("pushButton_4")
        # self.gridLayout.addWidget(self.pushButton_4, 5, 6, 1, 1)

        self.retranslateUi()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Client card"))
        self.lineedit_data = []
        with self.con:
            row_col = self.con.execute('Pragma table_info ("Customers")').fetchall()
            self.name_of_col = [i[1] for i in row_col]
            for i in range(len(self.name_of_col)):
                if i == 0 :
                    lineedit = QLineEdit(self)
                    lineedit.setEnabled(False)
                else: lineedit = QLineEdit(self)
                label_name = f'label_{i}'
                label = QLabel(f'{self.name_of_col[i]}')
                lineedit_name = f'lineedit_{i}'
                setattr(self, label_name, label)
                setattr(self, lineedit_name, lineedit)
                self.gridLayout.addWidget(lineedit, i+1, 0, 1, 1)
                self.gridLayout.addWidget(label, i+1, 1, 1, 1)

        # self.label_2.setText(_translate("Dialog", "name"))
        # self.label_5.setText(_translate("Dialog", "phone"))
        # self.label_4.setText(_translate("Dialog", "e-mail"))
        # self.label_3.setText(_translate("Dialog", "surname"))
        self.pushButton.setText(_translate("Dialog", "upload document"))
        # self.label.setText(_translate("Dialog", "id"))
        # self.label_6.setText(_translate("Dialog", "address"))
        self.pushButton_2.setText(_translate("Dialog", "Delete client"))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_4.setText(_translate("Dialog", "cancel"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
