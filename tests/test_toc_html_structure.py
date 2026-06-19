# test_toc_html_structure.py
# Spike: Investigate malformed HTML in the TOC page
#
# The TOC page appears to have at least one unclosed <a> tag, causing
# BeautifulSoup to incorrectly associate hundreds of label texts with
# a single URL. This spike maps the full extent of the problem by
# examining the raw HTML structure and identifying which links have
# suspiciously long or missing labels.
#
# Expected result: a clear picture of which URLs have correct labels
# and which are affected by the malformed HTML.

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
        url = urljoin(TOC_URL, href)
        label = a.get_text(strip=True)
        links.append((url, label))

print(f"Total PDF links found: {len(links)}\n")

# Analyze label lengths
label_lengths = [(len(label), url, label[:80]) for url, label in links]
label_lengths.sort(reverse=True)

print("Top 10 longest labels (potential malformed HTML):")
for length, url, preview in label_lengths[:10]:
    print(f"  {length:6} chars  {url.split('02echorm/')[1]:30}  {preview}")

print("\nLabels by length distribution:")
buckets = {"normal (< 200)": 0, "suspicious (200-1000)": 0, "malformed (> 1000)": 0}
for url, label in links:
    if len(label) < 200:
        buckets["normal (< 200)"] += 1
    elif len(label) < 1000:
        buckets["suspicious (200-1000)"] += 1
    else:
        buckets["malformed (> 1000)"] += 1

for bucket, count in buckets.items():
    print(f"  {bucket}: {count}")

print("\nFirst and last normal-length labels:")
normal = [(url, label) for url, label in links if len(label) < 200]
print(f"  First: {normal[0][1]}")
print(f"  Last:  {normal[-1][1]}")