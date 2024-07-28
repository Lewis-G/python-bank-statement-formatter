class BankCategory:
    
    def __init__(self, category_name, keyword_array=None):
        if keyword_array is None:
            keyword_array = []
        
        self._category_name: str = category_name
        self._keyword_array: list|None = keyword_array
        self._total_value: int = 0
        
        self._transactions_list = ""

    def compare_to_keywords(self, input_string):
        for keyword in self._keyword_array:
            if keyword in input_string:
                return True
        return False

    def add_to_list_and_value(self, date, value, data):
        self._transactions_list += f"Date: {date} , Value: ${value}, Description: {data}\n"
        self._total_value += value

    @property
    def category_name(self):
        return self._category_name

    @property
    def category_keywords(self):
        return self._keyword_array

    @property
    def total_value(self):
        return self._total_value

    @property
    def transactions_list(self):
        return self._transactions_list
