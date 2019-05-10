import requests
import time
import tkinter as tk
from datetime import datetime
from bs4 import BeautifulSoup
from functools import partial
from threading import Thread
import ctypes  # An included library with Python install.


url ='http://network.ntust.edu.tw/flowstatistical.aspx'

# default value of user data
ip = '140.118.170.224'
check_cycle = 300           # in second
warning_threshold = 3500    # in Mega Bytes
is_warning = True


def get_now_payload(ip):
	# first request without form data
	# parse vital form data
	get_form = requests.post(url, data={})
	soup = BeautifulSoup(get_form.text, 'html.parser')
	viewstate = soup.select("#__VIEWSTATE")[0]['value']
	eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']
	viewstategenerator = soup.select("#__VIEWSTATEGENERATOR")[0]['value']
	date = datetime.now().timetuple()
	year = date[0]
	month = date[1]
	day = date[2]
	payload = {'__EVENTTARGET':'',
	'__EVENTARGUMENT':'',
	'__LASTFOCUS':'',
	'__EVENTVALIDATION': eventvalidation,
	'__VIEWSTATE': viewstate,
	'__VIEWSTATEGENERATOR':viewstategenerator,
	'ctl00$ContentPlaceHolder1$txtip':ip,
	'ctl00$ContentPlaceHolder1$dlyear':year,
	'ctl00$ContentPlaceHolder1$dlmonth':month,
	'ctl00$ContentPlaceHolder1$dlday':day,
	'ctl00$ContentPlaceHolder1$dlcunit':'1048576',
	'ctl00$ContentPlaceHolder1$btnview':u'檢視24小時流量'}
	return payload


def get_data_usage(download, upload, total, last_update, ipEntry, checkEntry, warningEntry, var):
    while(True):
        try:
            ip = ipEntry.get()
            check_cycle = int(checkEntry.get())
            warning_threshold = int(warningEntry.get())
            if var.get():
                is_warning = True
            else:
                is_warning = False

            payload = get_now_payload(ip)
            r = requests.post(url, data=payload)
            soup = BeautifulSoup(r.text, 'html.parser')
            raw_data = soup.find_all('td')[1:4]
            data_usage = []
            for i in raw_data:
                tmp = i.text.replace(' ', '')
                tmp = tmp.replace('\r\n', '')
                #tmp = tmp.replace('(M)', '')
                data_usage.append(tmp)
            
            download.set(data_usage[0])
            upload.set(data_usage[1])
            total.set(data_usage[2])
            last_update.set(datetime.now().strftime("%Y-%m-%d %H:%M"))
            if int(data_usage[2].replace(',', '').replace('(M)', '')) > warning_threshold and is_warning:
                ctypes.windll.user32.MessageBoxW(0, "Your data usage has reach %s MB" % data_usage[2], "Data usage", 1)

            time.sleep(check_cycle)
        except:
            pass


def main():
    root=tk.Tk()

    root.minsize(width=480, height=130)
    root.maxsize(width=480, height=130)
    root.title('NTUST Network Data Usage Monitoring')
    left_frame = tk.Frame(root, width=280-15, height=130-20, bg='gainsboro').place(x=10, y=10)
    right_frame = tk.Frame(root, width=200-15, height=130-20, bg='gainsboro').place(x=280+5, y=10)

    tk.Label(left_frame, text='IP address:', bg='gainsboro').place(x=20, y=20)
    ipEntry = tk.Entry(left_frame)
    ipEntry.insert(0, ip)
    ipEntry.place(x=140, y=20)

    tk.Label(left_frame, text='Check cycle:', bg='gainsboro').place(x=20, y=45)
    checkEntry = tk.Entry(left_frame)
    checkEntry.insert(0, check_cycle)
    checkEntry.place(x=140, y=45)

    tk.Label(left_frame, text='Warning Threshold:', bg='gainsboro').place(x=20, y=70)
    warningEntry = tk.Entry(left_frame)
    warningEntry.insert(0, warning_threshold)
    warningEntry.place(x=140, y=70)

    tk.Label(left_frame, text='Show warning:', bg='gainsboro').place(x=20, y=95)
    var = tk.IntVar()
    isWCB = tk.Checkbutton(left_frame, variable=var, bg='gainsboro')
    isWCB.select()
    isWCB.place(x=140, y=95)

    download = tk.StringVar(right_frame)
    upload = tk.StringVar(right_frame)
    total = tk.StringVar(right_frame)
    last_update = tk.StringVar(right_frame)

    tk.Label(right_frame, text='Download:', bg='gainsboro').place(x=295, y=20)
    tk.Label(right_frame, text='Upload:', bg='gainsboro').place(x=295, y=45)
    tk.Label(right_frame, text='Total:', bg='gainsboro').place(x=295, y=70)
    tk.Label(right_frame, text='Last update:', bg='gainsboro').place(x=295, y=95)
    downloadLbl = tk.Label(right_frame, textvariable=download, bg='gainsboro').place(x=370, y=20)
    uploadLbl = tk.Label(right_frame, textvariable=upload, bg='gainsboro').place(x=370, y=45)
    totalLbl = tk.Label(right_frame, textvariable=total, bg='gainsboro').place(x=370, y=70)
    updateLbl = tk.Label(right_frame, textvariable=last_update, bg='gainsboro').place(x=370, y=95)

    func_arg = partial(get_data_usage, download, upload, total, last_update, ipEntry, checkEntry, warningEntry, var)
    
    t = Thread(target=get_data_usage, args=(download, upload, total, last_update, ipEntry, checkEntry, warningEntry, var,) )
    t.start()

    root.mainloop()
    #time.sleep(check_cycle)

if __name__ == '__main__':
    main()
