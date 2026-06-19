# test_page_folio_map.py
# Spike: Generate a complete page number to folio number lookup table.
#
# Reads every page of every downloaded PDF, extracting the page number
# from the header and the folio number from the footer. Outputs a
# Markdown table sorted by page number (e.g., AC-1, AC-2, BE-47)
# for use as a cross-reference lookup when navigating the manual.
#
# Output: tests/output/test_page_folio_map.md
#
# Expected result: ~1540 rows, one per page of the merged PDF, with
# page number, folio number, and chapter code.

import pdfplumber
import re
import os

DOWNLOAD_DIR = "pdfs"

print("Reading all pages from all PDFs...")
rows = []

# Count total PDFs first for progress display
total_files = sum(1 for root, dirs, files in os.walk(DOWNLOAD_DIR)
                  for f in files if f.endswith(".pdf"))
processed = 0

for root, dirs, files in os.walk(DOWNLOAD_DIR):
    for filename in files:
        if not filename.endswith(".pdf"):
            continue
        path = os.path.join(root, filename)
        processed += 1
        print(f"  [{processed}/{total_files}] {path}", end="\r")
        try:
            with pdfplumber.open(path) as pdf:
                for page_index, page in enumerate(pdf.pages):
                    page_height = page.height

                    # Extract folio number from footer (first page only)
                    if page_index == 0:
                        footer_region = page.crop(
                            (0, page_height - 50, page.width, page_height)
                        )
                        footer_text = footer_region.extract_text()
                        if footer_text:
                            match = re.search(r"Date.*?(\d+)\s*$", footer_text, re.MULTILINE)
                            base_folio = int(match.group(1)) if match else None
                        else:
                            base_folio = None

                    # Folio number for this page
                    folio_num = base_folio + page_index if base_folio else None

                    # Extract page number from header
                    header_region = page.crop((0, 0, page.width, 50))
                    header_text = header_region.extract_text()
                    page_num = header_text.split("\n")[0].strip() if header_text else "?"

                    if folio_num and page_num:
                        rows.append((page_num, folio_num, path))

        except Exception as e:
            print(f"  ERROR: {path}: {e}")

print(f"\n  Read {len(rows)} pages")

# Sort by chapter code then page number within chapter
def sort_key(row):
    page_num = row[0]
    match = re.match(r"([A-Z]+)-(\d+)", page_num)
    if match:
        return (match.group(1), int(match.group(2)))
    return (page_num, 0)

rows.sort(key=sort_key)

# Write Markdown output
os.makedirs("tests/output", exist_ok=True)
output_path = "tests/output/test_page_folio_map.md"

with open(output_path, "w") as f:
    f.write("# Toyota Echo Service Manual — Page Number to Folio Number Map\n\n")
    f.write("Use this table to find the folio number (position in the merged PDF) ")
    f.write("for any page number referenced in the manual (e.g., 'see page BE-47').\n\n")
    f.write("| Page Number | Folio |\n")
    f.write("|-------------|-------|\n")
    for page_num, folio_num, path in rows:
        f.write(f"| {page_num} | {folio_num} |\n")

print(f"Written to {output_path}")