import requests
import json

payload = {'app_id' : 'abec09cd',
            'app_key' : '66cc31dcd04ab364bff95bd62fe527c8',
            'q' : 'chicken'
}

r = requests.get('http://api.edamam.com/search', params=payload)
rdict = json.loads(r.text)

for hit in rdict['hits']:
    print(hit['recipe'])

