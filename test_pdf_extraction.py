# test_pdf_extraction.py
# Stage 2, Step 8 - Spike: Confirm text extraction from a downloaded PDF
#
# Tests whether pdfplumber can extract text from a locally saved PDF.
# Prints the raw extracted text from each page so we can verify the
# footer pattern is present and readable.
#
# Expected result: text extracted from each page, footer visible with
# pattern "Author: Date: [number]"

import pdfplumber

pdf_path = "test_download.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print(f"Number of pages: {len(pdf.pages)}\n")
    for i, page in enumerate(pdf.pages):
        print(f"--- Page {i+1} ---")
        text = page.extract_text()
        print(text)
        print()