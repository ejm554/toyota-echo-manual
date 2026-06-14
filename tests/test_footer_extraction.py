# test_footer_extraction.py
# Stage 2, Step 9 - Spike: Extract global page number from PDF footer
#
# Tests whether we can reliably extract the global sequential page number
# from the footer of the first page only, using coordinate-based cropping
# to target the bottom of the page. This avoids false matches from page
# number references in the body text.
#
# The footer contains: Author(cid:1): Date(cid:1): [number]
# The (cid:1) artifacts require a looser regex pattern.
# The regex anchors to end-of-line to avoid matching (cid:1) digits.
#
# Expected result: global page number 1448 extracted from test_download.pdf

import pdfplumber
import re

def extract_page_number(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]

        # Crop to bottom 50 points of the page
        # pdfplumber uses points (1/72 inch); 50 points ~ 0.7 inches
        page_height = first_page.height
        footer_region = first_page.crop((0, page_height - 50, first_page.width, page_height))

        footer_text = footer_region.extract_text()
        print(f"Raw footer text: {repr(footer_text)}")

        if footer_text:
            # Anchor to end-of-line to avoid matching digits inside (cid:1) artifacts
            match = re.search(r"Date.*?(\d+)\s*$", footer_text, re.MULTILINE)
            if match:
                return int(match.group(1))

    return None

result = extract_page_number("test_download.pdf")
print(f"Extracted page number: {result}")