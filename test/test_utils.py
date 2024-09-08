import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
src_dir = os.path.join(parent_dir, 'src')

sys.path.append(src_dir)
from database import DatabaseClient
from utils import format_rows_to_summary
from basic_file_utils import write_string_to_txt

db_path = f'{parent_dir}/transactions.db'

database = DatabaseClient(db_path)

columns = ["ID", "Date", "Cents", "Description", "Category"]

order_by_list = [
    {"Name": "Date", "Direction": "ASC"},
    {"Name": "Cents", "Direction": "ASC"},
    {"Name": "Description", "Direction": "ASC"},
    {"Name": "Category", "Direction": "ASC"}
]

where_categories_list = ["Medical", "Petrol"]
where_date_list = ["2019-01-15", "2025-01-15"]
where_cents_list = [0, 100000]

row_results = database.select(columns_input=columns, order_by=order_by_list, 
                where_categories=where_categories_list, where_dates=where_date_list,
                where_cents=where_cents_list)

summary = format_rows_to_summary(row_results)
print(summary)