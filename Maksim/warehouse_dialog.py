from PyQt5 import QtWidgets
import sqlite3

class AddWarehouseDialog(QtWidgets.QDialog):
    def __init__(self, existing_data=None):
        super().__init__()
        self.existing_data = existing_data
        print("Existing data:", self.existing_data)
        self.connection = sqlite3.connect('My/store_database.db')

        self.setWindowTitle("Добавление склада")
        self.setFixedSize(500, 400)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(20, 20, 20, 20)
        self.vertical_layout.setSpacing(10)

        self.line_edits = {}
        self.setup_ui()

        self.alert_msg = QtWidgets.QMessageBox()
        self.alert_msg.setWindowTitle('Information')
        self.alert_msg.setText('Are you sure you want to delete this warehouse?')
        self.alert_msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.alert_msg.setIcon(QtWidgets.QMessageBox.Warning)

    def setup_ui(self):
        with self.connection:
            columns = self.connection.execute('PRAGMA table_info(Warehouses)').fetchall()
            self.column_names = [col[1] for col in columns]

            self.form_layout = QtWidgets.QFormLayout()
            self.form_layout.setContentsMargins(0, 0, 0, 0)
            self.form_layout.setSpacing(10)

            for col_name in self.column_names:
                if col_name == 'id':
                    continue 

                label = QtWidgets.QLabel(col_name.replace('_', ' ').capitalize(), self)
                line_edit = QtWidgets.QLineEdit(self)
                self.line_edits[col_name] = line_edit
                self.form_layout.addRow(label, line_edit)

            self.vertical_layout.addLayout(self.form_layout)

            if self.existing_data:
                for i, col_name in enumerate(self.column_names):
                    if col_name == 'id':
                        continue
                    if i < len(self.existing_data):
                        self.line_edits[col_name].setText(self.existing_data[i])

        self.message_area = QtWidgets.QPlainTextEdit(self)
        self.message_area.setReadOnly(True)
        self.vertical_layout.addWidget(self.message_area)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_warehouse)
        self.button_layout.addWidget(self.save_button)

        self.delete_button = QtWidgets.QPushButton("Delete", self)
        self.delete_button.setEnabled(bool(self.existing_data))
        self.delete_button.clicked.connect(self.delete_warehouse)
        self.button_layout.addWidget(self.delete_button)

        self.close_button = QtWidgets.QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

        self.vertical_layout.addLayout(self.button_layout)

    def save_warehouse(self):
        data = {col_name: self.line_edits[col_name].text() for col_name in self.column_names if col_name != 'id'}

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        values = tuple(data.values())

        try:
            with self.connection:
                if self.existing_data:
                    warehouse_id = self.existing_data[0]
                    update_query = f"UPDATE Warehouses SET {', '.join([f'{col} = ?' for col in data.keys()])} WHERE id = ?"
                    self.connection.execute(update_query, values + (warehouse_id,))
                else:
                    insert_query = f"INSERT INTO Warehouses ({columns}) VALUES ({placeholders})"
                    self.connection.execute(insert_query, values)
            self.message_area.setPlainText("Completed successfully")
        except Exception as e:
            self.message_area.setPlainText(f"Failed to add/update warehouse: {e}")

    def delete_warehouse(self):
        self.alert_msg.setText('Are you sure you want to delete this warehouse?')
        result = self.alert_msg.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            try:
                warehouse_id = self.existing_data[0]
                with self.connection:
                    self.connection.execute("DELETE FROM Warehouses WHERE id = ?", (warehouse_id,))
                self.message_area.setPlainText("Warehouse deleted successfully")
                self.close()
            except Exception as e:
                self.message_area.setPlainText(f"Failed to delete warehouse: {e}")
