import sys
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QDialog
)

class Ui_Dialog3(QtWidgets.QDialog):
    def __init__(self, table_name):
        super().__init__()
        data_type = {'acceptance': ['INTEGER', 'INTEGER', 'INTEGER', 'DATETIME', 'VARCHAR(50)', 'INTEGER'],
          'sale': ['INTEGER', 'INTEGER', 'INTEGER', 'DATETIME', 'INTEGER', 'VARCHAR(50)', 'INTEGER'],
          'write-off': ['INTEGER','INTEGER','INTEGER','DATETIME','VARCHAR(50)','INTEGER'],
          'movement': ['INTEGER', 'INTEGER','INTEGER', 'INTEGER', 'DATETIME','VARCHAR(50)','INTEGER']}
        self.setObjectName("Dialog")
        self.resize(450, 0)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(40, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.columns_list = {
            'acceptance': ['product_id', 'warehouse_to', 'quantity', 'transaction_date', 'status', 'employee_id'],
            'sale': ['product_id', 'warehouse_from', 'quantity', 'transaction_date', 'customer_id', 'status',
                     'employee_id'],
            'write-off': ['product_id', 'warehouse_from', 'quantity', 'transaction_date', 'status', 'employee_id'],
            'movement': ['product_id', 'warehouse_from', 'warehouse_to', 'quantity', 'transaction_date', 'status',
                         'employee_id']}
        self.line_edits = []
        layout = QVBoxLayout()
        for i in range(len(self.columns_list[table_name])):
            h_layout = QHBoxLayout()
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Поле для ввода")
            self.line_edits.append(line_edit)
            label1 = QLabel(self.columns_list[table_name][i])
            label2 = QLabel(data_type[table_name][i])
            h_layout.addWidget(line_edit)
            h_layout.addWidget(label1)
            h_layout.addWidget(label2)
            h_layout.setAlignment(line_edit, Qt.AlignLeft)
            h_layout.setAlignment(label1, Qt.AlignLeft)
            h_layout.setAlignment(label2, Qt.AlignLeft)
            layout.addLayout(h_layout)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))

    def exec_(self):
        super().exec_()
        return [line.text() for line in self.line_edits]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("New transaction")

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        self.label = QLabel("Choose transaction")
        self.label.setGeometry(QtCore.QRect(50, 50, 100, 20))
        self.label.setStyleSheet("font: 75 12pt \"MS Shell Dlg 2\";")


        self.stacklayout.addWidget(self.label)


        btn = QPushButton("acceptance")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Ui_Dialog3('acceptance'))

        btn = QPushButton("sale")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Ui_Dialog3('sale'))

        btn = QPushButton("write-off")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Ui_Dialog3('write-off') )

        btn = QPushButton("movement")
        btn.pressed.connect(self.activate_tab_4)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Ui_Dialog3('movement'))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
        self.resp = []

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(1)
        self.resp = self.stacklayout.currentWidget().exec_()
        # self.stacklayout.currentWidget().close()
        if '' not in self.resp:
            self.resp.insert(0, 'acceptance')
            self.resp.insert(2, None)
            self.resp.insert(6, None)
            print(self.resp)
        self.close()

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(2)
        self.resp = self.stacklayout.currentWidget().exec_()
        if '' not in self.resp:
            self.resp.insert(0, 'sale')
            self.resp.insert(3, None)
            print(self.resp)
        self.close()

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(3)
        self.resp = self.stacklayout.currentWidget().exec_()
        if '' not in self.resp:
            self.resp.insert(0, 'write-off')
            self.resp.insert(3, None)
            self.resp.insert(6, None)
            print(self.resp)
        self.close()

    def activate_tab_4(self):
        self.stacklayout.setCurrentIndex(4)
        self.resp = self.stacklayout.currentWidget().exec_()
        if '' not in self.resp:
            self.resp.insert(0, 'movement')
            self.resp.insert(6, None)
            print(self.resp)
        self.close()

    def data(self):
        super().exec_()
        if '' not in self.resp:
            return self.resp


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
