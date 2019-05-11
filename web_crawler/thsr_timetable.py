import requests
from bs4 import BeautifulSoup

thsr_home_url = 'https://www.thsrc.com.tw/index.html'
thsr_timetable_url = 'https://www.thsrc.com.tw/tw/TimeTable/Search'


def get_station_hash():
    req = requests.get('https://www.thsrc.com.tw/tw/TimeTable/SearchResult')
    encode = req.apparent_encoding
    req.encoding = str(encode)
    soup = BeautifulSoup(req.text, 'html.parser')
    stations = soup.find('select', id='StartStation')
    stations = stations.find_all('option')
    for sta in stations:
        print(sta['value'], sta.text)
    

get_station_hash()

formdata = {} 
req = requests.post(thsr_timetable_url, data=formdata)
