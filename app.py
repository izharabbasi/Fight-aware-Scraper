import requests
from lxml import html
import json

def write_json(data):
    with open('data.json','w',encoding='utf-8') as f:
        f.write(json.dumps(data))

extracted_data = []

def get(l):
    try:
        return l.pop(0)
    except:
        return ''

script = '''
    headers = {
        ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
        ['cookie'] = '_ga=GA1.2.2058404892.1594700712; hubspotutk=e7d9134f5bfeb9151103a2af23f3a00c; __hssrc=1; __qca=P0-39502998-1594700719349; __zlcmid=zBjHZ1OiCSRCsP; _gid=GA1.2.170995674.1595059794; __hstc=53236791.e7d9134f5bfeb9151103a2af23f3a00c.1594700718626.1594706887807.1595059801680.3; __hssc=53236791.1.1595059801680'
  }
  splash.private_mode_enabled = false
  splash.images_enabled = false
  splash:set_custom_headers(headers)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return splash:html()
'''
resp = requests.post(url='http://localhost:8050/run' , json={
    'lua_source' : script,
    'url' : 'https://flightaware.com/live/flight/HOP1319'
})

tree = html.fromstring(html=resp.content)

upcoming_flights = tree.xpath("//div[@id='flightPageActivityLog']/div[1]/div[1]")

for filght in upcoming_flights:
    f = {
        'date': get(filght.xpath(".//div[@data-type='upcoming']/div[1]/span/em/text()")),
        'departure_time': get(filght.xpath(".//div[@data-type='upcoming']/div[2]/div/div/span/em/span/text()")),
        'departure_airport': get(filght.xpath(".//div[@data-type='upcoming']/div[2]/div/div/span[2]/text()")).strip(),
        'arrival_time': get(filght.xpath(".//div[@data-type='upcoming']/div[3]/div/div/span/em/span/text()")).strip(),
        'arrival_airport':get(filght.xpath(".//div[@data-type='upcoming']/div[3]/div/div/span[2]/text()")).strip(),
        'Aircraft':get(filght.xpath(".//div[@data-type='upcoming']/div[4]/span/text()")).strip(),
        'Duration':get(filght.xpath(".//div[@data-type='upcoming']/div[5]/em/text()")).strip()
    }
    extracted_data.append(f)

print(extracted_data)

write_json(extracted_data)