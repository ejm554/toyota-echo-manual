# merge_service_manual.py
# Main pipeline script for the Toyota Echo Service Manual Merger
#
# Performs the following steps in sequence:
#   1. Scrapes all PDF URLs from the caphector TOC page
#   2. Downloads each PDF into pdfs/ mirroring the server directory
#      structure, skipping any files already downloaded
#   3. Extracts the folio number from the footer of each PDF's first page
#   4. Sorts all PDFs by folio number
#   5. Merges them in order into a single output PDF
#
# Usage: python3 merge_service_manual.py
#
# Output: output/echo_service_manual.pdf
#
# Terminology:
#   Page number  — chapter-relative number in the header (e.g., CH-2, CL-1)
#   Folio number — sequential number in the footer (e.g., 864, 865)
#                  used internally to sort and merge PDFs in correct order
#
# Notes:
#   - Downloads are sequential with a 1 second delay between requests
#   - Resume support: already-downloaded PDFs are skipped
#   - PDFs are not included in git (see .gitignore)

import requests
import pdfplumber
import pypdf
import re
import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# --- Configuration ---

TOC_URL = "https://caphector.com/atoyota/TableOfContents/manual.html"
DOWNLOAD_DIR = "pdfs"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "echo_service_manual.pdf")
DOWNLOAD_DELAY = 1  # seconds between requests
MAX_DOWNLOADS = 10  # set to None to download all


# --- Step 1: Scrape PDF URLs from TOC page ---

def scrape_pdf_urls(toc_url):
    print("Step 1: Scraping PDF URLs from TOC page...")
    response = requests.get(toc_url)
    soup = BeautifulSoup(response.text, "html.parser")

    urls = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".pdf"):
            urls.append(urljoin(toc_url, href))

    print(f"  Found {len(urls)} PDF URLs")
    return urls


# --- Step 2: Download PDFs ---

def url_to_local_path(url):
    # Derive local path from URL structure, mirroring server directories.
    # Example URL: https://caphector.com/atoyota/techinfo.toyota.com/ileaf/
    #              02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/prec.pdf
    # Extracts the chapter/section/file portion after "02echorm/"
    match = re.search(r"02echorm/(.+)", url)
    if match:
        relative_path = match.group(1)
        return os.path.join(DOWNLOAD_DIR, relative_path)
    return None

def download_pdfs(urls):
    print("\nStep 2: Downloading PDFs...")
    downloaded = 0
    skipped = 0

    for i, url in enumerate(urls[:MAX_DOWNLOADS] if MAX_DOWNLOADS else urls):
        local_path = url_to_local_path(url)
        if not local_path:
            print(f"  WARNING: Could not derive local path for {url}")
            continue

        # Skip if already downloaded
        if os.path.exists(local_path):
            skipped += 1
            continue

        # Create directory if needed
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Download
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            downloaded += 1
            print(f"  [{i+1}/{len(urls)}] Downloaded: {local_path}")
        else:
            print(f"  [{i+1}/{len(urls)}] FAILED ({response.status_code}): {url}")

        time.sleep(DOWNLOAD_DELAY)

    print(f"  Done. {downloaded} downloaded, {skipped} skipped.")


# --- Step 3: Extract folio numbers ---

def extract_folio_num(pdf_path):
    # Extract the folio number from the footer of the first page only.
    # Uses coordinate-based cropping to target the bottom 50 points of
    # the page, avoiding false matches from page number references in
    # the body text.
    #
    # Footer format: "Author(cid:1): Date(cid:1): [folio number]"
    # The (cid:1) artifacts require anchoring the regex to end-of-line.
    try:
        with pdfplumber.open(pdf_path) as pdf:
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
    except Exception as e:
        print(f"  WARNING: Could not extract folio number from {pdf_path}: {e}")
    return None

def extract_all_folio_nums(urls):
    print("\nStep 3: Extracting folio numbers from PDF footers...")
    pdf_entries = []
    failures = []

    for url in urls:
        local_path = url_to_local_path(url)
        if not local_path or not os.path.exists(local_path):
            continue

        folio_num = extract_folio_num(local_path)
        if folio_num is not None:
            pdf_entries.append((folio_num, local_path))
        else:
            failures.append(local_path)
            print(f"  WARNING: No folio number found in {local_path}")

    print(f"  Extracted {len(pdf_entries)} folio numbers, {len(failures)} failures")
    return pdf_entries, failures


# --- Step 4: Sort by folio number ---

def sort_pdfs(pdf_entries):
    print("\nStep 4: Sorting PDFs by folio number...")
    sorted_entries = sorted(pdf_entries, key=lambda x: x[0])
    print(f"  First: folio {sorted_entries[0][0]} ({sorted_entries[0][1]})")
    print(f"  Last:  folio {sorted_entries[-1][0]} ({sorted_entries[-1][1]})")
    return sorted_entries


# --- Step 5: Merge ---

def merge_pdfs(sorted_entries):
    print("\nStep 5: Merging PDFs...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    writer = pypdf.PdfWriter()

    for i, (folio_num, path) in enumerate(sorted_entries):
        try:
            reader = pypdf.PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
            print(f"  [{i+1}/{len(sorted_entries)}] Added {path} (folio {folio_num})")
        except Exception as e:
            print(f"  WARNING: Could not merge {path}: {e}")

    with open(OUTPUT_FILE, "wb") as f:
        writer.write(f)

    print(f"\n  Merged PDF written to: {OUTPUT_FILE}")
    print(f"  Total pages: {len(writer.pages)}")


# --- Main ---

if __name__ == "__main__":
    urls = scrape_pdf_urls(TOC_URL)
    download_pdfs(urls)
    pdf_entries, failures = extract_all_folio_nums(urls)
    sorted_entries = sort_pdfs(pdf_entries)
    merge_pdfs(sorted_entries)

    if failures:
        print(f"\nWARNING: {len(failures)} PDFs could not be assigned a folio number and were excluded from the merge.")
    else:
        print("\nComplete. No failures.")