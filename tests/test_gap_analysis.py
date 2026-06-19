# test_gap_analysis.py
# Spike: Analyze folio number gaps to determine if they represent
# missing content or are accounted for by multi-page PDFs.
#
# For each gap in the folio number sequence, this script finds the
# PDF whose folio number immediately precedes the gap and counts its
# pages. If the PDF's page count bridges the gap, the gap is benign.
# If not, the gap represents potentially missing content.
#
# Expected result: all gaps accounted for by multi-page PDFs.

import pdfplumber
import re
import os

DOWNLOAD_DIR = "pdfs"

def get_all_entries():
    # Collect all local PDFs and their folio numbers
    entries = []
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for filename in files:
            if filename.endswith(".pdf"):
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
                                entries.append((folio_num, page_count, path))
                except Exception as e:
                    print(f"  ERROR reading {path}: {e}")
    return sorted(entries, key=lambda x: x[0])

print("Reading all PDFs and their folio numbers...")
entries = get_all_entries()
print(f"Found {len(entries)} PDFs\n")

# Find gaps
folio_nums = [e[0] for e in entries]
all_folios = set(folio_nums)
min_folio = min(folio_nums)
max_folio = max(folio_nums)
full_range = set(range(min_folio, max_folio + 1))
gaps = sorted(full_range - all_folios)

print(f"Folio range: {min_folio} to {max_folio}")
print(f"Total gaps: {len(gaps)}\n")

# For each gap, check if it's bridged by the preceding PDF's page count
unaccounted = []

for i, (folio_num, page_count, path) in enumerate(entries):
    # Find gaps that should be covered by this PDF
    expected_folios = set(range(folio_num + 1, folio_num + page_count))
    covered_gaps = expected_folios & set(gaps)
    uncovered = expected_folios - all_folios - set(gaps)

    if covered_gaps:
        pass  # These gaps are accounted for by this PDF's page count

# Check which gaps are NOT accounted for by any PDF's page count
covered = set()
for folio_num, page_count, path in entries:
    for p in range(folio_num + 1, folio_num + page_count):
        covered.add(p)

unaccounted_gaps = sorted(set(gaps) - covered)

print(f"Gaps accounted for by multi-page PDFs: {len(gaps) - len(unaccounted_gaps)}")
print(f"Unaccounted gaps: {len(unaccounted_gaps)}")

if unaccounted_gaps:
    print(f"\nUnaccounted gap folio numbers:")
    for g in unaccounted_gaps:
        # Find surrounding PDFs
        before = [(f, c, p) for f, c, p in entries if f < g]
        after = [(f, c, p) for f, c, p in entries if f > g]
        prev = before[-1] if before else None
        nxt = after[0] if after else None
        prev_str = f"folio {prev[0]} ({prev[2]}, {prev[1]} pages)" if prev else "none"
        next_str = f"folio {nxt[0]} ({nxt[2]})" if nxt else "none"
        print(f"  Gap {g}: after {prev_str}, before {next_str}")
else:
    print("\nAll gaps accounted for. No missing content detected.")