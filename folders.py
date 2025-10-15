
import os

# Path to your GitHub Pages folder
BASE_DIR = "cargotab.github.io"

# HTML template
html_start = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Folders Index</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 30px; }
        h1 { margin-bottom: 20px; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 8px 0; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
<h1>Available Folders</h1>
<ul>
"""

html_end = """
</ul>
</body>
</html>
"""

# Get all folders in BASE_DIR
folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]

# Generate list items
list_items = ""
for folder in folders:
    folder_path = os.path.join(folder, "index.html")
    list_items += f'    <li><a href="{folder_path}">{folder}</a></li>\n'

# Write to index.html
with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_start + list_items + html_end)

print("✅ index.html generated with all folders.")
