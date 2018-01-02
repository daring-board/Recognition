import urllib.request
import json

def weather():
    location = u'360020' #場所
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' %location
    html = urllib.request.urlopen(url)
    jsonfile = json.loads(html.read().decode('utf-8'))
    print(jsonfile['description'])
    return jsonfile['description']['text'].replace('\n', '')
