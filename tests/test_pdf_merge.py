# test_pdf_merge.py
# Stage 2, Step 7b - Spike: Confirm pypdf can merge multiple PDFs
#
# Tests whether pypdf can merge a small set of already-downloaded PDFs
# into a single output file. Uses PDFs already on disk from previous
# spikes rather than downloading new ones.
#
# Expected result: a valid merged PDF written to tests/output/test_merge.pdf
# containing pages from all input files in the correct order.

import pypdf
import os

# Use the PDF we already have on disk from previous spike runs
input_files = [
    "tests/output/test_download.pdf",
]

# Check which files exist
existing = [f for f in input_files if os.path.exists(f)]
print(f"Found {len(existing)} input files")

if not existing:
    print("No input files found. Run test_download_pdf.py first.")
    exit(1)

# Create test output directory if it doesn't exist
os.makedirs("tests/output", exist_ok=True)
output_path = "tests/output/test_merge.pdf"

# Merge PDFs
writer = pypdf.PdfWriter()

for path in existing:
    reader = pypdf.PdfReader(path)
    print(f"Adding {path}: {len(reader.pages)} page(s)")
    for page in reader.pages:
        writer.add_page(page)

with open(output_path, "wb") as f:
    writer.write(f)

print(f"\nMerged PDF written to: {output_path}")
print(f"Total pages in output: {len(writer.pages)}")