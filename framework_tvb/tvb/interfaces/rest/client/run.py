import requests


url = " http://127.0.0.1:9090/"
operation = input('Enter operation:')
response = requests.get(url+operation)
print(response.text)