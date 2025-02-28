import re
import sys

def extract_links(content, levels, current_level=0):
    if current_level > levels:
        return []

    bookmarks = []
    link_pattern = re.compile(r'<DT><A HREF="[^"]+" ADD_DATE="\d+">[^<]+<\/A>')
    nested_pattern = re.compile(r'<DL><p>\s*<DT><H3 ADD_DATE="\d+" LAST_MODIFIED="\d+">[^<]+<\/H3>\s*<DL><p>(.*?)<\/DL><p>', re.DOTALL)

    for match in link_pattern.finditer(content):
        bookmarks.append(match.group())

    for match in nested_pattern.finditer(content):
        nested_content = match.group(1)
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
