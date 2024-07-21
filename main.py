import os
import sys
from typing import List
from input_output import read_csv_to_string, write_string_to_csv, read_json_to_dict
from bank_category import BankCategory

# Create paths
script_dir = os.path.dirname(os.path.abspath(__file__))
# useful: downloads_folder = os.path.join(script_dir, 'downloads')

input_path = f'{script_dir}/input.csv'
output_path = f'{script_dir}/output.csv'

try:
    csv_string = read_csv_to_string(input_path)
except Exception as e:
    print(e)
    sys.exit(1)

try:
    csv_string = read_json_to_dict(input_path)
except Exception as e:
    print(e)
    sys.exit(1)

categories: List[BankCategory] = []

for i in range(100):
    categories.append(BankCategory(f'number {i}'))
    
for i in range(100):
    print(categories[i].category_name)

write_string_to_csv(csv_string, output_path)
