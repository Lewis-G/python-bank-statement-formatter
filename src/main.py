import os
import sys
from typing import List
from basic_file_utils import read_csv_to_string, read_json_to_dict
from bank_category import BankCategory
from parse_csv import parse_csv_split_and_insert_into_db
from database import DatabaseUtils

# Create paths
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))

input_csv_path = f'{parent_dir}/input.csv'
input_json_categories_path = f'{parent_dir}/categories.json'
db_path = f'{parent_dir}/transactions.db'

transactions_input = ''
categories_dict: dict = {}

try:
    transactions_input = read_csv_to_string(input_csv_path)
except Exception as e:
    print(e)
    sys.exit(1)

try:
    categories_dict = read_json_to_dict(input_json_categories_path)
except Exception as e:
    print(e)
    sys.exit(1)

category_objects: List[BankCategory] = []
category_names = list(categories_dict.keys())

# Use category name and keywords to create category objects
for i in range(len(category_names)):
    category_objects.append(BankCategory(category_names[i], categories_dict[category_names[i]]))

# Add a final category for transactions that don't match any keywords
category_objects.append(BankCategory("Other"))

database = DatabaseUtils(db_path)
if (database.check_if_table_exists()):
    database.delete_all_rows()
else:
    database.create_table()

parse_csv_split_and_insert_into_db(transactions_input, category_objects, database)

