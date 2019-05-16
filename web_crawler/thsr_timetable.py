import time
import requests
from bs4 import BeautifulSoup
import json
import re


def get_station_hash():
    #print('getting station hash for post requests...')

    # get THSR timetable result page
    thsr_timetable_result_url = 'https://www.thsrc.com.tw/tw/TimeTable/SearchResult'
    req = requests.get(thsr_timetable_result_url)
    encode = req.apparent_encoding
    req.encoding = encode

    # parsing the page
    soup = BeautifulSoup(req.text, 'html.parser')
    stations = soup.find('select', id='StartStation')
    stations = stations.find_all('option')
    sta_hash = {}
    for sta in stations[1:]:
        hash = sta['value']
        name = sta.text
        sta_hash[name] = hash
    return sta_hash
    
def get_thsr_timetable():
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
    print('{:>10} {:>10} {:>10} {:>10}'.format('Train No.', 'Departure', 'Arrival', 'Duration'))
    for train in trains:
        print('{:>10} {:>10} {:>10} {:>10}'.format(train['TrainNumber'], train['DepartureTime'], train['DestinationTime'], train['Duration']))


def book_thsr_ticket():
    thsr_booking_url = 'https://irs.thsrc.com.tw/IMINT/'
    thsr_booking_submit_url = 'https://irs.thsrc.com.tw/IMINT/?wicket:interface=:4:BookingS1Form:1:IFormSubmitListener'
    formdata = {
        'BookingS1Form:hf:0': '',
        'selectStartStation': '2',
        'selectDestinationStation': '5',
        'trainCon:trainRadioGroup': '0',
        'seatCon:seatRadioGroup': 'radio17',
        'bookingMethod': '1',
        'toTimeInputField': '2019/05/27',
        'toTimeTable': '',
        'toTrainIDInputField': '0809',
        'backTimeInputField': '2019/05/27',
        'backTimeTable': '',
        'backTrainIDInputField': '',
        'ticketPanel:rows:0:ticketAmount': '1F',
        'ticketPanel:rows:1:ticketAmount': '0H',
        'ticketPanel:rows:2:ticketAmount': '0W',
        'ticketPanel:rows:3:ticketAmount': '0E',
        'ticketPanel:rows:4:ticketAmount': '0P',
        'homeCaptcha:securityCode': 'QZ2T',
        'SubmitButton': '開始查詢'
    } 

    headers = {'user-agent': 'My User Agent 1.0'}
    cookies = {'from-my': 'browser'}
    req = requests.get(thsr_booking_url, headers=headers, cookies=cookies)
    encode = req.apparent_encoding
    req.encoding = encode
    soup = BeautifulSoup(req.text, 'html.parser')
    img = soup.find('img')
    img_url = img.get('src')
    img_url = re.sub(';[\w=]*', '', img_url)
    url = 'https://irs.thsrc.com.tw'+img_url
    print(url)


if __name__ == '__main__':
    pass
    #get_thsr_timetable()
    book_thsr_ticket()