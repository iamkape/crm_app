import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sqlite3


class DialogWindow(qtw.QWidget):

    submitted = qtc.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.resize(400, 350)

        self.comboBox = qtw.QComboBox()
        self.comboBox.addItems(['acceptance', 'sale', 'write-off', 'movement'])

        self.con = sqlite3.connect('store_database.db')  #!!!!!!!!!!!!!!! Change path, please!!!!!!!!!!

        with self.con:
            # table_data_product_id = self.con.execute("SELECT id FROM Products").fetchall()

            table_data_warehouse_id = self.con.execute("SELECT id, warehouse_name FROM Warehouses").fetchall()

            table_data_customers_id = self.con.execute("SELECT id, cust_last_name FROM Customers").fetchall()
            # table_data_employees_id = self.con.execute("SELECT id FROM Employees").fetchall()

            table_data = self.con.execute("SELECT id, product_name FROM Products").fetchall()

        # print(table_data)
        dicty = {}
        for i in range(len(table_data)):
            if dicty.get(list(table_data[i])[1], []):
                dicty[list(table_data[i])[1]].append(str(list(table_data[i])[0]))
            else:
                dicty[list(table_data[i])[1]] = [str(list(table_data[i])[0])]
        # print(dicty)
        self.comboBox_1 = qtw.QComboBox()

        for i in dicty.keys():
            self.comboBox_1.addItem(str(i), dicty[i])

        self.comboBox_1.activated.connect(self.clicker)

        self.comboBox_11 = qtw.QComboBox()
        self.comboBox_11.addItem(str(list(table_data[0])[0]))


        # Warehouses
        dicty = {}
        for i in range(len(table_data_warehouse_id)):
            if dicty.get(list(table_data_warehouse_id[i])[1], []):
                dicty[list(table_data_warehouse_id[i])[1]].append(str(list(table_data_warehouse_id[i])[0]))
            else:
                dicty[list(table_data_warehouse_id[i])[1]] = [str(list(table_data_warehouse_id[i])[0])]
        # print(dicty)
        self.comboBox_2 = qtw.QComboBox()
        self.comboBox_3 = qtw.QComboBox()

        for i in dicty.keys():
            self.comboBox_2.addItem(str(i), dicty[i])
            self.comboBox_3.addItem(str(i), dicty[i])


        self.comboBox_2.activated.connect(self.clicker2)
        self.comboBox_3.activated.connect(self.clicker3)

        self.comboBox_21 = qtw.QComboBox()
        self.comboBox_21.addItem(str(list(table_data_warehouse_id[0])[0]))

        self.comboBox_31 = qtw.QComboBox()
        self.comboBox_31.addItem(str(list(table_data_warehouse_id[0])[0]))

        #  Customers
        dicty = {}
        for i in range(len(table_data_customers_id)):
            if dicty.get(list(table_data_customers_id[i])[1], []):
                dicty[list(table_data_customers_id[i])[1]].append(str(list(table_data_customers_id[i])[0]))
            else:
                dicty[list(table_data_customers_id[i])[1]] = [str(list(table_data_customers_id[i])[0])]
        # print(dicty)
        self.comboBox_6 = qtw.QComboBox()

        for i in dicty.keys():
            self.comboBox_6.addItem(str(i), dicty[i])

        self.comboBox_6.activated.connect(self.clicker6)

        self.comboBox_61 = qtw.QComboBox()
        self.comboBox_61.addItem(str(list(table_data_customers_id[0])[0]))

# product_id
#         self.comboBox_1 = qtw.QComboBox()
#         self.temp_list = []
#         for item in table_data_product_id:
#             self.temp_list.append(list(item)[0])
#         self.temp_list.sort()
#         for item in self.temp_list:
#             self.comboBox_1.addItem(str(item))
#         print(self.temp_list)
# Warehouse from
# Warehouse to
#         self.comboBox_2 = qtw.QComboBox()
#         self.comboBox_3 = qtw.QComboBox()
#         self.temp_list = []
#         for item in table_data_warehouse_id:
#             self.temp_list.append(list(item)[0])
#         self.temp_list.sort()
#         for item in self.temp_list:
#             self.comboBox_2.addItem(str(item))
#             self.comboBox_3.addItem(str(item))
        # print(self.temp_list)
# Customers
#         self.comboBox_6 = qtw.QComboBox()
#         self.temp_list = []
#         for item in table_data_customers_id:
#             self.temp_list.append(list(item)[0])
#         self.temp_list.sort()
#         for item in self.temp_list:
#             self.comboBox_6.addItem(str(item))
        # print(self.temp_list)
