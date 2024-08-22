from PyQt5 import QtCore, QtGui, QtWidgets
from dialog1 import Ui_Dialog
import sqlite3

class Ui_MainWindow(object):
    def openDialog(self):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.dialog)
        self.dialog.show()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(782, 473)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(20, 10, 111, 31))
        self.comboBox.setObjectName("comboBox")


        self.trans = ['acceptance', 'sale', 'write-off', 'movement']
        self.comboBox.addItems(self.trans)

        # self.comboBox.currentIndexChanged.connect(self.selected_changeIndex)


        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 60, 751, 231))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.openDialog())
        self.pushButton.setGeometry(QtCore.QRect(670, 10, 93, 28))

        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.con = sqlite3.connect('store_database.db')
        self.table_name = 'Transactions_history'

        with self.con:
            resp = self.con.execute(f"Pragma table_info ({self.table_name})").fetchall()
            self.columns_list = [i[1] for i in resp]
            # print(self.columns_list)
            table_data = self.con.execute(f"SELECT * FROM {self.table_name}").fetchall()
            self.tableWidget.setColumnCount(len(self.columns_list))
            self.tableWidget.setHorizontalHeaderLabels(self.columns_list)
            self.tableWidget.setRowCount(len(table_data))
            for i in range(len(table_data)):
                for j in range(len(table_data[i])):
                    item = QtWidgets.QTableWidgetItem(str(table_data[i][j]))
                    self.tableWidget.setItem(i, j, item)

    # def selected_changeIndex(self, index):
    #     self.columns = ['id', 'transaction_type', 'product_id', 'warehouse_from', 'warehouse_to', 'quantity', 'transaction_date', 'customer_id', 'status', 'employee_id']
    #     # dicty = {}
    #     self.col = []
    #     with self.con:
    #         table_data = []
    #         if self.comboBox.currentIndex() == 0:
    #             table_data = self.con.execute(f"SELECT * FROM {self.table_name} WHERE transaction_type = {self.trans[0]}").fetchall()
    #             print(table_data)
    #             self.col = ['id', 'transaction_type', 'product_id', 'warehouse_to', 'quantity',
    #                             'transaction_date', 'status', 'employee_id']
    #         if self.comboBox.currentIndex() == 1:
    #             table_data = self.con.execute(
    #                 f"SELECT * FROM {self.table_name} WHERE transaction_type = {self.trans[1]}").fetchall()
    #             print(table_data)
    #             self.col = ['id', 'transaction_type', 'product_id', 'warehouse_from', 'quantity',
    #                             'transaction_date', 'customer_id', 'status', 'employee_id']
    #         if self.comboBox.currentIndex() == 2:
    #             table_data = self.con.execute(
    #                 f"SELECT * FROM {self.table_name} WHERE transaction_type = {self.trans[2]}").fetchall()
    #             print(table_data)
    #             self.col = ['id', 'transaction_type', 'product_id', 'warehouse_from', 'warehouse_to', 'quantity',
    #                             'transaction_date', 'status', 'employee_id']
    #         if self.comboBox.currentIndex() == 3:
    #             table_data = self.con.execute(
    #                 f"SELECT * FROM {self.table_name} WHERE transaction_type = {self.trans[3]}").fetchall()
    #             print(table_data)
    #             self.col = ['id', 'transaction_type', 'product_id', 'warehouse_from', 'warehouse_to', 'quantity',
    #                             'transaction_date', 'status', 'employee_id']
    #         # self.con = str(self.col)
            # print(self.con)
            # table_data = self.con.execute(f"SELECT {self.con} FROM {self.table_name}").fetchall()
            # self.tableWidget.clear()
            # self.tableWidget.setColumnCount(len(self.columns))
            # self.tableWidget.setHorizontalHeaderLabels(self.columns)
            # self.tableWidget.setRowCount(len(table_data))
            # for i in range(len(table_data)):
            #     for j in range(len(table_data[i])):
            #         item = QtWidgets.QTableWidgetItem(str(table_data[i][j]))
            #         self.tableWidget.setItem(i, j, item)


        # print(index)
        # print(self.comboBox.currentIndex())
        # print(self.comboBox.currentText())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "New"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
