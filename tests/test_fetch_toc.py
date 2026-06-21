# test_fetch_toc.py
# Stage 1, Step 4 - Spike: Confirm TOC page is fetchable
#
# Tests whether the caphector.com table of contents page is reachable
# and returns expected HTML content. This is a prerequisite for all
# subsequent scraping work.
#
# Expected result: status 200, content-type text/html, HTML with PDF links visible

import requests

url = "https://caphector.com/atoyota/TableOfContents/manual.html"

response = requests.get(url)

print("Status code:", response.status_code)
print("Content type:", response.headers.get("content-type"))
print("First 500 characters:\n")
print(response.text[:500])