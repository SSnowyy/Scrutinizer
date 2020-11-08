from flask import Flask, jsonify, request
import requests

class Nessie():

  base_url = 'http://api.reimaginebanking.com'
  
  api_key = '58317cb8a2fc6ee600adc99f39292e3d'
  #api_key = '3ace02217b05e8623bed792da13c98a3'
  
  def delete_all_data(self):
    self.delete('/data?type=Deposits')
    self.delete('/data?type=Withdrawals')
    self.delete('/data?type=Accounts')
    self.delete('/data?type=Customers')
 
  def get(self, path):
    resp = requests.get(self.url(path))

    if resp.status_code != 200:
      return None
      #raise ApiError('GET {} {}'.format(url, resp.status_code))
	  
    return resp.json()

	
  def post(self, path, obj):
    resp = requests.post(self.url(path), json=obj)

    if resp.status_code != 201:
      return None
    #  raise ApiError('POST {} {}'.format(url, resp.status_code))

    return resp.json()

  def delete(self, path):
    resp = requests.delete(self.url(path))

    #if resp.status_code != 200:
    #  raise ApiError('DELETE {} {}'.format(url, resp.status_code))

    #return resp.json()
	
  def url(self, path):
    if '?' in path:
      return '{}{}&key={}'.format(self.base_url, path, self.api_key)
    else:
      return '{}{}?key={}'.format(self.base_url, path, self.api_key)
      
