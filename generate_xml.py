import csv
import requests
from lxml import etree

def fetch_xml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful requests
        return etree.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch XML from URL: {url}")
        print(f"Error: {e}")
        return None

def combine_xml(xml_list):
    root = etree.Element("combined")
    for xml in xml_list:
        root.append(xml)
    return root

def is_disambiguation(xml):
    person_element = xml.find(".//person")
    if person_element is not None:
        publtype = person_element.get("publtype")
        return publtype == "disambiguation"
    return False

# Read the CSV file and replace .html with .xml for each URL
urls = []
with open('Input\cleaned_url.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        url = row[0].replace('.html', '.xml')
        urls.append(url)

# Fetch XML data from each URL and remove disambiguation URLs
xml_list = []
removed_urls = []
for url in urls:
    xml = fetch_xml(url)
    if xml is not None:
        if is_disambiguation(xml):
            print(f"URL with disambiguation publtype: {url}")
            removed_urls.append(url)
        else:
            xml_list.append(xml)

# Combine the XML data
combined_xml = combine_xml(xml_list)

# Write the combined XML to a file
with open('combined.xml', 'wb') as file:
    file.write(etree.tostring(combined_xml, pretty_print=True))

print("Combined XML saved as combined.xml")

# Remove disambiguation URLs from the CSV file
with open('urls.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

with open('urls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in rows:
        url = row[0]
        if url.replace('.html', '.xml') not in removed_urls:
            writer.writerow(row)

print("Disambiguation URLs removed from urls.csv")
