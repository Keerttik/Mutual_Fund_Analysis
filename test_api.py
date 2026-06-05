import requests
import json
url = "http://127.0.0.1:8001/api/chat"
headers = {"Content-Type": "application/json"}
data = {"query": "suggestest hdfc mutual fund for medium risk investor"}
try:
    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Exception:", e)
