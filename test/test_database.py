import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
src_dir = os.path.join(parent_dir, 'src')

sys.path.append(src_dir)
from database import DatabaseUtils

db_path = f'{parent_dir}/transactions.db'

database = DatabaseUtils(db_path)

if (database.check_if_table_exists()):
    database.delete_all_rows()
else:
    database.create_table()

database.insert([1, "2020-01-01", 100, "Hello", "World"])

# print(database.select_all())

columns = ["ID", "Date", "Cents", "Description", "Category"]

order_by_list = [
    {"Name": "ID", "Direction": "ASC"},
    {"Name": "Date", "Direction": "ASC"},
    {"Name": "Cents", "Direction": "ASC"},
    {"Name": "Description", "Direction": "ASC"},
    {"Name": "Category", "Direction": "ASC"}
]

where_categories_list = ["World"]
where_date_list = ["2019-01-15", "2025-01-15"]
where_cents_list = [0, 100000]

result = database.select(columns_input=columns, order_by=order_by_list, 
                where_categories=where_categories_list, where_dates=where_date_list,
                where_cents=where_cents_list)

print(result)

database.close()