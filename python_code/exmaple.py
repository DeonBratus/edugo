import requests
import json

# Чтение данных из JSON-файла
with open('data.json', 'r') as file:
    requests_data = json.load(file)

# URL сервиса
service_url = "http://127.0.0.1:8000/"

# Отправка каждого запроса
for request in requests_data['requests']:
    response = requests.post(url=service_url, json=request['body'])
    print(f"Response for {request['name']} - {response.json()}")