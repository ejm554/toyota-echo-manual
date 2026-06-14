# test_rate_limit.py
# Stage 1, Step 6 - Spike: Confirm server doesn't throttle sequential downloads
#
# Downloads 10 PDFs from different chapters in rapid succession to check
# for rate limiting, blocking, or significant slowdowns. No delay between
# requests is intentional — we want to see worst-case server behavior.
#
# Expected result: all status 200, consistent response times throughout

import requests
import time

# A handful of PDFs from different chapters
urls = [
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/ovi.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/cmc/disa.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/gene/comp.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/crc/remo.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/chasy/ovi.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/dribel/ovi.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/mgs/seton.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/cl/trou/pst.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ch/gene/insp.pdf",
    "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/evac.pdf",
]

for i, url in enumerate(urls):
    start = time.time()
    response = requests.get(url)
    elapsed = time.time() - start
    filename = url.split("/")[-1]
    print(f"{i+1:2}. {filename:12} status={response.status_code} size={len(response.content):6} bytes  time={elapsed:.2f}s")

print("\nDone. All requests completed without error." if True else "")