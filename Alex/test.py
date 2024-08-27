import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class DialogWindow(qtw.QWidget):

    submitted = qtc.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.resize(600, 300)

        self.comboBox = qtw.QComboBox()
        self.comboBox.addItems(['acceptance', 'sale', 'write-off', 'movement'])

        self.comboBox.currentIndexChanged.connect(self.curIndexChanged)

        self.edit_1 = qtw.QLineEdit()
        self.edit_2 = qtw.QLineEdit()
        self.edit_3 = qtw.QLineEdit()
        self.edit_4 = qtw.QLineEdit()
        self.edit_5 = qtw.QLineEdit()
        self.edit_6 = qtw.QLineEdit()
        self.edit_7 = qtw.QLineEdit()
        self.edit_8 = qtw.QLineEdit()

        self.edit_2.setDisabled(True)
        self.edit_3.setDisabled(False)
        self.edit_6.setDisabled(True)

        self.data = []

        self.cancel_button = qtw.QPushButton('Cancel')
        self.submit_button = qtw.QPushButton('Submit')

        self.setLayout(qtw.QFormLayout())

        self.layout().addWidget(self.comboBox)

        self.layout().addRow('product_id                INTEGER  ', self.edit_1)
        self.layout().addRow('warehouse_from       INTEGER  ', self.edit_2)
        self.layout().addRow('warehouse_to           INTEGER  ', self.edit_3)
        self.layout().addRow('quantity                    INTEGER  ', self.edit_4)
        self.layout().addRow('transaction_date        DATETIME ', self.edit_5)
        self.layout().addRow('customer_id              INTEGER  ', self.edit_6)
        self.layout().addRow('status                       VARCHAR  ', self.edit_7)
        self.layout().addRow('employee_id              INTEGER  ', self.edit_8)

        buttons = qtw.QWidget()
        buttons.setLayout(qtw.QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('', buttons)

        self.submit_button.clicked.connect(self.on_submit)
        self.cancel_button.clicked.connect(self.close)

        self.data = []
        self.show()   # active when we run dialog as __main__


    def curIndexChanged(self):
        if self.comboBox.currentIndex() == 0:
            self.edit_2.setDisabled(True)
            self.edit_3.setDisabled(False)
            self.edit_6.setDisabled(True)
        if self.comboBox.currentIndex() == 1:
            self.edit_2.setDisabled(False)
            self.edit_3.setDisabled(True)
            self.edit_6.setDisabled(False)
        if self.comboBox.currentIndex() == 2:
            self.edit_2.setDisabled(False)
            self.edit_3.setDisabled(True)
            self.edit_6.setDisabled(True)
        if self.comboBox.currentIndex() == 3:
            self.edit_2.setDisabled(False)
            self.edit_3.setDisabled(False)
            self.edit_6.setDisabled(True)

    def on_submit(self):
        self.data = []
        self.data.append(self.edit_1.text())
        self.data.append(self.edit_2.text())
        self.data.append(self.edit_3.text())
        self.data.append(self.edit_4.text())
        self.data.append(self.edit_5.text())
        self.data.append(self.edit_6.text())
        self.data.append(self.edit_7.text())
        self.data.append(self.edit_8.text())
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
    mw =  DialogWindow()
    # mw = MainWindow()
    sys.exit(app.exec())


















