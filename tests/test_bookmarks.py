# test_bookmarks.py
# Stage 4, Spike: Confirm pypdf can add bookmarks to a merged PDF
#
# Downloads 5 PDFs from different chapters, extracts their header page
# numbers and folio numbers, merges them, and adds a bookmark for each
# section using the format: "CH-17: Charging > Generator > Installation"
#
# Expected result: a merged PDF written to tests/output/test_bookmarks.pdf
# that displays a bookmark panel in Preview with correctly labeled and
# positioned entries.

import requests
import pdfplumber
import pypdf
import re
import io
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Sample URLs from different chapters
SAMPLES = [
    ("Charging",   "Generator",    "Disassembly",  "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/gene/disa.pdf"),
    ("Charging",   "Generator",    "Inspection",   "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/gene/insp.pdf"),
    ("Clutch",     "Troubleshooting", "Problem Symptoms Table", "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/trou/pst.pdf"),
    ("Clutch",     "Clutch Master Cylinder", "Removal", "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/cmc/remo.pdf"),
    ("Air Conditioning", "Air Conditioning System", "Precaution", "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/prec.pdf"),
]

def extract_folio_num(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        first_page = pdf.pages[0]
        page_height = first_page.height
        footer_region = first_page.crop(
            (0, page_height - 50, first_page.width, page_height)
        )
        footer_text = footer_region.extract_text()
        if footer_text:
            match = re.search(r"Date.*?(\d+)\s*$", footer_text, re.MULTILINE)
            if match:
                return int(match.group(1))
    return None

def extract_page_num(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        first_page = pdf.pages[0]
        header_region = first_page.crop((0, 0, first_page.width, 50))
        header_text = header_region.extract_text()
        if header_text:
            return header_text.split("\n")[0].strip()
    return None

# Download and collect data
print("Downloading sample PDFs...")
entries = []
for chapter, section, procedure, url in SAMPLES:
    response = requests.get(url)
    pdf_bytes = response.content
    folio_num = extract_folio_num(pdf_bytes)
    page_num = extract_page_num(pdf_bytes)
    entries.append((folio_num, page_num, chapter, section, procedure, pdf_bytes))
    print(f"  folio={folio_num} page={page_num} — {chapter} > {section} > {procedure}")
    time.sleep(0.5)

# Sort by folio number
entries.sort(key=lambda x: x[0])

# Merge and add bookmarks
print("\nMerging and adding bookmarks...")
writer = pypdf.PdfWriter()
current_page = 0

for folio_num, page_num, chapter, section, procedure, pdf_bytes in entries:
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    for page in reader.pages:
        writer.add_page(page)

    # Bookmark label format: "CH-8: Charging > Generator > Disassembly"
    label = f"{page_num}: {chapter} > {section} > {procedure}"
    writer.add_outline_item(label, current_page)
    print(f"  Added bookmark: {label} (at merged page {current_page + 1})")

    current_page += len(reader.pages)

import os
os.makedirs("tests/output", exist_ok=True)
output_path = "tests/output/test_bookmarks.pdf"
with open(output_path, "wb") as f:
    writer.write(f)

print(f"\nWritten to: {output_path}")
print(f"Total pages: {current_page}")
print("\nOpen in Preview and check the bookmark panel (View > Table of Contents).")