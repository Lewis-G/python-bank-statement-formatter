import os
import sys
import pytest
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
src_dir = os.path.join(parent_dir, 'src')
sys.path.append(src_dir)

from database import DatabaseClient

@pytest.fixture(scope="module")
def database_client():
    # Before All
    db_path = f'{parent_dir}/transactions.db'
    client = DatabaseClient(db_path)

    if (client.check_if_table_exists()):
        client.delete_all_rows()
    else:
        client.create_table()
    
    yield client
    
    # After All
    client.close()
    
def test_insert_rows_exist(database_client:DatabaseClient):
    # Arrange
    input_data = [1, "2020-01-01", 100, "Hello", "World"]
    # Act
    database_client.insert(input_data)
    # Assert
    result = database_client.select_all()

def test_select_returns_valid_rows(database_client:DatabaseClient):

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

    result = database_client.select(columns_input=columns, order_by=order_by_list, 
                    where_categories=where_categories_list, where_dates=where_date_list,
                    where_cents=where_cents_list)

def test_select_sum_cents_is_valid(database_client:DatabaseClient):
    result = database_client.select_sum_cents()

def test_create_summary_text(database_client:DatabaseClient):
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

    row_results = database_client.select(columns_input=columns, order_by=order_by_list, 
                    where_categories=where_categories_list, where_dates=where_date_list,
                    where_cents=where_cents_list)

    row_results_by_category = defaultdict(list)

    for i in range(len(row_results)):
        tmp_date = f"{row_results[i][1]},"
        tmp_date = f"{tmp_date:<23}"
        
        tmp_cents_str = str(row_results[i][2])
        tmp_cents_str = f"{tmp_cents_str[:-2]}.{tmp_cents_str[-2:]},"
        tmp_cents_str = f"{tmp_cents_str:<19}"
        
        tmp_category_name = row_results[i][4]
        tmp_description = row_results[i][3]
        
        row_results_by_category[tmp_category_name].append(f"Date: {tmp_date} Dollars: ${tmp_cents_str} Description: {tmp_description}")

    database_client.close()

    for _category in row_results_by_category:
        print(f'{_category}:\n{'\n'.join(row_results_by_category[_category])}\n')