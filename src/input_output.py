import json

def read_csv_to_string(input_path):
    try:
        with open(input_path, mode='r', newline='', encoding='utf-8') as file:
            output_string = file.read()
        return output_string
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{input_path}' was not found.")
    except PermissionError:
        raise PermissionError(
            f"Permission denied to read the file '{input_path}'.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading the file '{
                        input_path}': {e}")

def read_json_to_dict(input_path):
    try:
        with open(input_path, mode='r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{input_path}' was not found.")
    except PermissionError:
        raise PermissionError(
            f"Permission denied to read the file '{input_path}'.")
    except json.JSONDecodeError:
        raise ValueError(f"The file '{input_path}' is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading the file '{
                        input_path}': {e}")

def write_string_to_txt(input_string, output_path):
    try:
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            file.write(input_string)
    except PermissionError:
        raise PermissionError(
            f"Permission denied to write to the file '{output_path}'.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while writing to the file '{
                        output_path}': {e}")
        

temp = 5