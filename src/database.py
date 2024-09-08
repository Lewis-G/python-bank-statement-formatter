import sqlite3

class DatabaseClient:
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

    def select(self, columns_input:list=None, order_by:list=None, 
               where_categories:list=None, where_dates:list=None, where_cents:list=None):
        """Specify columns to select.

        Args:
            columns_input (list, optional): _description_. If no parameter is provided, all columns are selected.
            order_by (list, optional): _description_. The order of keys in the list determine the ordering rank.
        """
        
        columns = "*"
        if columns_input:
            columns = ", ".join(columns_input)
        
        select_str = f'''SELECT {columns} FROM Transactions'''
        has_where_conditions = False
        
        if where_categories:
            has_where_conditions = True
            select_str += f" WHERE Category IN ({", ".join([f'"{value}"' for value in where_categories])})"
            
        if where_dates:
            where_dates_str = f"Date > '{where_dates[0]}' AND Date < '{where_dates[1]}'"
            if has_where_conditions:
                select_str += f" AND {where_dates_str}"
            else:
                select_str += f" WHERE {where_dates_str}"
            has_where_conditions = True
        
        if where_cents:
            where_cents_str = f"Cents > {where_cents[0]} AND Cents < {where_cents[1]}"
            if has_where_conditions:
                select_str += f" AND {where_cents_str}"
            else:
                select_str += f" WHERE {where_cents_str}"
        
        if order_by:
            order_by_str = ''
            for i in range(len(order_by)):
                order_by_str += f"{order_by[i]["Name"]} {order_by[i]["Direction"]}, "
            
            order_by_str = order_by_str[:-2]
            select_str += f" ORDER BY {order_by_str}"
        
        select_str += ";"
        # print(select_str)
        self._cursor.execute(select_str)
        result = self._cursor.fetchall()
        return result
    
    def select_sum_cents(self):
        self._cursor.execute('''SELECT Category, SUM(Cents) AS TotalValue
                             FROM Transactions
                             GROUP BY Category;
                             ''')
        result = self._cursor.fetchall()
        return result
        # output example - [('ATO Credit', -13591), ('Eating out/Take-away', 5526), ('Medical', -812)]
    
    def close(self):
        self._connection.close()