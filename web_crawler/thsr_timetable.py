import requests
from bs4 import BeautifulSoup
import json

thsr_home_url = 'https://www.thsrc.com.tw/index.html'
thsr_timetable_url = 'https://www.thsrc.com.tw/tw/TimeTable/Search'
sta_hash={}

def get_station_hash():
    print('getting station hash for post requests...')
    req = requests.get('https://www.thsrc.com.tw/tw/TimeTable/SearchResult')
    encode = req.apparent_encoding
    req.encoding = str(encode)
    soup = BeautifulSoup(req.text, 'html.parser')
    stations = soup.find('select', id='StartStation')
    stations = stations.find_all('option')
    for sta in stations[1:]:
        #print(sta['value'], sta.text)
        hash = sta['value']
        name = sta.text
        sta_hash[name] = hash
    

get_station_hash()
a = list(sta_hash.keys())
start = a[0]
end = a[1]
formdata = {
    'StartStationName': start,
    'EndStationName': end,
    'SearchType': 'S',
    'StartStation': sta_hash[start],
    'EndStation': sta_hash[end],
    'DepartueSearchDate': '2019/05/23',
    'DepartueSearchTime': '14:00',
    'DepartueTrainCode': '',
    'DestinationSearchDate': '',
    'DestinationSearchTime': '',
    'DiscountType': ''
} 
req = requests.post(thsr_timetable_url, data=formdata)
encode = req.apparent_encoding
req.encoding = str(encode)


result = json.loads(req.text)
trains = result['data']['DepartureTable']['TrainItem']
coach_price = result['data']['PriceTable']['Coach'][0]
print('Time table between {} -> {}'.format(start, end))
print('Price: {}'.format(coach_price))
print('{:>10} {:>10} {:>12} {:>10}'.format('Train No.', 'Departure', 'Destination', 'Duration'))
for train in trains:
    print('{:>10} {:>10} {:>12} {:>10}'.format(train['TrainNumber'], train['DepartureTime'], train['DestinationTime'], train['Duration']))

