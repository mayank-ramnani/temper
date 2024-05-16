import requests
from bs4 import BeautifulSoup
import json
import re

OPENSSF_URL = "https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html"
DB_FILE = "db.json"

def extract_tables_from_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # find all <table> tags
        tables = soup.find_all('table')
        return tables
    else:
        print("Failed to fetch HTML content")
        return []

def table_to_dicts(table):
    # table headers
    headers = [header.get_text() for header in table.find_all('th')]
    # table rows
    rows = table.find_all('tr')[1:]  # Skip the header row
    # rows to dictionaries
    data = []
    for row in rows:
        row_data = []
        for cell in row.find_all('td'):
            for r in cell:
                if (r.string is None):
                    r.string = ' '
            row_data.append(cell.get_text())
        row_dict = dict(zip(headers, row_data))
        data.append(row_dict)
    return data

def convert_to_json(table_data):
    json_data = []
    for entry in table_data:
        # print(entry)
        # flags = entry['Compiler Flag'].split(' ')[1:]
        flags = [entry['Compiler Flag']]
        for flag in flags:
            json_entry = {
                    "opt": f"{flag}",
                    "desc": entry['Description'],
                    "requires": extract_versions(entry['Supported since'])
                    }
            json_data.append(json_entry)
    return json_data

def extract_versions(input_string):
    versions = {}

    # regular expressions to match GCC and Clang versions
    gcc_pattern = re.compile(r'GCC\s+(\d+\.\d+\.\d+)')
    clang_pattern = re.compile(r'Clang\s+(\d+\.\d+)')

    # GCC version
    gcc_match = gcc_pattern.search(input_string)
    if gcc_match:
        versions['gcc'] = gcc_match.group(1)

    # Clang version
    clang_match = clang_pattern.search(input_string)
    if clang_match:
        versions['clang'] = clang_match.group(1)

    return versions

tables = extract_tables_from_html(OPENSSF_URL)

# convert tables to array of dictionaries
# we only care about tables 1 and 2 for recommended options
tables_data = []
recommended_data = []
table_1 = table_to_dicts(tables[1])
table_2 = table_to_dicts(tables[2])

# merge entries
for entry in table_1:
    recommended_data.append(entry)

for entry in table_2:
    recommended_data.append(entry)

# convert table format to JSON format
json_data = convert_to_json(recommended_data)

with open(DB_FILE, "w") as fp:
    output_db = {"options": {"recommended": json_data}}
    json_formatted_str = json.dumps(output_db, indent=4)
    print("Write compiler options in json:", DB_FILE)
    # print(json_formatted_str)
    fp.write(json_formatted_str)
