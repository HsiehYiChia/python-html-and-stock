import requests
from bs4 import BeautifulSoup

req = requests.get('https://www.thsrc.com.tw/index.html')
soup = BeautifulSoup(req.text, 'html.parser')

divs = soup.find_all(class_ ='revision04_title')
for div in divs:
    print(div.get("title"))
