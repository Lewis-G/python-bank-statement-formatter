import re
from bank_category import BankCategory
from database import DatabaseUtils

def parse_csv_split_and_insert_into_db(csv:str, category_objects:list[BankCategory], database:DatabaseUtils=None):
    
    csv_split = csv.split('\n')
    column_pattern = r'"(.*)", "(.*)", "(.*)"'

    for i in range(len(csv_split)):
        if (csv_split[i] == ""):
            break
        
        row_groups = re.match(column_pattern, csv_split[i])
        
        # Input date format must be: dd/mm/yyyy 
        date_dd_mm_yyyy = row_groups.group(1)
        date_groups = re.match(r"^(\d{1,2})/(\d{1,2})/(\d{4})$", date_dd_mm_yyyy)
        
        if not date_groups:
            print(f"""1st value of row {i} is invalid.
                        {row_groups.group(1), row_groups.group(2), row_groups.group(3)}
                    This row will be skipped\n""")
            continue
        
        # Reformat date
        date_yyyy_mm_dd = f"{date_groups.group(3)}/{(date_groups.group(2)):0>2}/{(date_groups.group(1)):0>2}"
        
        # Value format must be <Sequence of digits>.<2 digits>
        dollar_value = row_groups.group(2)
        if (re.search(r'^-?\d+\.\d{2}$', dollar_value) == None):
            print(f"""2nd value of row {i} is invalid.
                        {date_yyyy_mm_dd, row_groups.group(2), row_groups.group(3)}
                    This row will be skipped\n""")
            continue
        
        cent_value = int(dollar_value.replace(".", ""))
        
        text = row_groups.group(3)
        category_name = "Other"     # If there is no match, append category to 'Other'
        matched_keyword = False
        j = 0
        while (j < len(category_objects)-1) and matched_keyword == False:
            
            if (category_objects[j].compare_to_keywords(text)):
                matched_keyword = True
                category_name = category_objects[j].category_name
            j = j + 1
            
        database.insert([i, date_yyyy_mm_dd, cent_value, text, category_name])