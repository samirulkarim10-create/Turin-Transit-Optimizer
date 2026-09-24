# Extracts the GTFS data and unpacks it


import requests
import zipfile
import io
import sys

GTT_URL = "https://www.gtt.to.it/cms/opendata/google_transit.zip"

print("Downloading Turin transit data. This might take a few seconds...")

# 1. Add a User-Agent to mimic a macOS web browser
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(GTT_URL, headers=headers)

# 2. Check if the server actually gave us a successful response (Status 200)
if response.status_code != 200:
    print(f"Error: Server returned status {response.status_code}. The link might have moved.")
    sys.exit()

# 3. Check if the file starts with 'PK' (the universal byte signature for zip files)
if not response.content.startswith(b'PK'):
    print("Error: The server returned a webpage instead of a zip file. It is likely blocking automated downloads.")
    sys.exit()

# 4. Extract the verified zip file
zip_buffer = io.BytesIO(response.content)
with zipfile.ZipFile(zip_buffer) as gtfs_zip:
    gtfs_zip.extractall("data")

print("Success! Check your 'data' folder.")