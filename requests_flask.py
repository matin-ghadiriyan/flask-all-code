import requests
req = requests.post('http://127.0.0.1:8080/API' , json={'apikey':'1234567890'})
json = req.json()
if json['Error.Json.API.Key'] == 'error':
    print(json['Error.Json.API.Key'])
else:
    for json_data in json['data']:
        print(f'{json_data}\n')