
import requests
import json

url = "http://127.0.0.1:1234/userlogin"

payload="{\n    \"username\": \"test2\",\"password\": \"test2\"\n}"
print(payload)
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


url = "http://127.0.0.1:1234/state"
header = {}
# Pass from dictionary to a json object.
header['Authorization'] = 'Bearer  '+ response.json()['access_token']
json.dumps(header)
print(header)
resp = requests.request("GET", url, headers=header, data=payload)

print(resp.text)
 
url = "http://127.0.0.1:1234/devices"

# Get devices 
resp = requests.request("GET", url, headers=header, data=payload)
# add a new device
print(resp.text)
payload={'name':'Caldera'}
resp = requests.request("POST", url, headers=header, json=payload)
'''
print(route)
    headers = {
      'Content-Type': 'application/json'
    }
    payload={}
    # Pass from dictionary to a json object.
    payload['username'] = _username
    payload['password']=_password
    json.dumps(payload)
    print(payload)
    response = requests.request("POST", route, headers=headers, data=payload)
    
    '''