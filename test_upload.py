import requests
import json

url = 'http://localhost:8080/api/upload'
file_path = r'C:\Users\finan\Downloads\BAO CAO TAI CHINH ALPHA GROUP 2025.xlsx'

with open(file_path, 'rb') as f:
    files = {'file': (file_path.split('\\')[-1], f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
    response = requests.post(url, files=files)

with open('test_upload_resp.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=2)
