# test_footer_consistency.py
# Stage 2, Step 10 - Spike: Confirm footer extraction is consistent across diverse PDFs
#
# Downloads and extracts the global page number from 15 PDFs spanning
# multiple chapters. Verifies that the footer pattern is consistent and
# that no PDFs are missing the expected number.
#
# Expected result: all 15 PDFs return a valid integer page number with no
# None results or unexpected patterns.

import requests
import pdfplumber
import re
import io

URLS = [
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/prec.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/evac.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acu/remo.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/cmc/remo.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/cmc/disa.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/trou/pst.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/gene/comp.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/gene/disa.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/gene/insp.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/chasy/ovi.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/dribel/ovi.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/mgs/seton.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/mgs/setoff.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/reflin/ovi.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/crc/remo.pdf",
]

def extract_page_number(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        first_page = pdf.pages[0]
        page_height = first_page.height
        footer_region = first_page.crop((0, page_height - 50, first_page.width, page_height))
        footer_text = footer_region.extract_text()
        if footer_text:
            match = re.search(r"Date.*?(\d+)\s*$", footer_text, re.MULTILINE)
            if match:
                return int(match.group(1))
    return None

failures = []

for url in URLS:
    filename = url.split("/")[-1]
    chapter = url.split("/")[-3]
    response = requests.get(url)
    page_num = extract_page_number(response.content)
    status = "OK" if page_num is not None else "FAIL"
    print(f"{status}  {chapter:10} {filename:12}  page={page_num}")
    if page_num is None:
        failures.append(url)

print(f"\n{len(failures)} failures out of {len(URLS)} PDFs")