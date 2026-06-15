# test_header_extraction.py
# Stage 2, Step 9b - Spike: Extract page number from PDF header
#
# Scrapes all 816 URLs from the TOC, picks the first and last URL from
# each unique chapter directory, then extracts the header page number
# from each. This confirms:
#   1. All chapter prefix codes (e.g., AC, BR, SFI)
#   2. Maximum page number digits per chapter (e.g., AC-91 vs AC-1)
#   3. Whether any prefixes use 3+ letters
#   4. Whether multi-line headers are isolated or common
#
# Expected result: first and last page numbers per chapter, all matching
# pattern [A-Z]+-\d+, with a complete list of unique prefixes.

import requests
import pdfplumber
import re
import io
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

TOC_URL = "https://caphector.com/atoyota/TableOfContents/manual.html"

def scrape_urls(toc_url):
    response = requests.get(toc_url)
    soup = BeautifulSoup(response.text, "html.parser")
    urls = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".pdf"):
            urls.append(urljoin(toc_url, href))
    return urls

def get_chapter_dir(url):
    match = re.search(r"02echorm/([^/]+)/", url)
    return match.group(1) if match else None

def extract_header(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        first_page = pdf.pages[0]
        header_region = first_page.crop((0, 0, first_page.width, 50))
        return header_region.extract_text()

def fetch_header(url):
    response = requests.get(url)
    content_type = response.headers.get("content-type", "unknown")
    if "pdf" not in content_type.lower():
        return None, f"SKIPPED - content-type: {content_type}"
    try:
        return extract_header(response.content), None
    except Exception as e:
        return None, f"ERROR: {e}"

# Scrape all URLs and pick first and last per chapter directory
print("Scraping TOC...")
all_urls = scrape_urls(TOC_URL)
print(f"Found {len(all_urls)} URLs\n")

chapter_first = {}
chapter_last = {}
for url in all_urls:
    chapter_dir = get_chapter_dir(url)
    if chapter_dir:
        if chapter_dir not in chapter_first:
            chapter_first[chapter_dir] = url
        chapter_last[chapter_dir] = url

print(f"Unique chapter directories: {len(chapter_first)}")
print("Testing first and last PDF per chapter...\n")

prefixes_found = set()
multiline_headers = []
failures = []

for chapter_dir in sorted(chapter_first.keys()):
    first_url = chapter_first[chapter_dir]
    last_url = chapter_last[chapter_dir]

    first_header, first_err = fetch_header(first_url)
    time.sleep(0.5)

    if first_url == last_url:
        last_header, last_err = None, "same as first"
    else:
        last_header, last_err = fetch_header(last_url)
        time.sleep(0.5)

    first_str = repr(first_header) if first_header else first_err
    last_str = repr(last_header) if last_header else last_err

    if first_header:
        prefixes_found.add(first_header.split("-")[0])

    # Flag multi-line headers
    if first_header and "\n" in first_header:
        multiline_headers.append(f"{chapter_dir} (first): {repr(first_header)}")
    if last_header and "\n" in last_header:
        multiline_headers.append(f"{chapter_dir} (last): {repr(last_header)}")

    print(f"  {chapter_dir:10} first={first_str:15} last={last_str}")

    if first_err:
        failures.append(f"{chapter_dir} (first)")
    if last_err and last_err != "same as first":
        failures.append(f"{chapter_dir} (last)")

print(f"\nUnique prefixes found ({len(prefixes_found)}): {sorted(prefixes_found)}")

if multiline_headers:
    print(f"\nMulti-line headers found ({len(multiline_headers)}):")
    for h in multiline_headers:
        print(f"  {h}")
else:
    print("\nNo multi-line headers found.")

if failures:
    print(f"\nFailures ({len(failures)}): {failures}")
else:
    print("\nNo failures.")