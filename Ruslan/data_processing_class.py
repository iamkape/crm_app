import sqlite3


class DataProcessing:
    def __init__(self, data: list, file_db='../My/store_database.db'):
        self.con = sqlite3.connect(file_db)
        self.data = data
        self.transaction = data[1]
        self.product_id = data[2]
        self.quantity = data[5]
        self.warehouse_from = data[3]
        self.warehouse_to = data[4]
        self.quantity_in_w1 = self.get_quantity_in_warehouse(data[3])
        self.quantity_in_w2 = self.get_quantity_in_warehouse(data[4])

    def get_quantity_in_warehouse(self, warehouse_id: int = None) -> int | None:
        """Функция возвращает количество товара на выбранном складе (либо None если товар отсутствует)."""
        if warehouse_id is None:
            return None
        resp = self.con.execute(f'''
        SELECT quantity FROM Stock
        WHERE warehouse_id = "{warehouse_id}"
        AND product_id = "{self.product_id}"
        ''').fetchone()
        if resp is not None:
            return resp[0]

    def remove_from_warehouse(self) -> str:
        """Уменьшает количество товара на складе на N ед."""
        if (self.quantity_in_w1 is None) or (self.quantity_in_w1 - self.quantity < 0):
            return 'Exceeds the quantity of goods in warehouse'
        result = self.quantity_in_w1 - self.quantity
        with self.con:
            try:
                self.con.execute('BEGIN')
                self.con.execute(f'''UPDATE Stock SET quantity = "{result}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"
                ''')
                if result == 0:
                    self.con.execute(f'''DELETE FROM Stock
                                          WHERE product_id = "{self.product_id}"
                                            AND warehouse_id = "{self.warehouse_from}
                    ''')
                self.con.execute('COMMIT')

                return 'Operation completed successfully'
            except sqlite3.Error as err:
                self.con.execute('ROLLBACK')
                return f'Operation error: {err}'

    def add_to_warehouse(self) -> str:
        """Увеличивает количество товара на выбранном складе на N ед."""
        with self.con:
            try:
                self.con.execute('BEGIN')
                #if self.quantity_in_w1 is None:
                #    self.con.execute('''INSERT INTO Stock ''')
                self.con.execute(f'''UPDATE Stock SET quantity = "{self.quantity + self.quantity_in_w2}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"
                ''')
                self.con.execute('COMMIT')
                return 'Operation completed successfully'
            except sqlite3.Error as err:
                self.con.execute('ROLLBACK')
                return f'Operation error: {err}'
    def movement_from_warehouse(self):
        if (self.quantity_in_w1 is None) or (self.quantity_in_w1 - self.quantity < 0):
            return 'Exceeds the quantity of goods in warehouse'
        with self.con:
            try:
                difference = self.quantity_in_w1 - self.quantity
                self.con.execute('BEGIN')
                self.con.execute(f'''UPDATE Stock SET quantity = "{difference}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"
                                        
                ''')
                self.con.execute(f'''UPDATE Stock SET quantity = "{self.quantity + self.quantity_in_w2}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"

                                ''')
                if difference == 0:
                    self.con.execute(f'''DELETE FROM Stock
                                          WHERE product_id = "{self.product_id}"
                                            AND warehouse_id = "{self.warehouse_from}
                    ''')
                self.con.execute('COMMIT')
                return 'Operation completed successfully'
            except sqlite3.Error as err:
                self.con.execute('ROLLBACK')
                return f'Operation error: {err}'