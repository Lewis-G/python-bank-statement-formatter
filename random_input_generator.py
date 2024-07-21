import random
import os
from datetime import datetime, timedelta
from input_output import write_string_to_csv

def generate_csv_data():
    
    categories = [
        {"Eating out/Take-away": ["Frank's pasta", "McPoyle Coffee", "Dennis' Pizza"]},
        {"Other Shopping": ["Amazon", "E-bay", "Facebook Marketplace"]},
        {"Utilities": ["Frank's Food N Stuff", "Dee's Groceries"]}, 
        {"Petrol": ["Charlie's petrol, Dee's gas", "Mac's car fuel"]}, 
        {"Tolls": ["Government E-toll"]}, 
        {"Medical": ["Dentist", "General practitioner", "Optometrist"]},  
    ]
    
    random_int_1 = random.randint(0, len(categories)-1)
    
    keys = [list(category.keys())[0] for category in categories]
    key = keys[random_int_1]
    
    sub_array_length = len(categories[random_int_1][key])
    random_int_2 = random.randint(0, sub_array_length-1)
    
    random_dollar_value = random.randint(0, random_int_1*30+random_int_2*5)
    random_dollar_value += random.randint(0, 99)/100
    
    return random_dollar_value, categories[random_int_1][key][random_int_2]

def format_date(date: datetime):
    return f'{date.day}/{date.month}/{date.year}'

csv_data = ""

now = datetime.now()
datetime_ptr = datetime(now.year-1, now.month, now.day)


for i in range(364):
    if (i % 7 == 0):
        csv_data += f'"{format_date(datetime_ptr)}", "$300", "Weekly rent"\n'
    if (i % 14 == 11):
        csv_data += f'"{format_date(datetime_ptr)}", "$2400", "Income payment"\n'
    
    for i in range(random.randint(0, 3)):
        temp_data = generate_csv_data()
        csv_data += f'"{format_date(datetime_ptr)}", "${temp_data[0]}", "{temp_data[1]}"\n'    
        
    datetime_ptr = datetime_ptr + timedelta(days=1)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = f'{script_dir}/random-input.csv'    
write_string_to_csv(csv_data, output_path)