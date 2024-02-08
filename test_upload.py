import requests
from dotenv import load_dotenv
import os
load_dotenv()

def upload_files(url, file_paths):
    headers = {"x-api-key": os.getenv("FASTAPI_KEY")}
    files = [('files', (file_path, open(file_path, 'rb'), 'application/pdf')) for file_path in file_paths]
    response = requests.post(url, files=files, headers=headers)
    return response

url = 'http://0.0.0.0:8000/upload/'
file_paths = ['data/iso27001.pdf']
response = upload_files(url, file_paths)
print("Status Code:", response.status_code)
print("Response:", response.json())
