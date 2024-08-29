import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
import sqlite3

class DialogWindow(qtw.QWidget):

    submitted = qtc.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.resize(400, 300)

        self.comboBox = qtw.QComboBox()
        self.comboBox.addItems(['acceptance', 'sale', 'write-off', 'movement'])

        self.con = sqlite3.connect('database/store_database.db')  #!!!!!!!!!!!!!!! Change path, please!!!!!!!!!!

        with self.con:
            table_data_product_id = self.con.execute("SELECT id FROM Products").fetchall()
            table_data_warehouse_id = self.con.execute("SELECT id FROM Warehouses").fetchall()
            table_data_customers_id = self.con.execute("SELECT id FROM Customers").fetchall()
            table_data_employees_id = self.con.execute("SELECT id FROM Employees").fetchall()
# product_id
        self.comboBox_1 = qtw.QComboBox()
        self.temp_list = []
        for item in table_data_product_id:
            self.temp_list.append(list(item)[0])
        self.temp_list.sort()
        for item in self.temp_list:
            self.comboBox_1.addItem(str(item))
        print(self.temp_list)
# Warehouse from
# Warehouse to
        self.comboBox_2 = qtw.QComboBox()
        self.comboBox_3 = qtw.QComboBox()
        self.temp_list = []
        for item in table_data_warehouse_id:
            self.temp_list.append(list(item)[0])
        self.temp_list.sort()
        for item in self.temp_list:
            self.comboBox_2.addItem(str(item))
            self.comboBox_3.addItem(str(item))
        print(self.temp_list)
# Customers
        self.comboBox_6 = qtw.QComboBox()
        self.temp_list = []
        for item in table_data_customers_id:
            self.temp_list.append(list(item)[0])
        self.temp_list.sort()
        for item in self.temp_list:
            self.comboBox_6.addItem(str(item))
        print(self.temp_list)
# Employees
        self.comboBox_8 = qtw.QComboBox()
        self.temp_list = []
        for item in table_data_employees_id:
            self.temp_list.append(list(item)[0])
        self.temp_list.sort()
        for item in self.temp_list:
            self.comboBox_8.addItem(str(item))
        print(self.temp_list)



        self.comboBox_1.setEditable(True)
        self.comboBox_2.setEditable(True)
        self.comboBox_3.setEditable(True)
        self.comboBox_6.setEditable(True)
        self.comboBox_8.setEditable(True)

        self.comboBox.currentIndexChanged.connect(self.curIndexChanged)

        # self.edit_1 = qtw.QLineEdit()
        # self.edit_2 = qtw.QLineEdit()
        # self.edit_3 = qtw.QLineEdit()
        self.edit_4 = qtw.QLineEdit()
        self.edit_5 = qtw.QLineEdit()
        # self.edit_6 = qtw.QLineEdit()
        self.edit_7 = qtw.QLineEdit()
        # self.edit_8 = qtw.QLineEdit()

        self.comboBox_2.setDisabled(True)
        self.comboBox_3.setDisabled(False)
        self.comboBox_6.setDisabled(True)

        self.data = []

        self.cancel_button = qtw.QPushButton('Cancel')
        self.submit_button = qtw.QPushButton('Submit')

        self.setLayout(qtw.QFormLayout())

        self.layout().addWidget(self.comboBox)

        self.layout().addRow('product_id             ', self.comboBox_1)  # INTEGER
        self.layout().addRow('warehouse_from         ', self.comboBox_2)  # INTEGER
        self.layout().addRow('warehouse_to           ', self.comboBox_3)  # INTEGER
        self.layout().addRow('quantity               ', self.edit_4)  # INTEGER
        self.layout().addRow('transaction_date       ', self.edit_5)  # DATETIME
        self.layout().addRow('customer_id            ', self.comboBox_6)  # INTEGER
        self.layout().addRow('status                 ', self.edit_7)  # VARCHAR
        self.layout().addRow('employee_id            ', self.comboBox_8)  # INTEGER

        buttons = qtw.QWidget()
        buttons.setLayout(qtw.QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('', buttons)

        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)

        self.data = []
        # self.show()   # active when we run dialog as __main__


    def curIndexChanged(self):
        if self.comboBox.currentIndex() == 0:
            self.comboBox_2.setDisabled(True)
            self.comboBox_3.setDisabled(False)
            self.comboBox_6.setDisabled(True)
        if self.comboBox.currentIndex() == 1:
            self.comboBox_2.setDisabled(False)
            self.comboBox_3.setDisabled(True)
            self.comboBox_6.setDisabled(False)
        if self.comboBox.currentIndex() == 2:
            self.comboBox_2.setDisabled(False)
            self.comboBox_3.setDisabled(True)
            self.comboBox_6.setDisabled(True)
        if self.comboBox.currentIndex() == 3:
            self.comboBox_2.setDisabled(False)
            self.comboBox_3.setDisabled(False)
            self.comboBox_6.setDisabled(True)
    def on_submit(self):
        self.data = []
        self.data.append(self.comboBox_1.currentText())
        self.data.append(self.comboBox_2.currentText())
        self.data.append(self.comboBox_3.currentText())
        self.data.append(self.edit_4.text())
        self.data.append(self.edit_5.text())
        self.data.append(self.comboBox_6.currentText())
        self.data.append(self.edit_7.text())
        self.data.append(self.comboBox_8.currentText())
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

