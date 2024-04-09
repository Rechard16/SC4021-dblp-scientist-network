from lxml import etree

def count_dblpperson_tags(xml_file):
    dblpperson_count = 0
    for event, element in etree.iterparse(xml_file, events=("start",), tag="dblpperson"):
        dblpperson_count += 1
        # It's good practice to clear the element to free up memory
        element.clear()

    return dblpperson_count

# Replace 'path_to_xml_file.xml' with the path to your XML file
file_path = 'C:\Users\yixia\Documents\Code\dblp-scientist-network\combined.xml'
print(f"The number of <dblpperson> tags is: {count_dblpperson_tags(file_path)}")
