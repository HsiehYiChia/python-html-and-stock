import requests
from bs4 import BeautifulSoup
url ='http://www.thsrc.com.tw/tw/TimeTable/SearchResult'
payload = {
	'StartStation':'977abb69-413a-4ccf-a109-0272c24fd490',
	'EndStation':'3301e395-46b8-47aa-aa37-139e15708779',
	'SearchDate':'2016/04/29',
	'SearchTime':'09:30',
	'SearchWay':'DepartureInMandarin',
	'RestTime':'',
	'EarlyOrLater':''
}

r = requests.post(url, data=payload)

soup = BeautifulSoup(r.text,'html.parser')
print (soup.select('#StartStation'))



