import requests

body =  [
{ "type": "calc", "op": "+", "var": "x", "left": 10, "right": 2 },
{ "type": "print", "var": "x" },
{ "type": "calc", "op": "-", "var": "y", "left": "x", "right": 3 },
{ "type": "calc", "op": "*", "var": "z", "left": "x", "right": "y" },
{ "type": "print", "var": "w" },
{ "type": "calc", "op": "*", "var": "w", "left": "z", "right": 0 }
]
response = requests.post(url="http://127.0.0.1:8080/post", json=body)
print(response.text)