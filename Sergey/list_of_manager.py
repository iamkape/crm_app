from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


class Ui_listManager(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('My/store_database.db')
        self.setObjectName("list_manager")
        self.resize(836, 577)
        self.alert_msg = QtWidgets.QMessageBox()
        self.alert_msg.setWindowTitle('Information')
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30, 70, 771, 281))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(30, 390, 761, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False)
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_2.clicked.connect(self.closeDial)
        self.pushButton.clicked.connect(self.deleteManager)
        self.tableWidget.clicked.connect(self.chooseManager)
        self.retranslateUi()
        self.fullDial()



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("list_manager", "List Manager"))
        self.pushButton.setText(_translate("list_manager", "delete manager"))
        self.pushButton_2.setText(_translate("list_manager", "cancel"))


    def fullDial(self):
        with self.con:
            col = self.con.execute('Pragma table_info ("Employees")').fetchall()
            column_names = [n[1] for n in col]
            val = self.con.execute('SELECT * FROM Employees').fetchall()
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            self.tableWidget.setRowCount(len(val))
            self.tableWidget.setColumnCount(len(column_names))
            for x in range(len(val)):
                for y in range(len(val[x])):
                    item = QtWidgets.QTableWidgetItem(str(val[x][y]))
                    item.setFlags(item.flags() & ~ Qt.ItemIsEditable)
                    self.tableWidget.setItem(x, y, item)

    def closeDial(self):
        QtWidgets.QDialog.close(self)

    def chooseManager(self):
        self.pushButton.setEnabled(True)

    def deleteManager(self):
        cur = self.tableWidget.currentRow()
        current_id = self.tableWidget.item(cur,0).text()
        print(current_id)
        with self.con:
            try:
                database_query = (f"DELETE FROM Employees WHERE id={current_id}")
                self.alert_msg.setText('Are you sure you want to delete this manager?')
                self.alert_msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                res = self.alert_msg.exec_()
                if res == QMessageBox.Ok:
                    self.con.execute(database_query)
                    self.alert_msg.close()
                else:
                    self.alert_msg.close()
            except Exception as er:
                self.alert_msg.setText(f'Something Wrong {er}')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_listManager()
    ui.show()
    sys.exit(app.exec_())
