import os
import sys
from typing import List
from basic_file_utils import read_csv_to_string, read_json_to_dict
from bank_category import BankCategory
import re

# Create paths
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))

input_csv_path = f'{parent_dir}/input.csv'
input_json_categories_path = f'{parent_dir}/categories.json'
output_path = f'{parent_dir}/output.txt'

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

output_string = ''

transactions_input = transactions_input.split('\n')

column_pattern = r'(".*"), (".*"), (".*")'

for i in range(len(transactions_input)):
    if (transactions_input[i] == ""):
        break
    
    row_groups = re.match(column_pattern, transactions_input[i])
    
    # Input date format must be: dd/mm/yyyy 
    date_dd_mm_yyyy = row_groups.group(1)[1:-1]
    date_groups = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date_dd_mm_yyyy)
    
    if not date_groups:
        print(f"""1st value of row {i} is invalid.
                    {row_groups.group(1), row_groups.group(2), row_groups.group(3)}
                This row will be skipped\n""")
        continue
    
    # Reformat date
    date_yyyy_mm_dd = f"{date_groups.group(3)}/{(date_groups.group(2)):0>2}/{(date_groups.group(1)):0>2}"
    
    # Value format must be <Sequence of digits>.<2 digits>
    dollar_value = row_groups.group(2)[2:-1]
    if (re.search(r'^\d+\.\d{2}$', dollar_value) == None):
        print(f"""2nd value of row {i} is invalid.
                    {date_yyyy_mm_dd, row_groups.group(2), row_groups.group(3)}
                This row will be skipped\n""")
        continue
    
    text = row_groups.group(3)
    
    matched_keyword = False
    j = 0
    while (j < len(category_objects)-1) and matched_keyword == False:
        
        if (category_objects[j].compare_to_keywords(text)):
            matched_keyword = True
        j = j + 1
    
            
