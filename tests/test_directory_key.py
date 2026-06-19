# test_directory_key.py
# Spike: Generate a directory key mapping URL path abbreviations to
# their full names, derived from TOC URL/label pairs.
#
# The URL structure is:
#   02echorm/[chapter]/[section]/[filename].pdf
# The label structure is:
#   R.M. 2002::[Chapter]: [Section]: [Procedure] (Echo)
#
# This spike extracts all unique mappings and writes them to
# DIRECTORY_KEY.md in the project root.
#
# Expected result: a complete mapping of all chapter dirs, section
# dirs, and filenames to their human-readable equivalents.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

TOC_URL = "https://caphector.com/atoyota/TableOfContents/manual.html"
MAX_LABEL_LENGTH = 200  # ignore malformed labels

response = requests.get(TOC_URL)
soup = BeautifulSoup(response.text, "html.parser")

chapter_map = {}
section_map = {}
filename_map = {}

for a in soup.find_all("a", href=True):
    href = a["href"]
    if not href.endswith(".pdf"):
        continue

    label = a.get_text(strip=True)
    if len(label) > MAX_LABEL_LENGTH:
        continue

    url = urljoin(TOC_URL, href)
    match = re.search(r"02echorm/([^/]+)/([^/]+)/([^/]+)\.pdf", url)
    if not match:
        continue

    chapter_dir, section_dir, filename = match.groups()

    # Parse label: "R.M. 2002::Chapter: Section: Procedure (Echo)"
    label_clean = label.replace(" (Echo)", "").strip()
    parts = label_clean.split("::")
    if len(parts) < 2:
        continue
    content = parts[1].strip()
    content_parts = [p.strip() for p in content.split(":")]
    if len(content_parts) < 3:
        continue

    chapter_name, section_name, procedure_name = content_parts[0], content_parts[1], content_parts[2]

    chapter_map[chapter_dir] = chapter_name
    section_map[section_dir] = section_name
    filename_map[filename] = procedure_name

# Write DIRECTORY_KEY.md
lines = []
lines.append("# Directory Key")
lines.append("")
lines.append("Mapping of abbreviated directory and filename components in the `pdfs/` folder to their full names as used in the Toyota Echo Service Manual (RM884U).")
lines.append("")
lines.append("## Chapter Directories")
lines.append("")
lines.append("| Directory | Chapter Name |")
lines.append("|-----------|-------------|")
for k, v in sorted(chapter_map.items()):
    lines.append(f"| `{k}` | {v} |")

lines.append("")
lines.append("## Section Directories")
lines.append("")
lines.append("| Directory | Section Name |")
lines.append("|-----------|-------------|")
for k, v in sorted(section_map.items()):
    lines.append(f"| `{k}` | {v} |")

lines.append("")
lines.append("## Filenames")
lines.append("")
lines.append("| Filename | Procedure |")
lines.append("|----------|-----------|")
for k, v in sorted(filename_map.items()):
    lines.append(f"| `{k}.pdf` | {v} |")

output = "\n".join(lines)
with open("DIRECTORY_KEY.md", "w") as f:
    f.write(output)

print(f"Chapter directories:  {len(chapter_map)}")
print(f"Section directories:  {len(section_map)}")
print(f"Unique filenames:     {len(filename_map)}")
print("\nWritten to DIRECTORY_KEY.md")