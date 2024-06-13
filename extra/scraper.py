import requests
from bs4 import BeautifulSoup
import json
import re

OPENSSF_URL = "https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html"
DB_FILE = "scraped-db.json"

# returns a BeautifulSoup object on successful scraping, else None
def scrape_document(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print("Failed to fetch HTML content")
        return None

# assuming version is in the first paragraph element
def extract_version_from_soup(soup):
    subtitle = soup.find('p').get_text()
    version = ""
    date_pattern = r'\b\d{4}-\d{2}-\d{2}\b'
    if subtitle:
        match = re.search(date_pattern, subtitle)
        if match:
            date = match.group(0)
            return date
        else:
            print("No version date found in the subtitle of document.")
    else:
        print("No subtitle found in the document")

def extract_tables_from_soup(soup):
    # find all <table> tags
    tables = soup.find_all('table')
    return tables

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
            desc = entry['Description']
            prereq = ""
            # extract prerequisite content separately
            index = desc.find("Requires")
            if (index != -1):
                prereq = desc[index:]
                desc = desc[0:index]

            json_entry = {}
            json_entry["opt"] = flag
            json_entry["desc"] = desc
            if not (prereq == ""):
                json_entry["prereq"] = prereq
            json_entry["requires"] = extract_versions(entry['Supported since'])

            json_data.append(json_entry)
    return json_data

def extract_versions(input_string):
    versions = {}

    # regular expressions 
    # NOTE: the last version node is assumed to be single digit
    # if you need to support multiple digits, d+ can be added
    # however, it will start including the superscript references in the version number
    gcc_pattern = re.compile(r'GCC\s+(\d+\.\d+\.\d)')
    clang_pattern = re.compile(r'Clang\s+(\d+\.\d+\.\d)')
    binutils_pattern = re.compile(r'Binutils\s+(\d+\.\d+\.\d)')
    libcpp_pattern = re.compile(r'libc\+\+\s+(\d+\.\d+\.\d)')
    libstdcpp_pattern = re.compile(r'libstdc\+\+\s+(\d+\.\d+\.\d)')

    # GCC version
    gcc_match = gcc_pattern.search(input_string)
    if gcc_match:
        versions['gcc'] = gcc_match.group(1)

    # Clang version
    clang_match = clang_pattern.search(input_string)
    if clang_match:
        versions['clang'] = clang_match.group(1)

    # binutils version
    binutils_match = binutils_pattern.search(input_string)
    if binutils_match:
        versions['binutils'] = binutils_match.group(1)

    # libc++ version
    libcpp_match = libcpp_pattern.search(input_string)
    if libcpp_match:
        versions['libc++'] = libcpp_match.group(1)

    # libstdc++ version
    libstdcpp_match = libstdcpp_pattern.search(input_string)
    if libstdcpp_match:
        versions['libstdc++'] = libstdcpp_match.group(1)

    return versions

def main():
    soup = scrape_document(OPENSSF_URL)
    if (soup):
        # extract document version info
        version = extract_version_from_soup(soup)
        tables = extract_tables_from_soup(soup)

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
            output_db = {"version": version, "options": {"recommended": json_data}}
            json_formatted_str = json.dumps(output_db, indent=4)
            print("Write compiler options in json:", DB_FILE)
            # print(json_formatted_str)
            fp.write(json_formatted_str)


if __name__ == "__main__":
    main()
