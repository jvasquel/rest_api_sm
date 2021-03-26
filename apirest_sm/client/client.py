import requests
import json

class Request:
  url=''
  header={''}

  def __init__(self,_url):
    self.url=_url
    self.header={}
  
  def set_dir(self,endpoint):
    _url=self.url
    if  _url=='':
      return False
    
    return _url+endpoint
  


  def userlogin(self,_username,_password):
    route=Request.set_dir(self,"userlogin")
    print(route)
    
    payload={}
    payload['username'] = _username
    payload['password']=_password
    json.dumps(route)
    print(payload)
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", route, headers=headers, json=payload)

    print(response.text)
    print("REsponse")
    self.header['Authorization'] = 'Bearer  '+ response.json()['access_token']
    json.dumps(self.header)
    return response

  def getstate(self):
    route=Request.set_dir(self,"state")
    print(route)
    resp = requests.request("GET", route, headers=self.header )
    print(resp.text)

  def getdevices(self):
    route=Request.set_dir(self,"devices")
    print(route)
    resp = requests.request("GET", route, headers=self.header )
    print(resp.text)



  def addevices(self,_name):
    route=Request.set_dir(self,"devices")
    payload={}
    payload['name']=_name
    json.dumps(payload)
    resp = requests.request("POST", route, headers=self.header, json=payload)
    print(resp.text)




  