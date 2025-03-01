import re
import sys

def is_valid_link(link):
    required_elements = ["http", "www", ".com"]
    return all(element in link for element in required_elements)

def extract_links(content, levels, current_level=0):
    if current_level > levels:
        return []

    bookmarks = []
    link_pattern = re.compile(r'<DT><A HREF="[^"]+" ADD_DATE="\d+"(?: ICON="[^"]+")?(?: DESCRIPTION="[^"]*")?>[^<]+<\/A>')
    nested_pattern = re.compile(r'<DT><H3 ADD_DATE="\d+"(?: LAST_MODIFIED="\d+")?(?: PERSONAL_TOOLBAR_FOLDER="true")?>([^<]+)<\/H3>\s*<DL><p>(.*?)<\/DL><p>', re.DOTALL)

    for match in link_pattern.finditer(content):
        link = match.group()
        if is_valid_link(link):
            bookmarks.append(link)

    for match in nested_pattern.finditer(content):
        section_title = match.group(1)
        nested_content = match.group(2)
        bookmarks.append(f'<DT><H3>{section_title}</H3>')
        bookmarks += extract_links(nested_content, levels, current_level + 1)

    return bookmarks

def flatten_bookmarks(file_path, levels):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    flat_bookmarks = extract_links(content, levels)
    flat_content = '<DL><p>\n' + '\n'.join(flat_bookmarks) + '\n</DL><p>'

    with open('flattened_bookmarks.html', 'w', encoding='utf-8') as file:
        file.write(flat_content)

    print(f"Bookmarks flattened to {levels} levels and saved to 'flattened_bookmarks.html'")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flatten_bookmarks.py <file_path> <levels>")
        sys.exit(1)

    input_file = sys.argv[1]
    levels = int(sys.argv[2])
    flatten_bookmarks(input_file, levels)
