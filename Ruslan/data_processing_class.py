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
        if resp is None:
            return None
        else:
            return resp[0]

    def remove_from_warehouse(self):
        with self.con:
            try:
                self.con.execute('BEGIN')
                self.con.execute(f'''UPDATE Stock SET quantity = "{self.quantity_in_w1 - self.quantity}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"
                ''')
                self.con.execute('COMMIT')
            except sqlite3.Error:
                self.con.execute('ROLLBACK')

    def add_to_warehouse(self):
        with self.con:
            try:
                self.con.execute('BEGIN')
                self.con.execute(f'''UPDATE Stock SET quantity = "{self.quantity + self.quantity_in_w1}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"
                ''')
                self.con.execute('COMMIT')
            except sqlite3.Error:
                self.con.execute('ROLLBACK')

    def movement_from_warehouse(self):
        with self.con:
            try:
                self.con.execute('BEGIN')
                self.con.execute(f'''UPDATE Stock SET quantity = "{self.quantity_in_w1 - self.quantity}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"
                                        
                ''')
                self.con.execute(f'''UPDATE Stock SET quantity = "{self.quantity + self.quantity_in_w2}"
                                      WHERE product_id = "{self.product_id}"
                                        AND warehouse_id = "{self.warehouse_from}"

                                ''')
                self.con.execute('COMMIT')
            except sqlite3.Error:
                self.con.execute('ROLLBACK')



test = DataProcessing([1, 'moving', 1, 1, None, 1, 2024-11-11, 1, 'сompleted', 1])
