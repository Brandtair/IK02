import requests
import json

payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : 'chicken'
}

r = requests.get('http://api.edamam.com/search', params=payload)
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)
print(type(r.text))
rdict = json.loads(r.text)
for rec in rdict:
    print(rdict[rec])