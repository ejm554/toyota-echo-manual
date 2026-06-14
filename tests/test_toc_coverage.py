# test_toc_coverage.py
# Stage 3, Step 12 - Spike: Verify TOC link count looks complete
#
# Extracts all PDF links and their label text, then groups them by
# chapter to check for obvious gaps. We're looking for a reasonable
# distribution across chapters with nothing obviously missing.
#
# Expected result: multiple chapters represented, counts that look
# plausible for a full factory service manual.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import Counter

TOC_URL = "https://caphector.com/atoyota/TableOfContents/manual.html"

response = requests.get(TOC_URL)
soup = BeautifulSoup(response.text, "html.parser")

chapters = Counter()

for a in soup.find_all("a", href=True):
    href = a["href"]
    if href.endswith(".pdf"):
        label = a.get_text(strip=True)
        # Label format: "R.M. 2002::Chapter: Section: Procedure"
        parts = label.split("::")
        if len(parts) >= 2:
            chapter = parts[1].split(":")[0].strip()
            chapters[chapter] += 1

print(f"Total chapters: {len(chapters)}")
print(f"Total PDFs: {sum(chapters.values())}\n")
for chapter, count in sorted(chapters.items()):
    print(f"  {count:4}  {chapter}")