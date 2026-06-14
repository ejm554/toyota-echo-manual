import requests

url = "https://caphector.com/atoyota/techinfo.toyota.com/ileaf/02toyrm/02toypdf/02rmsour/2002/02echorm/ac/acsy/prec.pdf"

response = requests.get(url)

print("Status code:", response.status_code)
print("Content type:", response.headers.get("content-type"))
print("File size (bytes):", len(response.content))

# Write to disk
with open("test_download.pdf", "wb") as f:
    f.write(response.content)

print("File written: test_download.pdf")