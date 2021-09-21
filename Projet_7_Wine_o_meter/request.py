import requests

url = "http://localhost:5000/predict_live"
r = requests.post(url, json=[])
assert r.status_code == 200
print(r.json())