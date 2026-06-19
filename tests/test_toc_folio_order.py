# test_toc_folio_order.py
# Spike: Generate a full TOC listing in folio order for bookmark
# structure review.
#
# Combines folio numbers extracted from downloaded PDFs with label
# text from the TOC page, then outputs a structured Markdown document
# in folio order. Used to decide on bookmark nesting depth.
#
# Output: tests/output/test_toc_folio_order.md
#
# Expected result: 815 entries in folio order, grouped by chapter
# and section, formatted as readable Markdown.

import pdfplumber
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os

TOC_URL = "https://caphector.com/atoyota/TableOfContents/manual.html"
DOWNLOAD_DIR = "pdfs"
MAX_LABEL_LENGTH = 200

# Step 1: Scrape URLs and labels from TOC
print("Scraping TOC...")
response = requests.get(TOC_URL)
soup = BeautifulSoup(response.text, "html.parser")

url_to_label = {}
for a in soup.find_all("a", href=True):
    href = a["href"]
    if not href.endswith(".pdf"):
        continue
    url = urljoin(TOC_URL, href)
    label = a.get_text(strip=True)
    if len(label) <= MAX_LABEL_LENGTH:
        url_to_label[url] = label

print(f"  Found {len(url_to_label)} valid labels")

# Step 2: Build URL-to-local-path mapping
def url_to_local_path(url):
    match = re.search(r"02echorm/(.+)", url)
    if match:
        return os.path.join(DOWNLOAD_DIR, match.group(1))
    return None

# Step 3: Extract folio numbers from downloaded PDFs
print("Reading folio numbers from downloaded PDFs...")
entries = []
for url, label in url_to_label.items():
    local_path = url_to_local_path(url)
    if not local_path or not os.path.exists(local_path):
        continue
    try:
        with pdfplumber.open(local_path) as pdf:
            first_page = pdf.pages[0]
            page_height = first_page.height
            footer_region = first_page.crop(
                (0, page_height - 50, first_page.width, page_height)
            )
            footer_text = footer_region.extract_text()
            if footer_text:
                match = re.search(r"Date.*?(\d+)\s*$", footer_text, re.MULTILINE)
                if match:
                    folio_num = int(match.group(1))
                    # Also extract page number from header
                    header_region = first_page.crop((0, 0, first_page.width, 50))
                    header_text = header_region.extract_text()
                    page_num = header_text.split("\n")[0].strip() if header_text else "?"
                    # Parse label into parts
                    label_clean = label.replace(" (Echo)", "").strip()
                    parts = label_clean.split("::")
                    content = parts[1].strip() if len(parts) >= 2 else label_clean
                    content_parts = [p.strip() for p in content.split(":")]
                    entries.append((folio_num, page_num, content_parts, local_path))
    except Exception as e:
        print(f"  ERROR: {local_path}: {e}")

# Sort by folio number
entries.sort(key=lambda x: x[0])
print(f"  Sorted {len(entries)} entries\n")

# Step 4: Write Markdown output
os.makedirs("tests/output", exist_ok=True)
output_path = "tests/output/test_toc_folio_order.md"

with open(output_path, "w") as f:
    f.write("# Toyota Echo Service Manual — Table of Contents\n")
    f.write("\n")
    f.write("Entries listed in folio order (the order they appear in the merged PDF).\n")
    f.write("Page numbers are chapter-relative (e.g. CH-1). Folio numbers are the sequential numbers used for sorting.\n")
    f.write("\n")

    current_chapter = None
    current_section = None

    for folio_num, page_num, parts, path in entries:
        chapter = parts[0] if len(parts) > 0 else "?"
        section = parts[1] if len(parts) > 1 else "?"
        procedure = parts[2] if len(parts) > 2 else "?"

        if chapter != current_chapter:
            f.write(f"\n## {chapter}\n")
            current_chapter = chapter
            current_section = None

        if section != current_section:
            f.write(f"\n### {section}\n\n")
            f.write(f"| Page | Folio | Procedure |\n")
            f.write(f"|------|-------|-----------|\n")
            current_section = section

        f.write(f"| {page_num} | {folio_num} | {procedure} |\n")

print(f"Written to {output_path}")