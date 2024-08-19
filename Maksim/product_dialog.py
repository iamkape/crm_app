from PyQt5 import QtWidgets
import sqlite3

class AddProductDialog(QtWidgets.QDialog):
    def __init__(self, existing_data=None, manager_id=None):
        super().__init__()
        self.manager_id = manager_id
        self.existing_data = existing_data
        self.con = sqlite3.connect('My/store_database.db')

        self.setWindowTitle("Добавление товара")
        self.setFixedSize(500, 400)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(20, 20, 20, 20)
        self.vertical_layout.setSpacing(10)

        self.line_edits = {}
        self.setup_ui()

    def setup_ui(self):
        with self.con:
            cursor = self.con.execute('PRAGMA table_info(Products)')
            columns = cursor.fetchall()
            self.column_names = [col[1] for col in columns]

            self.form_layout = QtWidgets.QFormLayout()
            self.form_layout.setContentsMargins(0, 0, 0, 0)
            self.form_layout.setSpacing(10)

            for col_name in self.column_names:
                if col_name == 'id' or col_name == 'employee_id':
                    continue

                label = QtWidgets.QLabel(col_name.replace('_', ' ').capitalize(), self)
                line_edit = QtWidgets.QLineEdit(self)
                self.line_edits[col_name] = line_edit
                if self.existing_data and col_name in self.existing_data:
                    line_edit.setText(self.existing_data[col_name])
                self.form_layout.addRow(label, line_edit)

            self.vertical_layout.addLayout(self.form_layout)

        self.message_area = QtWidgets.QPlainTextEdit(self)
        self.message_area.setReadOnly(True)
        self.vertical_layout.addWidget(self.message_area)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_product)
        self.button_layout.addWidget(self.save_button)

        self.delete_button = QtWidgets.QPushButton("Delete", self)
        self.delete_button.setEnabled(False)
        self.button_layout.addWidget(self.delete_button)

        self.close_button = QtWidgets.QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

        self.vertical_layout.addLayout(self.button_layout)

    def save_product(self):
        data = {col_name: self.line_edits[col_name].text() for col_name in self.column_names if col_name not in ['id', 'employee_id']}
        data['employee_id'] = self.manager_id

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        values = tuple(data.values())

        try:
            with self.con:
                self.con.execute(f"INSERT INTO Products ({columns}) VALUES ({placeholders})", values)
            self.message_area.setPlainText("Completed successfully")
        except Exception as e:
            self.message_area.setPlainText(f"Failed to add product{e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = AddProductDialog(manager_id=1)
    dialog.show()
    sys.exit(app.exec_())
