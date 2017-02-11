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
    date = datetime.now().timetuple()
    year = date[0]
    month = date[1]
    day = date[2]
    payload = {'__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__LASTFOCUS':'',
    '__VIEWSTATE':'gJ3vWjzBUCxcK4FL0ZzYgN725+9Fn1UShI50Acjb3gUwAEROum/N+cevdQOLKCFyfh1Yyv4ZpsZm3dG5cq2mMbLCvTU2Gn43ZiTT9K+4UIG0zZXPgi8V59JONInSjZaDQY1k7deLYvpqEKE5qMlKrPNChWJx3gkSaUdX4Wj22y6WekKiS4MSLxWT2E2FE8UWU3Spm1T+NDQQzW16Sk1ZN16AgiTEhZB/sr+j9j145XYfISdA6QtZfPhDFX3lVfBjskwf7530rnzBbG998rUhohTGVMN9TtsrVTD2A0WfBOsWvl/qr8CTRKtto+8b9g8pquykSG2Vgxp648xM11nIkqkeuUOfxo2bgTXoNer1ptmJc7Ub9vFQTNqdC1z8vTdM6A4TGNzMLvXzMoNSxTmLz29MPVd/+5pI+ty1LKJ2qUeUwJln1MoC0W9a5JJQNZUCpeXsp4jv7OI/5aSKNQyg6fvSOs/aPIVNU3KJZYti78oIwJdlMjk2tsERrV/5TgiQRdoZemqDJttJoshLhFd76D9aZjJoAiILg07X+V8h2GKh+1fyWsKhlaQ6o3W9GiokSjEhcTv2DGyaOqPReur62ddb2oWA2UY6eTAKqC7hPua/yUw7wRJbJXuBr7CJNMgFI+SJMz6gwh6YHtd5Z+OnIAXC3a05kd26jtCPVYmkkn9UqGS80qqY8/EAsL8BGlTfArmF1W73fL8J2SpMPs+IC/tx18yKTLzpzDt3H/VDDzUExkqRIH1hUJxtzb2cYXoRA0ytsfIOJwo6BWcB2cVaaSQOSZrEzDWGSTUnbI+bHn5mYs4NpEVbTHWEbPatkL7gAewlNs3O3SBfLCsRBTDxOA/6PbJWhNz45lyGw04TMwxgWd8zt8TAXiMiQw514BCUZKzhbFRhqcQk9pnPCCUGudKNvuQ8qSP49bnRYZvIBabg5DQw7l8kF9qkBL6rSBT38PDyBu1FlyjOO7tGLBLPcxyHFcxq6lKXYby6lSgTYiEOx68NAHI7+YRlTCrV8knDdKx6EyFtm523KBGKuMgEXU/xAeennLiJWtP+loYteqnZq4Jg/BMQahCvWBRxhsfBl7mbsKTU6/D0i/IVHaYfynnpt611i74eQMaxkFyglrxYuxKpfBQgj1T5gVLWHiP4ULGx5VLAOoglcUbujVRaAQ==',
    '__VIEWSTATEGENERATOR':'67237148',
    '__EVENTVALIDATION':'92hkWXXy33uhxT73wPdbjVW7z1owq2XsOPq0qvE4P2spuF2s2r9ZwBJiCxQvliIr4dbYHnFu/mfFqpH+FVCqUYJ3Yj9neCt4hLWvg9pFUsHBbK2LMhqaKbac4KAHVSJmsyMLea9GBdB6eUBJUXgGez4PHvA0Kob8U+yAFrmQGIb/8I2q5vqy4lJPZkzAyxXc8X79rLgjy0qmZDe8TdnyFvnyeIT8N3RbK3+8wdH70lhu3jbsMFUe2HVk2bb7qOPyaRfP7vrDoTWmvZtxS4pYT6FfxBOj297js1AE49HUGxhWmvK6xSgTDy+zVQr0Ym7U/JDhTpqgxknAnyHa4ZTVwIDhzCfRO4QkJBfCyBezefA73GzgGOxtpBdukrGbyzk5EffwxxafkhKHmsMC2+T6aNCksuu1STqG/26f0xxRloCZbYZGYbze+d/S1PirmHz5M3wrxx601FZX1qVYqnGwPl09MSAjgicI0P6kgdeFj4VVert7eJnyGVuAJqg2byCYMrgIy+/XBwQnUSxWUKUZanVcey/XTEkjTMOo+G1xdXvfDq+nuQnN/iShuXsYYZEBxarku31VHm+RRsQC0IZXFPRd8b6gqai3KcpNl064MP6IjYZhbHEV9K5YMVEBxz7VpcR8h3UQyp/FlxS56ZjXCjmzAcSnx48lukvSj3n+dPcbuoKIR5Zd6UDTBdvM6vaTMgGgPjQQCJV+CyoOZea7EqM6Km+zQUHY+mgVQ3NS7zxDhhRyLVaM7Sa2uxSG58TJDYQXlacTrV2ZhWFjffbkmMUy/rkTRc+WuCVfSXM447ctId82qs6TQKwZ5d27/Nb2nSRIo3dv0/RW5alj8p9ZgIXl4Lpo8bqO6Urs1dy9UkNRzPbuGeDsJj7pjFSGd7f2m+iFG4svQUIK+4wEiuyGHHU4I3pXuw5RPoJXlVf5Zc1po9/aBdnEGQh5kwVyxnlMDKoWJ4ScgIszu40eKuoJ2v2C9/1bbYUvCB/fEFYRVU0HhnwfzbzO8O2F+TP/LEjctRh31fMFDj/JZPjq6pbGtTYIxwhYkdyigkRTTPK4couKl5g6OB35JeH0RXlA91TiZDXCY7UQ+z9ZciRlxzhKn3Waq8NhZ4MHku1nIYARFugn2nDAivJmpILz7OX75fdBlYGmxHB/uVgxWwWDszLnohTSpCeqAf+3umWfcNB4KNK0470z+EO0XQAJ84g0YCYXhKgOPh/fmMyTJJKwu/MkPA==',
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
            last_update.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    left_frame = tk.Frame(root, width=280-15, height=240-20).place(x=10, y=10)
    right_frame = tk.Frame(root, width=200-15, height=240-20).place(x=280+5, y=10)

    tk.Label(left_frame, text='IP address:').place(x=20, y=20)
    ipEntry = tk.Entry(left_frame)
    ipEntry.insert(0, ip)
    ipEntry.place(x=140, y=20)

    tk.Label(left_frame, text='check_cycle:').place(x=20, y=45)
    checkEntry = tk.Entry(left_frame)
    checkEntry.insert(0, check_cycle)
    checkEntry.place(x=140, y=45)

    tk.Label(left_frame, text='Warning Threshold:').place(x=20, y=70)
    warningEntry = tk.Entry(left_frame)
    warningEntry.insert(0, warning_threshold)
    warningEntry.place(x=140, y=70)

    tk.Label(left_frame, text='Show warning:').place(x=20, y=95)
    var = tk.IntVar()
    isWCB = tk.Checkbutton(left_frame, variable=var)
    isWCB.select()
    isWCB.place(x=140, y=95)

    download = tk.StringVar(right_frame)
    upload = tk.StringVar(right_frame)
    total = tk.StringVar(right_frame)
    last_update = tk.StringVar(right_frame)

    tk.Label(right_frame, text='Download:').place(x=295, y=20)
    tk.Label(right_frame, text='Upload:').place(x=295, y=45)
    tk.Label(right_frame, text='Total:').place(x=295, y=70)
    tk.Label(right_frame, text='Last update:').place(x=295, y=95)
    downloadLbl = tk.Label(right_frame, textvariable=download).place(x=370, y=20)
    uploadLbl = tk.Label(right_frame, textvariable=upload).place(x=370, y=45)
    totalLbl = tk.Label(right_frame, textvariable=total).place(x=370, y=70)
    updateLbl = tk.Label(right_frame, textvariable=last_update).place(x=370, y=95)

    func_arg = partial(get_data_usage, download, upload, total, last_update, ipEntry, checkEntry, warningEntry, var)
    
    t = Thread(target=get_data_usage, args=(download, upload, total, last_update, ipEntry, checkEntry, warningEntry, var,) )
    t.start()

    root.mainloop()
    #time.sleep(check_cycle)

if __name__ == '__main__':
    main()
