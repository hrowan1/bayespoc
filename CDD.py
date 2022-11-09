import json
import urllib.request

from urllib.request import Request

with urllib.request.urlopen('https://valorant-api.com/v1/agents') as url:
    data = json.loads(url.read())
    
for i in data['data']:
    try:
        f = open(r'Agents/{0}.png'.format(i['displayName']),'wb')
        url = 'https://github.com/InFinity54/Valorant_DDragon/blob/master/Characters/{0}.png?raw=true'.format(i['uuid'].upper())
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        f.write(urllib.request.urlopen(req).read())
        f.close()
    except:
        pass
