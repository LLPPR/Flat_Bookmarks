import re

def flatten_bookmarks(file_path, levels):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract bookmarks with directory levels
    bookmark_pattern = r'((<DL><p>\n)+<DT><A HREF="[^"]+">[^<]+</A>(\n</DL><p>)+)'
    bookmarks = re.findall(bookmark_pattern, content)

    flat_bookmarks = []

    for bm in bookmarks:
        # Count the number of <DL> tags to determine the level
        level_count = bm[0].count('<DL><p>')
        if level_count <= levels:
            # Extract actual bookmark and add to flat list
            flat_bookmarks.append(re.search(r'<DT><A HREF="[^"]+">[^<]+</A>', bm[0]).group())

    flat_content = '<DL><p>\n' + '\n'.join(flat_bookmarks) + '\n</DL><p>'

    with open('flattened_bookmarks.html', 'w', encoding='utf-8') as file:
        file.write(flat_content)

    print(f"Bookmarks flattened to {levels} levels and saved to 'flattened_bookmarks.html'")

if __name__ == "__main__":
    input_file = input("Enter the path to your bookmarks HTML file: ")
    levels = int(input("Enter the number of directory levels to flatten to: "))
    flatten_bookmarks(input_file, levels)
