import requests
"""
Skeleton sample for prototyping unit tests
"""
BASE = "http://localhost:5000"

response = requests.get(BASE + "foo")
print(response.json())
