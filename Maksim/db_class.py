import sqlite3
import os
import random
from faker import Faker
from datetime import datetime, timedelta
import re


class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.faker = Faker()
        
    
    def create_database(self):
        with self.connection:
            self.connection.execute('''CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY,
                product_name VARCHAR(50) NOT NULL,
                category VARCHAR(50) NOT NULL,
                sku VARCHAR(100) UNIQUE NOT NULL,
                employee_id INTEGER NOT NULL,
                unit_of_measurement VARCHAR(50) NOT NULL,
                image_path VARCHAR(255),
                price FLOAT NOT NULL,
                description VARCHAR(1000),
                FOREIGN KEY (employee_id) REFERENCES Employees(id)
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS Stock (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                warehouse_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                expiration_date DATE,
                FOREIGN KEY (product_id) REFERENCES Products(id),
                FOREIGN KEY (warehouse_id) REFERENCES Warehouses(id)
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS Warehouses (
                id INTEGER PRIMARY KEY,
                warehouse_name VARCHAR(50) NOT NULL,
                warehouse_address VARCHAR(100) UNIQUE NOT NULL,
                geolocation_text VARCHAR(255),
                coords VARCHAR(255) UNIQUE NOT NULL
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS Transactions_history (
                id INTEGER PRIMARY KEY,
                transaction_type VARCHAR(50) NOT NULL,
                product_id INTEGER NOT NULL,
                warehouse_from INTEGER,
                warehouse_to INTEGER,
                quantity INTEGER NOT NULL,
                transaction_date DATETIME NOT NULL DEFAULT (CURRENT_TIMESTAMP),
                customer_id INTEGER,
                status VARCHAR(50) NOT NULL,
                employee_id INTEGER NOT NULL,
                product_experation_date DATE,
                FOREIGN KEY (product_id) REFERENCES Products(id),
                FOREIGN KEY (warehouse_from) REFERENCES Warehouses(id),
                FOREIGN KEY (warehouse_to) REFERENCES Warehouses(id),
                FOREIGN KEY (customer_id) REFERENCES Customers(id),
                FOREIGN KEY (employee_id) REFERENCES Employees(id)
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS Transactions_Items (
                id INTEGER PRIMARY KEY,
                transactions_history_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price FLOAT NOT NULL,
                FOREIGN KEY (transactions_history_id) REFERENCES Transactions_history(id),
                FOREIGN KEY (product_id) REFERENCES Products(id)
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS Customers (
                id INTEGER PRIMARY KEY,
                cust_first_name VARCHAR(50) NOT NULL,
                cust_last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) UNIQUE NOT NULL,
                cust_address VARCHAR(100) UNIQUE NOT NULL
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS Employees (
                id INTEGER PRIMARY KEY,
                empl_first_name VARCHAR(50) NOT NULL,
                empl_last_name VARCHAR(50) NOT NULL,
                login VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) UNIQUE NOT NULL,
                super_admin VARCHAR(50) NOT NULL
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS documents_type (
                id INTEGER PRIMARY KEY,
                document_name VARCHAR(50) NOT NULL,
                type VARCHAR(50) NOT NULL
            )''')

            print(f"База данных {self.db_file} создана.")

    def delete_database(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
            print(f"База данных {self.db_file} удалена.")
        else:
            print(f"База данных {self.db_file} не существует.")

    def create_super_admin(self, first_name, last_name, login, password):
        with sqlite3.connect(self.db_file) as connection:
            connection.execute('''INSERT INTO Employees (empl_first_name, empl_last_name, login, password, super_admin)
                                  VALUES (?, ?, ?, ?, ?)''', (first_name, last_name, login, password, 'super'))
            print(f"Суперадмин {first_name} {last_name} создан.")

    def populate_database(self):
        with self.connection:
            # Генерация данных для таблицы Warehouses
            warehouse_data = [
                (self.faker.company(), self.faker.address(), self.faker.sentence(), f"{self.faker.latitude()}, {self.faker.longitude()}")
                for _ in range(2)
            ]
            self.connection.executemany('''INSERT INTO Warehouses (warehouse_name, warehouse_address, geolocation_text, coords)
                                        VALUES (?, ?, ?, ?)''', warehouse_data)

            # Генерация данных для таблицы Products
            categories = ["Electronics", "Furniture", "Groceries", "Clothing", "Books"]
            unit_of_measurements = ["kg", "liters", "units", "packs"]
            products_data = [
                (self.faker.word(), random.choice(categories), self.faker.uuid4(), 1, random.choice(unit_of_measurements), None, round(random.uniform(10, 500), 2), self.faker.text(max_nb_chars=200))
                for _ in range(10)
            ]
            self.connection.executemany('''INSERT INTO Products (product_name, category, sku, employee_id, unit_of_measurement, image_path, price, description)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', products_data)

            # Генерация данных для таблицы Stock
            stock_data = [
                (i+1, random.randint(1, 2), random.randint(50, 200), (datetime.now() + timedelta(days=random.randint(0, 365))).date() if random.choice([True, False]) else None)
                for i in range(10)
            ]
            self.connection.executemany('''INSERT INTO Stock (product_id, warehouse_id, quantity, expiration_date)
                                        VALUES (?, ?, ?, ?)''', stock_data)

            # Генерация данных для таблицы Customers
            customers_data = [
                (self.faker.first_name(), self.faker.last_name(), self.faker.email(), self.faker.phone_number(), self.faker.address())
                for _ in range(5)
            ]
            self.connection.executemany('''INSERT INTO Customers (cust_first_name, cust_last_name, email, phone, cust_address)
                                        VALUES (?, ?, ?, ?, ?)''', customers_data)
            
            # Генерация данных для таблицы Transactions_history
            transaction_types = ["Приемка", "Продажа", "Списание", "Перемещение"]
            statuses = ["completed", "pending", "canceled"]
            
            transactions_data = []
            for _ in range(10):
                transaction_type = random.choice(transaction_types)
                product_id = random.randint(1, 10)
                warehouse_from = random.randint(1, 2) if transaction_type == "Перемещение" else None
                warehouse_to = random.randint(1, 2) if transaction_type in ["Перемещение", "Приемка"] else None
                quantity = random.randint(1, 50)
                transaction_date = self.faker.date_time_between(start_date='-1y', end_date='now')
                customer_id = random.randint(1, 5) if transaction_type == "Продажа" else None
                status = random.choice(statuses)
                employee_id = 1  # Предполагается, что существует администратор с id=1
                product_experation_date = (datetime.now() + timedelta(days=random.randint(0, 365))).date() if random.choice([True, False]) else None

                transactions_data.append((
                    transaction_type,
                    product_id,
                    warehouse_from,
                    warehouse_to,
                    quantity,
                    transaction_date,
                    customer_id,
                    status,
                    employee_id,
                    product_experation_date
                ))
            
            self.connection.executemany('''INSERT INTO Transactions_history 
                                        (transaction_type, product_id, warehouse_from, warehouse_to, quantity, transaction_date, customer_id, status, employee_id, product_experation_date)
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', transactions_data)

            print("База данных успешно заполнена случайными данными.")


        
    def validate_data(self, table_name: str, data: dict) -> tuple[bool, str]:
        """
        Метод для валидации данных перед добавлением в базу данных.
        
        :param table_name: Название таблицы ('Products', 'Stock', 'Warehouses', 'Transactions_history', 'Transactions_Items', 'Customers', 'Employees', 'documents_type')
        :param data: Словарь с данными для валидации
        :return: Возвращает True, если данные валидны, иначе False и сообщение об ошибке.
        """
        validation_rules = {
            'Products': {
                'product_name': str,
                'category': str,
                'sku': str,
                'employee_id': str,
                'unit_of_measurement': str,
                'image_path': str,
                'price': float,
                'description': str,
            },
            'Stock': {
                'product_id': int,
                'warehouse_id': int,
                'quantity': int,
                'expiration_date': str
            },
            'Warehouses': {
                'warehouse_name': str,
                'warehouse_address': str,
                'geolocation_text': str,
                'coords': str
            },
            'Transactions_history': {
                'transaction_type': str,
                'product_id': int,
                'warehouse_from': (int, type(None)),
                'warehouse_to': (int, type(None)),
                'quantity': int,
                'transaction_date': str,
                'customer_id': (int, type(None)),
                'status': str,
                'employee_id': str,
                'product_experation_date': str
            },
            'Transactions_Items': {
                'transactions_history_id': int,
                'product_id': int,
                'quantity': int,
                'price': float,
            },
            'Customers': {
                'cust_first_name': str,
                'cust_last_name': str,
                'email': str,
                'phone': str,
                'cust_address': str
            },
            'Employees': {
                'empl_first_name': str,
                'empl_last_name': str,
                'login': str,
                'password': str,
                'super_admin': str,
            },
            'documents_type': {
                'document_name': str,
                'type': str,
            }
        }

        if table_name not in validation_rules:
            raise ValueError(f"No validation rules defined for table {table_name}")

        rules = validation_rules[table_name]

        for field, expected_type in rules.items():
            if field not in data:
                return False, f"Missing required field: {field}"

            if isinstance(data[field], str):
                # Проверка строковых полей
                if expected_type == str and field != 'employee_id':
                    # Проверка на то, что строка не состоит только из цифр
                    if data[field].isdigit():
                        return False, f"Field '{field}' should not be a number as a string. Found: {data[field]}"
                try:
                    # Попытка преобразовать строку в числовое значение, если это ожидается
                    if expected_type == int:
                        data[field] = int(data[field])
                    elif expected_type == float:
                        data[field] = float(data[field])
                except ValueError:
                    return False, f"Field '{field}' should be of type {expected_type.__name__}, but cannot be converted from string."
            elif not isinstance(data[field], expected_type) and not (expected_type == (int, type(None)) and data[field] is None):
                return False, f"Field '{field}' type error, got {type(data[field]).__name__}"

            if field == 'email' and not self.is_valid_email(data[field]):
                return False, f"Invalid email format: {data[field]}"
            if field == 'phone' and not self.is_valid_phone(data[field]):
                return False, f"Invalid phone number format: {data[field]}"
            if field == 'expiration_date':
                if data[field] and not self.is_valid_date(data[field]):
                    return False, f"Invalid date format for 'expiration_date'. Expected format: YYYY-MM-DD"
            if field == 'transaction_date':
                if not self.is_valid_datetime(data[field]):
                    return False, f"Invalid date-time format for 'transaction_date'. Expected format: YYYY-MM-DD HH:MM:SS"
            if field == 'coords':
                if not self.is_valid_coords(data[field]):
                    return False, f"Invalid format for 'coords'. Expected format: 'latitude longitude' with numeric values."

        return True, "Data is valid"

    def is_valid_email(self, email: str) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def is_valid_phone(self, phone: str) -> bool:
        return re.match(r"^\+?[1-9]\d{1,14}$", phone) is not None

    def is_valid_date(self, date_str: str) -> bool:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def is_valid_datetime(self, datetime_str: str) -> bool:
        try:
            datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

    def is_valid_coords(self, coords: str) -> bool:
        return re.match(r'^\d+(\.\d+)? \d+(\.\d+)?$', coords) is not None


if __name__ == "__main__":
    db = DatabaseManager("store_database.db")
    db.create_database()
    db.create_super_admin("Admin", "Super", "admin_login", "3ef892b184bd162b6261e2dd77e31af8")
    db.populate_database()