# Employees
#         self.comboBox_8 = qtw.QComboBox()
#         self.temp_list = []
#         for item in table_data_employees_id:
#             self.temp_list.append(list(item)[0])
#         self.temp_list.sort()
#         for item in self.temp_list:
#             self.comboBox_8.addItem(str(item))
        # print(self.temp_list)

        # self.comboBox_1.setEditable(True)
        # self.comboBox_2.setEditable(True)
        # self.comboBox_3.setEditable(True)
        # self.comboBox_6.setEditable(True)
        # self.comboBox_8.setEditable(True)

        self.comboBox.currentIndexChanged.connect(self.curIndexChanged)

        # self.edit_1 = qtw.QLineEdit()
        # self.edit_2 = qtw.QLineEdit()
        # self.edit_3 = qtw.QLineEdit()
        self.edit_4 = qtw.QLineEdit()
        self.edit_5 = qtw.QLineEdit()
        self.edit_5.setDisabled(True)
        # self.edit_6 = qtw.QLineEdit()
        self.edit_7 = qtw.QLineEdit()

        self.edit_8 = qtw.QLineEdit()
        self.edit_8.setDisabled(True)

        self.edit_9 = qtw.QLineEdit()

        self.comboBox_2.setDisabled(True)
        self.comboBox_21.setDisabled(True)

        self.comboBox_3.setDisabled(False)
        self.comboBox_31.setDisabled(False)

        self.comboBox_6.setDisabled(True)
        self.comboBox_61.setDisabled(True)

        self.data = []

        self.cancel_button = qtw.QPushButton('Cancel')
        self.submit_button = qtw.QPushButton('Submit')

        self.setLayout(qtw.QFormLayout())

        self.layout().addWidget(self.comboBox)

        self.combo_widget = qtw.QWidget()
        self.combo_widget.setLayout(qtw.QHBoxLayout())
        # self.combo_widget.layout().addWidget(qtw.QLabel('product_id '))
        self.combo_widget.layout().addWidget(self.comboBox_1)
        self.combo_widget.layout().addWidget(self.comboBox_11)
        self.layout().addRow('product_id ', self.combo_widget)
        # self.setLayout(layout)

        self.combo_widget2 = qtw.QWidget()
        self.combo_widget2.setLayout(qtw.QHBoxLayout())
        # self.combo_widget.layout().addWidget(qtw.QLabel('product_id '))
        self.combo_widget2.layout().addWidget(self.comboBox_2)
        self.combo_widget2.layout().addWidget(self.comboBox_21)
        self.layout().addRow('warehouse_from ', self.combo_widget2)

        self.combo_widget3 = qtw.QWidget()
        self.combo_widget3.setLayout(qtw.QHBoxLayout())
        # self.combo_widget.layout().addWidget(qtw.QLabel('product_id '))
        self.combo_widget3.layout().addWidget(self.comboBox_3)
        self.combo_widget3.layout().addWidget(self.comboBox_31)
        self.layout().addRow('warehouse_to ', self.combo_widget3)


        # self.layout().addRow('product_id                ', self.comboBox_1)  # INTEGER
        # self.layout().addRow('warehouse_from            ', self.comboBox_2)  # INTEGER
        # self.layout().addRow('warehouse_to              ', self.comboBox_3)  # INTEGER
        self.layout().addRow('quantity                  ', self.edit_4)  # INTEGER
        self.layout().addRow('transaction_date          ', self.edit_5)  # DATETIME

        # self.layout().addRow('customer_id               ', self.comboBox_6)  # INTEGER
        self.combo_widget6 = qtw.QWidget()
        self.combo_widget6.setLayout(qtw.QHBoxLayout())
        # self.combo_widget.layout().addWidget(qtw.QLabel('product_id '))
        self.combo_widget6.layout().addWidget(self.comboBox_6)
        self.combo_widget6.layout().addWidget(self.comboBox_61)
        self.layout().addRow('customer_id ', self.combo_widget6)


        self.layout().addRow('status                    ', self.edit_7)  # VARCHAR
        self.layout().addRow('employee_id               ', self.edit_8)  # INTEGER self.comboBox_8
        self.layout().addRow('product_experation_date   ', self.edit_9)  # INTEGER

        buttons = qtw.QWidget()
        buttons.setLayout(qtw.QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('', buttons)

        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)

        self.data = []
        # self.show()   # active when we run dialog as __main__

    def clicker(self, index):
        # Clear the second box
        self.comboBox_11.clear()
        # Do the dependant thing
        self.comboBox_11.addItems(self.comboBox_1.itemData(index))

    def clicker2(self, index):
        # Clear the second box
        self.comboBox_21.clear()
        # Do the dependant thing
        self.comboBox_21.addItems(self.comboBox_2.itemData(index))

    def clicker3(self, index):
        # Clear the second box
        self.comboBox_31.clear()
        # Do the dependant thing
        self.comboBox_31.addItems(self.comboBox_3.itemData(index))

    def clicker6(self, index):
        # Clear the second box
        self.comboBox_61.clear()
        # Do the dependant thing
        self.comboBox_61.addItems(self.comboBox_6.itemData(index))

    def curIndexChanged(self):
        if self.comboBox.currentIndex() == 0:
            self.comboBox_2.setDisabled(True)
            self.comboBox_21.setDisabled(True)
            self.comboBox_3.setDisabled(False)
            self.comboBox_31.setDisabled(False)
            self.comboBox_6.setDisabled(True)
            self.comboBox_61.setDisabled(True)
        if self.comboBox.currentIndex() == 1:
            self.comboBox_2.setDisabled(False)
            self.comboBox_21.setDisabled(False)
            self.comboBox_3.setDisabled(True)
            self.comboBox_31.setDisabled(True)
            self.comboBox_6.setDisabled(False)
            self.comboBox_61.setDisabled(False)
        if self.comboBox.currentIndex() == 2:
            self.comboBox_2.setDisabled(False)
            self.comboBox_21.setDisabled(False)
            self.comboBox_3.setDisabled(True)
            self.comboBox_31.setDisabled(True)
            self.comboBox_6.setDisabled(True)
            self.comboBox_61.setDisabled(True)
        if self.comboBox.currentIndex() == 3:
            self.comboBox_2.setDisabled(False)
            self.comboBox_21.setDisabled(False)
            self.comboBox_3.setDisabled(False)
            self.comboBox_31.setDisabled(False)
            self.comboBox_6.setDisabled(True)
            self.comboBox_61.setDisabled(True)


    def on_submit(self):
        self.data = []
        self.data.append(self.comboBox_11.currentText())
        self.data.append(self.comboBox_21.currentText())
        self.data.append(self.comboBox_31.currentText())
        self.data.append(self.edit_4.text())
        # self.data.append(self.edit_5.text())
        self.data.append(None)
        self.data.append(self.comboBox_61.currentText())
        self.data.append(self.edit_7.text())
        self.data.append(None)  # self.comboBox_8.currentText()
        if self.edit_9.text():
            self.data.append(self.edit_9.text())
        else:
            self.data.append(None)
        if self.comboBox.currentIndex() == 0:
            self.data[1] = None
            self.data[5] = None
        if self.comboBox.currentIndex() == 1:
            self.data[2] = None
        if self.comboBox.currentIndex() == 2:
            self.data[2] = None
            self.data[5] = None
        if self.comboBox.currentIndex() == 3:
            self.data[5] = None

        self.data.insert(0, self.comboBox.currentText())
        print(self.data)
        self.submitted.emit(
            self.data  # What you need
        )
        self.close()


# for example how to connect to get list
class MainWindow(qtw.QWidget):

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        self.resize(640, 480)
        # Main UI code goes here
        self.message_a = 'Hello'
        self.message_b = 'my friend'

        self.message_a_display = qtw.QLabel(
            text = self.message_a,
            font = qtg.QFont('Sans', 20)
        )
        self.message_b_display = qtw.QLabel(
            text = self.message_b,
            font = qtg.QFont('Sans', 20)
        )

        self.edit_button = qtw.QPushButton(
            'Edit',
            clicked=self.edit_messages
        )

        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(self.message_a_display)
        self.layout().addWidget(self.message_b_display)
        self.layout().addWidget(self.edit_button)

        # End main UI code
        self.show()
        self.data_from_outside = []

    @qtc.pyqtSlot(list)
    def update_data(self, data):
        self.data_from_outside = data  # What you need!!!!!!!!!!!
        print('Data from outside: ')
        print(self.data_from_outside)

    def edit_messages(self):
        self.dialog = DialogWindow()
        self.dialog.submitted.connect(self.update_data)
        self.dialog.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # mw =  DialogWindow()
    mw = MainWindow()
    sys.exit(app.exec())



