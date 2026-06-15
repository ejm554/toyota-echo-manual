# test_download_pdf.py
# Stage 1, Step 5 - Spike: Confirm single PDF download works
#
# Tests whether the server will serve individual PDF files and whether
# we can write them to disk. Uses a known AC section PDF as a sample.
#
# Expected result: status 200, content-type application/pdf, file written
# to tests/output/test_download.pdf

import requests
import os

url = "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/prec.pdf"

response = requests.get(url)

print("Status code:", response.status_code)
print("Content type:", response.headers.get("content-type"))
print("File size (bytes):", len(response.content))

# Create test output directory if it doesn't exist
os.makedirs("tests/output", exist_ok=True)

# Write to disk
with open("tests/output/test_download.pdf", "wb") as f:
    f.write(response.content)

print("File written: tests/output/test_download.pdf")