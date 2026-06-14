import requests

url = "https://caphector.com/atoyota/TableOfContents/manual.html"

response = requests.get(url)

print("Status code:", response.status_code)
print("Content type:", response.headers.get("content-type"))
print("First 500 characters:\n")
print(response.text[:500])