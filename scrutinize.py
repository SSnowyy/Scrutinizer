import requests

class Scrutinize():
  base_url = 'http://127.0.0.1:5000'

  def get(self, path):
    resp = requests.get(self.url(path))

    #if resp.status_code != 200:
    #  raise ApiError('GET {} {}'.format(url, resp.status_code))
	
    return resp.json()

	
  def post(self, path, obj):
    resp = requests.post(self.url(path), json=obj)

    #if resp.status_code != 201:
    #  raise ApiError('POST {} {}'.format(url, resp.status_code))

    return resp.json()

  def delete(self, path):
    resp = requests.delete(self.url(path))

    #if resp.status_code != 200:
    #  raise ApiError('DELETE {} {}'.format(url, resp.status_code))

    #return resp.json()
	
  def url(self, path):
    if '?' in path:
      return '{}{}'.format(self.base_url, path)
    else:
      return '{}{}'.format(self.base_url, path)
