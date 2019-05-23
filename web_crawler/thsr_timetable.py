import os
import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup
import json
import re
import cv2
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


def get_station_hash():
    # get THSR timetable result page
    thsr_timetable_result_url = 'https://www.thsrc.com.tw/tw/TimeTable/SearchResult'
    req = requests.get(thsr_timetable_result_url)
    req.encoding = req.apparent_encoding

    # parse to get station hash for post requests in get_thsr_timetable
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
    req.encoding = req.apparent_encoding

    result = json.loads(req.text)
    trains = result['data']['DepartureTable']['TrainItem']
    coach_price = result['data']['PriceTable']['Coach'][0]
    print('Time table between {} -> {}'.format(start_sta, end_sta))
    print('Date: {}'.format(date))
    print('Price: {}'.format(coach_price))
    print('{:>10} {:>10} {:>10} {:>10}'.format('Train No.', 'Departure', 'Arrival', 'Duration'))
    for train in trains:
        print('{:>10} {:>10} {:>10} {:>10}'.format(train['TrainNumber'], train['DepartureTime'], train['DestinationTime'], train['Duration']))


def get_secyrityCode_img():
    print('Images will be saved in security_code_image/ folder')
    print('Maximum 600 images can be fetched for single run')
    try:
        os.mkdir('security_code_image')
        print('create security_code_image/ folder')
    except:
        pass


    # use session because we need to use cookies
    thsr_booking_url = 'https://irs.thsrc.com.tw/IMINT/'
    session = requests.Session()
    headers = {'user-agent': 'My User Agent 1.0'}
    cookies = {'from-my': 'browser'}
    
    for i in range(0, 600):
        # get html of booking ticket page
        req = session.get(thsr_booking_url, headers=headers, cookies=cookies)
        req.encoding = req.apparent_encoding

        # parse security code image url
        soup = BeautifulSoup(req.text, 'html.parser')
        img = soup.find('img')
        img_url = img.get('src')
        img_url = re.sub(';[\w=]*', '', img_url)
        img_url = 'https://irs.thsrc.com.tw'+img_url
        print(i, img_url)
        req = session.get(img_url, headers=headers, cookies=cookies)
        with open('security_code_image/'+str(i)+'.png', 'wb') as file:
            file.write(req.content)
            file.flush()

def de_noise_and_curveline(src):
    denoise_img = cv2.fastNlMeansDenoisingColored(src, None, 30, 10, 7, 21)
    ret, thresh_img = cv2.threshold(denoise_img, 127, 255, cv2.THRESH_BINARY_INV)

    # take only first 5 and last 5 column for curve line regression
    imgarr = cv2.cvtColor(thresh_img, cv2.COLOR_BGR2GRAY)
    imgarr[:, 5:-5] = 0
    imagedata = np.where(imgarr == 255)

    # create polynominal regression 
    height, width = imgarr.shape
    X = np.array([imagedata[1]])
    Y = height - imagedata[0]
    poly_reg = PolynomialFeatures(degree=2)
    X_ = poly_reg.fit_transform(X.T)
    regr = LinearRegression().fit(X_, Y)
    
    X2 = np.array([[i for i in range(0,width)]])
    X2_ = poly_reg.fit_transform(X2.T)
    curve_line_img = np.zeros((height, width, 1), np.uint8)
    dst =  cv2.cvtColor(thresh_img, cv2.COLOR_BGR2GRAY)
    for ele in np.column_stack([regr.predict(X2_).round(0),X2[0],] ):
        pos = height-int(ele[0])
        curve_line_img[pos-3:pos+3,int(ele[1])] = 255
        dst[pos-3:pos+3,int(ele[1])] = 255 - dst[pos-3:pos+3,int(ele[1])]

    return dst

def train_security_code_model(images_path):
    try:
        os.mkdir('pre_processed')
    except:
        pass
        
    for i in range(0, 600):
        src_path = images_path+str(i)+'.png'
        dst_path = 'pre_processed/'+str(i)+'.png'
        print('training', src_path)
        src = cv2.imread(src_path, cv2.IMREAD_COLOR)
        
        dst = de_noise_and_curveline(src)
        cv2.imwrite(dst_path, dst)

        cv2.imshow("Original Img", src)
        cv2.imshow("dst", dst)
        cv2.waitKey(500)
    cv2.destroyAllWindows()

        

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timetable',
        action='store_true', default=False, dest='timetable', help='get time table of THSR')
    parser.add_argument('-g', '--get_sec',
        action='store_true', default=False, dest='get_sec', help='get security code images for training')
    parser.add_argument('-T', '--train_sec',
        action='store_true', default=False, dest='train_sec', help='train security code recognition model')
    parser.add_argument('-b', '--book_ticket',
        action='store_true', default=False, dest='book_ticket', help='book THSR ticket')
    args = parser.parse_args()

    
    if args.timetable == True:
        get_thsr_timetable()
    if args.get_sec == True:
        get_secyrityCode_img()
    if args.train_sec == True:
        train_security_code_model('security_code_image/')
    if args.book_ticket == True:
        book_thsr_ticket()
    if len(sys.argv) <= 1:
        parser.print_help()

    
