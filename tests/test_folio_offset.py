# test_folio_offset.py
# Spike: Find where the offset between Preview page numbers and folio
# numbers accumulates in the merged PDF.
#
# Reads the page-folio map and reconstructs the merged PDF page order
# by sorting entries by folio number. Tracks the cumulative offset
# (Preview page number minus folio number) and reports every point
# where it changes.
#
# Expected result: a list of folio numbers where the offset increases,
# indicating multi-page PDFs that contribute extra pages to the merge.

import pdfplumber
import re
import os

DOWNLOAD_DIR = "pdfs"

print("Reading all PDFs in folio order...")

# Collect first-page folio numbers and page counts
pdf_entries = []
for root, dirs, files in os.walk(DOWNLOAD_DIR):
    for filename in files:
        if not filename.endswith(".pdf"):
            continue
        path = os.path.join(root, filename)
        try:
            with pdfplumber.open(path) as pdf:
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
                        page_count = len(pdf.pages)
                        pdf_entries.append((folio_num, page_count, path))
        except Exception as e:
            print(f"  ERROR: {path}: {e}")

# Sort by folio number
pdf_entries.sort(key=lambda x: x[0])

print(f"Found {len(pdf_entries)} PDFs\n")
print("Folio numbers where offset changes (multi-page PDFs):\n")
print(f"  {'Folio':>6}  {'Pages':>5}  {'Offset After':>12}  {'Path'}")
print(f"  {'-'*6}  {'-'*5}  {'-'*12}  {'-'*40}")

cumulative_offset = 0
preview_page = 0

for folio_num, page_count, path in pdf_entries:
    preview_page += page_count
    new_offset = preview_page - (folio_num + page_count - 1)
    
    if page_count > 1:
        extra = page_count - 1
        cumulative_offset += extra
        short_path = path.replace("pdfs/", "")
        print(f"  {folio_num:>6}  {page_count:>5}  {cumulative_offset:>12}  {short_path}")

print(f"\nTotal offset at end of document: {cumulative_offset}")
print(f"(Preview page count will exceed highest folio number by {cumulative_offset})")