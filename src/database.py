import sqlite3

class DatabaseUtils:
    def __init__(self, db_path):
        self._connection = sqlite3.connect(db_path)
        self._cursor = self._connection.cursor()

    def create_table(self):
        self._cursor.execute('''CREATE TABLE Transactions
                            (ID INT PRIMARY KEY NOT NULL,
                            Date TEXT NOT NULL,
                            Cents INT NOT NULL,
                            Description TEXT NOT NULL,
                            Category TEXT);''')
        self._connection.commit()

    def check_if_table_exists(self):
        self._cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='Transactions';''')
        if not self._cursor.fetchone():
            return False
        else:
            return True
    
    def delete_all_rows(self):
        self._cursor.execute('''DELETE FROM Transactions;''')
        self._connection.commit()
    
    def insert(self, data:list):
        insert_str = 'INSERT INTO Transactions VALUES (?, ?, ?, ?, ?);'
        self._cursor.execute(insert_str, data)
        self._connection.commit()

    def select_all(self):
        self._cursor.execute('''SELECT * FROM Transactions;''')
        result = self._cursor.fetchall()
        return result

    def select(self, columns_input:list=None, order:dict=None):
        
        columns = "*"
        if columns_input:
            columns = ", ".join(columns)
        
        # Order determines the rank
        order_by = [
            {"Name": "ID", "Direction": "ASC"},
            {"Name": "Date", "Direction": "ASC"},
            {"Name": "Cents", "Direction": "ASC"},
            {"Name": "Description", "Direction": "ASC"},
            {"Name": "Category", "Direction": "ASC"}
        ]
        
        # Default?
        order_by_string = ''
        for item in enumerate(order_by):
            order_by_string += f"{item["Name"]}, {item["Direction"]} "
        order_by_string = order_by_string[:-1]

        select_str = f'''SELECT {columns} FROM Transactions
                        ORDER BY {order_by_string};'''
        
        
        # Where, date, value, category
        
    def close(self):
        self._connection.close()