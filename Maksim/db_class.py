import sqlite3
import os
import random
from faker import Faker
from datetime import datetime, timedelta


class DatabaseManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.faker = Faker()
        
    
    def create_database(self):
        with self.connection:
            self.connection.execute('''CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                category VARCHAR(50) NOT NULL,
                sku VARCHAR(100) UNIQUE NOT NULL,
                employee_id INTEGER NOT NULL,
                unit_of_measurement VARCHAR(50) NOT NULL,
                image_path BLOB,
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
                name VARCHAR(50) NOT NULL,
                address VARCHAR(100) UNIQUE NOT NULL,
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
                transaction_date DATETIME NOT NULL,
                customer_id INTEGER,
                status VARCHAR(50) NOT NULL,
                employee_id INTEGER NOT NULL,
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
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                phone VARCHAR(20) UNIQUE NOT NULL,
                address VARCHAR(100) UNIQUE NOT NULL
            )''')

            self.connection.execute('''CREATE TABLE IF NOT EXISTS Employees (
                id INTEGER PRIMARY KEY,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
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
            connection.execute('''INSERT INTO Employees (first_name, last_name, login, password, super_admin)
                                  VALUES (?, ?, ?, ?, ?)''', (first_name, last_name, login, password, 'super'))
            print(f"Суперадмин {first_name} {last_name} создан.")

    def populate_database(self):
        with self.connection:
            # Генерация данных для таблицы Warehouses
            warehouse_data = [
                (self.faker.company(), self.faker.address(), self.faker.sentence(), f"{self.faker.latitude()}, {self.faker.longitude()}")
                for _ in range(2)
            ]
            self.connection.executemany('''INSERT INTO Warehouses (name, address, geolocation_text, coords)
                                           VALUES (?, ?, ?, ?)''', warehouse_data)

            # Генерация данных для таблицы Products
            categories = ["Electronics", "Furniture", "Groceries", "Clothing", "Books"]
            unit_of_measurements = ["kg", "liters", "units", "packs"]
            products_data = [
                (self.faker.word(), random.choice(categories), self.faker.uuid4(), 1, random.choice(unit_of_measurements), None, round(random.uniform(10, 500), 2), self.faker.text(max_nb_chars=200))
                for _ in range(10)
            ]
            self.connection.executemany('''INSERT INTO Products (name, category, sku, employee_id, unit_of_measurement, image_path, price, description)
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
            self.connection.executemany('''INSERT INTO Customers (first_name, last_name, email, phone, address)
                                           VALUES (?, ?, ?, ?, ?)''', customers_data)

            print("База данных успешно заполнена случайными данными.")


if __name__ == "__main__":
    db = DatabaseManager("store_database.db")
    db.create_database()
    db.create_super_admin("Admin", "Super", "admin_login", "3ef892b184bd162b6261e2dd77e31af8")
    db.populate_database()
