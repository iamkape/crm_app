import os
from PyQt5 import QtWidgets, QtGui, QtCore
import sqlite3
from .db_class import DatabaseManager

class AddProductDialog(QtWidgets.QDialog):
    def __init__(self, existing_data=None, manager_id=None):
        super().__init__()
        self.db = DatabaseManager('My/store_database.db')
        self.manager_id = manager_id
        self.existing_data = existing_data
        print("Existing data:", self.existing_data)
        self.connection = sqlite3.connect('My/store_database.db')

        self.setWindowTitle("Добавление товара")
        self.resize(600, 700)

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(20, 20, 20, 20)
        self.vertical_layout.setSpacing(10)

        self.line_edits = {}
        self.setup_ui()

        self.alert_msg = QtWidgets.QMessageBox()
        self.alert_msg.setWindowTitle('Information')
        self.alert_msg.setText('Are you sure you want to delete this product?')
        self.alert_msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.alert_msg.setIcon(QtWidgets.QMessageBox.Warning)

    def setup_ui(self):
        with self.connection:
            columns = self.connection.execute('PRAGMA table_info(Products)').fetchall()
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
                self.form_layout.addRow(label, line_edit)

            self.vertical_layout.addLayout(self.form_layout)

            self.image_label = QtWidgets.QLabel(self)
            self.image_label.setFixedSize(565, 400)
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)
            self.vertical_layout.addWidget(self.image_label)

            if self.existing_data:
                for i, col_name in enumerate(self.column_names):
                    if col_name == 'id' or col_name == 'employee_id':
                        continue
                    if i < len(self.existing_data):
                        self.line_edits[col_name].setText(self.existing_data[i])
                self.display_image(self.existing_data[self.column_names.index('image_path')])

        self.message_area = QtWidgets.QPlainTextEdit(self)
        self.message_area.setReadOnly(True)
        self.vertical_layout.addWidget(self.message_area)

        self.button_layout = QtWidgets.QHBoxLayout()

        self.save_button = QtWidgets.QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_product)
        self.button_layout.addWidget(self.save_button)

        self.delete_button = QtWidgets.QPushButton("Delete", self)
        self.delete_button.setEnabled(bool(self.existing_data))
        self.delete_button.clicked.connect(self.delete_product)
        self.button_layout.addWidget(self.delete_button)

        self.close_button = QtWidgets.QPushButton("Close", self)
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)

        self.vertical_layout.addLayout(self.button_layout)

    def display_image(self, image_path):
        if image_path:
            absolute_image_path = os.path.join('My', 'image', image_path)
            if os.path.isfile(absolute_image_path):
                pixmap = QtGui.QPixmap(absolute_image_path)
                if not pixmap.isNull():
                    self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio))
                else:
                    self.image_label.setText("Image not loaded properly.")
            else:
                self.image_label.setText("Image file not found.")
        else:
            self.image_label.clear()

    def save_product(self):
        data = {col_name: self.line_edits[col_name].text() for col_name in self.column_names if col_name not in ['id', 'employee_id']}
        data['employee_id'] = self.manager_id

        valid, message = self.db.validate_data('Products', data)

        if not valid:
            self.message_area.setPlainText(message)
            return

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        values = tuple(data.values())

        try:
            with self.connection:
                if self.existing_data:
                    product_id = self.existing_data[0]
                    update_query = f"UPDATE Products SET {', '.join([f'{col} = ?' for col in data.keys()])} WHERE id = ?"
                    self.connection.execute(update_query, values + (product_id,))
                else:
                    insert_query = f"INSERT INTO Products ({columns}) VALUES ({placeholders})"
                    self.connection.execute(insert_query, values)
            self.message_area.setPlainText("Completed successfully")
            self.display_image(data.get('image_path', ''))
        except Exception as e:
            self.message_area.setPlainText(f"Failed to add/update product: {e}")

    def delete_product(self):
        self.alert_msg.setText('Are you sure you want to delete this product?')
        result = self.alert_msg.exec_()
        if result == QtWidgets.QMessageBox.Ok:
            try:
                product_id = self.existing_data[0]
                with self.connection:
                    self.connection.execute("DELETE FROM Products WHERE id = ?", (product_id,))
                self.message_area.setPlainText("Product deleted successfully")
                self.close()
            except Exception as e:
                self.message_area.setPlainText(f"Failed to delete product: {e}")
