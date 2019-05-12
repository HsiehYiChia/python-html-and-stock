import time
import requests
from bs4 import BeautifulSoup
import json


def get_station_hash():
    print('getting station hash for post requests...')
    sta_hash = {}

    # get THSR timetable result page
    req = requests.get('https://www.thsrc.com.tw/tw/TimeTable/SearchResult')
    encode = req.apparent_encoding
    req.encoding = encode

    # parsing the page
    soup = BeautifulSoup(req.text, 'html.parser')
    stations = soup.find('select', id='StartStation')
    stations = stations.find_all('option')
    for sta in stations[1:]:
        hash = sta['value']
        name = sta.text
        sta_hash[name] = hash
    return sta_hash
    





if __name__ == '__main__':
    thsr_home_url = 'https://www.thsrc.com.tw/index.html'
    thsr_timetable_url = 'https://www.thsrc.com.tw/tw/TimeTable/Search'

    sta_hash = get_station_hash()
    start_idx = input("Departure station? 1)南港 2)台北 3)板橋 4)桃園 5)新竹 6)苗栗 7)台中 8)彰化 9)雲林 10)嘉義 11)台南 12)左營    ")
    end_idx = input("Destination station? 1)南港 2)台北 3)板橋 4)桃園 5)新竹 6)苗栗 7)台中 8)彰化 9)雲林 10)嘉義 11)台南 12)左營    ")
    date = input ("Date? (yyyy/mm/dd)    ")
    start_idx = int(start_idx) -1
    end_idx = int(end_idx) - 1
    sta_list = list(sta_hash.keys())
    start_sta = sta_list[start_idx]
    end_sta = sta_list[end_idx]

    formdata = {
    'StartStationName': start_sta,
    'EndStationName': end_sta,
    'SearchType': 'S',
    'StartStation': sta_hash[start_sta],
    'EndStation': sta_hash[end_sta],
    'DepartueSearchDate': date,
    'DepartueSearchTime': '8:00',        # Don't care
    'DepartueTrainCode': '',
    'DestinationSearchDate': '',
    'DestinationSearchTime': '',
    'DiscountType': ''
    } 
    req = requests.post(thsr_timetable_url, data=formdata)
    encode = req.apparent_encoding
    req.encoding = encode

    result = json.loads(req.text)
    trains = result['data']['DepartureTable']['TrainItem']
    coach_price = result['data']['PriceTable']['Coach'][0]
    print('Time table between {} -> {}'.format(start_sta, end_sta))
    print('Date: {}'.format(date))
    print('Price: {}'.format(coach_price))
    print('{:>10} {:>10} {:>12} {:>10}'.format('Train No.', 'Departure', 'Destination', 'Duration'))
    for train in trains:
        print('{:>10} {:>10} {:>12} {:>10}'.format(train['TrainNumber'], train['DepartureTime'], train['DestinationTime'], train['Duration']))