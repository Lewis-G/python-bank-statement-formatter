pip install python-dateutil

Parse CSV and JSON, add categories to transactions and save to DB

TO DO: check if CSV is in valid format, do bank CSVs allow double quotes?
TO DO: check that all value data has a . with 2 decimal places, when importing
TO DO: improve column_pattern to assess double quotes within values

CSV format: Escaped double quotes are done with 2 consequitive double quotes
"This value has ""escaped"" quotes"

TO DO: Testable code?
TO DO: More edge case checks when parsing data