# test_scrape_toc.py
# Stage 3, Step 11 - Spike: Parse all PDF links from the TOC page
#
# Tests whether BeautifulSoup can extract all PDF links from the
# caphector TOC page and construct valid absolute URLs for downloading.
# Uses urljoin to correctly resolve relative URLs including ../ paths.
#
# Expected result: a list of clean absolute URLs, count in the hundreds,
# all ending in .pdf with no ../ artifacts

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

TOC_URL = "https://caphector.com/atoyota/TableOfContents/manual.html"

response = requests.get(TOC_URL)
soup = BeautifulSoup(response.text, "html.parser")

links = []
for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.endswith(".pdf"):
        absolute_url = urljoin(TOC_URL, href)
        links.append(absolute_url)

print(f"Total PDF links found: {len(links)}")
print("\nFirst 5:")
for url in links[:5]:
    print(" ", url)
print("\nLast 5:")
for url in links[-5:]:
    print(" ", url)