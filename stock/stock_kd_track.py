from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
import numpy as np
import pandas as pd
from pandas import DataFrame
import talib as ta
import smtplib # Import smtplib for the actual sending function
from email.mime.text import MIMEText # Import the email modules we'll need
from datetime import datetime, date

def Get_kd(data):
    indicators={}
    # calculate KD
    indicators['k'],indicators['d']=ta.STOCH(np.array(data['High']),np.array(data['Low']),np.array(data['Close']),fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)
    indicators=pd.DataFrame(indicators)
    return indicators

# credit from https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ("successfully sent the mail")
    except:
        print ("failed to send mail")







if __name__ == "__main__":

    # get price data (return pandas dataframe)
    param = {
	'q': "0050.TW", # Stock symbol (ex: "AAPL")
	'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
	#'x': "TWSE", # Stock exchange symbol on which stock is traded (ex: "NASD")
	'p': "2Y" # Period (Ex: "1Y" = 1 year)
    }
    price_df = get_price_data(param)
    print (price_df)

    # calculate KD
    kd = Get_kd(price_df)
    print (kd)

    today_price = price_df.tail(1)
    user = ""
    pwd = ""
    recipient = [""]
    subject = "%s KD analysis of 0050.TW" % date.today()
    body = """
    %s
    0050.TW
    Open: %d
    High: %d
    Low: %d
    Close: %d
    K: %d
    D: %d
    """ % (date.today(), today_price["Open"], today_price["High"], today_price["Low"], today_price["Close"], kd['k'][kd.index[-1]], kd['d'][kd.index[-1]])

    if kd['k'][kd.index[-1]] > 80 or kd['k'][kd.index[-1]] < 20:
        print ("k>80 or k<20, sent email to %s" % user)
        send_email(user, pwd, recipient, subject, body)
