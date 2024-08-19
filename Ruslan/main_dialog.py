

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTabWidget, QWidget, QVBoxLayout, QLabel, QTableWidget
from functools import partial
import sqlite3
from Sergey.client_card import Ui_Client_Add
from Sergey.authorization import Ui_Authorization
#from Maksim.warehouse_dialog import AddWarehouseDialog
from Maksim.product_dialog import AddProductDialog


class MainDialog(QtWidgets.QDialog):
    def __init__(self, user=None, manager_id=None):
        super().__init__()
        self.manager_id = manager_id
        self.user = user
        self.con = sqlite3.connect('My/store_database.db')
        self.table_widgets = []  # Ссылки на виджеты таблиц.
        self.table_names = ['Transactions_history', 'Customers', 'Stock', 'Products']

        self.setObjectName("Dialog")
        self.setFixedSize(1200, 940)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1200, 940))
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 1175, 850))
        self.tableWidget.setObjectName("tableWidget")
        self.table_widgets.append(self.tableWidget)
        self.table_widgets[0].setEditTriggers(QTableWidget.NoEditTriggers)

        self.new_transaction = QtWidgets.QPushButton(self.tab)
        self.new_transaction.setGeometry(QtCore.QRect(1040, 10, 131, 31))
        self.new_transaction.setObjectName("new_transaction")

        self.upload_document = QtWidgets.QPushButton(self.tab)
        self.upload_document.setGeometry(QtCore.QRect(900, 10, 131, 31))
        self.upload_document.setObjectName("upload_document")

        self.add_document = QtWidgets.QPushButton(self.tab)
        self.add_document.setGeometry(QtCore.QRect(620, 10, 131, 31))
        self.add_document.setObjectName("add_document")
        if user != 'super':
            self.add_document.setEnabled(False)

        self.add_manager = QtWidgets.QPushButton(self.tab)
        self.add_manager.setGeometry(QtCore.QRect(760, 10, 131, 31))
        self.add_manager.setObjectName("add_manager")
        if user != 'super':
            self.add_manager.setEnabled(False)

        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(180, 20, 153, 21))
        self.lineEdit.setObjectName("lineEdit")

        self.tabWidget.addTab(self.tab, "")

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setGeometry(QtCore.QRect(10, 50, 1175, 850))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.table_widgets.append(self.tableWidget_2)
        self.table_widgets[1].setEditTriggers(QTableWidget.NoEditTriggers)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 20, 153, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.add_client = QtWidgets.QPushButton(self.tab_2)
        self.add_client.setGeometry(QtCore.QRect(1040, 10, 131, 31))
        self.add_client.setObjectName("add_client")

        self.tabWidget.addTab(self.tab_2, "")

        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.tableWidget_3 = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_3.setGeometry(QtCore.QRect(10, 50, 1175, 850))
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.table_widgets.append(self.tableWidget_3)
        self.table_widgets[2].setEditTriggers(QTableWidget.NoEditTriggers)

        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(180, 20, 153, 21))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.add_warehouse = QtWidgets.QPushButton(self.tab_3)
        self.add_warehouse.setGeometry(QtCore.QRect(1040, 10, 131, 31))
        self.add_warehouse.setObjectName("add_warehouse")

        self.edit_warehouse = QtWidgets.QPushButton(self.tab_3)
        self.edit_warehouse.setGeometry(QtCore.QRect(900, 10, 131, 31))
        self.edit_warehouse.setObjectName("edit_warehouse")

        self.comboBox = QtWidgets.QComboBox(self.tab_3)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 161, 21))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Stock'])
        self.warehouse_count = self.add_warehouses_to_combobox()

        self.tabWidget.addTab(self.tab_3, "")

        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.tableWidget_4 = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_4.setGeometry(QtCore.QRect(10, 50, 1175, 850))
        self.tableWidget_4.setObjectName("tableWidget_4")
        self.table_widgets.append(self.tableWidget_4)
        self.table_widgets[3].setEditTriggers(QTableWidget.NoEditTriggers)

        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_4.setGeometry(QtCore.QRect(180, 20, 153, 21))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.add_product = QtWidgets.QPushButton(self.tab_4)
        self.add_product.setGeometry(QtCore.QRect(1040, 10, 131, 31))
        self.add_product.setObjectName("add_product")

        self.tabWidget.addTab(self.tab_4, "")

        self.tabWidget.currentChanged.connect(self.insert_data_into_table)
        self.comboBox.activated.connect(self.insert_data_into_table)
        self.add_client.clicked.connect(self.open_client_card)
        self.add_manager.clicked.connect(self.open_manager_card)
        self.add_product.clicked.connect(self.open_product_card)
        self.tableWidget_2.cellDoubleClicked.connect(self.open_client_card)
        self.tableWidget_4.cellDoubleClicked.connect(self.open_product_card)
        # self.add_warehouse.clicked.connect(self.open_warehouse_card)
        # self.edit_warehouse.clicked.connect(partial(self.open_warehouse_card, True))

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "CRM Application"))
        self.new_transaction.setText(_translate("Dialog", "New transaction"))
        self.upload_document.setText(_translate("Dialog", "Upload document"))
        self.add_document.setText(_translate("Dialog", "Add document"))
        self.add_manager.setText(_translate("Dialog", "Add manager"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Operations"))
        self.add_client.setText(_translate("Dialog", "Add client"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Сlients"))
        self.add_warehouse.setText(_translate("Dialog", "Add warehouse"))
        self.edit_warehouse.setText(_translate("Dialog", "Edit warehouse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Warehouses"))
        self.add_product.setText(_translate("Dialog", "Add product"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Products"))

    def insert_data_into_table(self) -> None:
        """Заполняет tableWidget данными из текущей таблицы в comboBox."""
        #self.changes_dict = {}  # Обнуляем словарь изменений
        combobox_id = self.comboBox.currentIndex()
        tab_index = self.tabWidget.currentIndex()
        table = self.table_widgets[tab_index]
        with self.con:
            resp = self.con.execute(f"Pragma table_info ({self.table_names[tab_index]})").fetchall()
            self.columns_list = [i[1] for i in resp]
            table_data = self.con.execute(f"SELECT * FROM {self.table_names[tab_index]}").fetchall()
            rows_list = [str(i[0]) for i in table_data]
            self.table_widgets[tab_index].setColumnCount(len(self.columns_list))  # Указывает количество столбцов.
            self.table_widgets[tab_index].setHorizontalHeaderLabels(self.columns_list)  # Указывает имена столбцов.
            self.table_widgets[tab_index].setRowCount(len(rows_list))  # Указывает количество строк.
            self.table_widgets[tab_index].setVerticalHeaderLabels(rows_list)  # Указывает имена строк.
            for i in range(len(table_data)):
                #self.changes_dict[str(rows_list[i])] = dict.fromkeys(self.columns_list, None)
                for j in range(len(table_data[i])):
                    #self.changes_dict[str(rows_list[i])][self.columns_list[j]] = table_data[i][j]
                    item = QtWidgets.QTableWidgetItem(str(table_data[i][j]))
                    self.table_widgets[tab_index].setItem(i, j, item)

    def add_warehouses_to_combobox(self):
        warehouse_names = [el[0] for el in self.con.execute("SELECT name FROM Warehouses").fetchall()]
        self.comboBox.addItems(warehouse_names)
        return len(warehouse_names) + 1

    def get_string_values(self, row):
        column_count = self.table_widgets[self.tabWidget.currentIndex()].columnCount()
        values = []
        for column in range(column_count):
            item = self.table_widgets[self.tabWidget.currentIndex()].item(row, column)
            if item is not None:
                values.append(item.text())
            else:
                values.append('')  # Если ячейка пустая
        return values

    def open_client_card(self, arg):
        if arg is not False:
            arg = self.get_string_values(arg)
        client_card_window = Ui_Client_Add(arg)
        resp = client_card_window.exec_()

    def open_manager_card(self):
        manager_card_window = Ui_Authorization()
        resp = manager_card_window.exec_()

    # def open_warehouse_card(self, arg=None):
    #     warehouse = self.comboBox.currentText()
    #     if arg and warehouse != 'Stock':
    #         arg = self.con.execute(f"SELECT * FROM Warehouses WHERE name = '{warehouse}'").fetchall()[0]
    #     print(arg)
    #     warehouse_card_window = AddWarehouseDialog(arg)
    #     resp = warehouse_card_window.exec_()

    def open_product_card(self, arg):
        if arg is not False:
            arg = self.get_string_values(arg)
        product_card_window = AddProductDialog(arg, self.manager_id)
        resp = product_card_window.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainDialog()
    ui.show()
    sys.exit(app.exec_())
