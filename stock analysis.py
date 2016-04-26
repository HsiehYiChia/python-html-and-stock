from yahoo_finance import Share
import sqlite3
from datetime import date, timedelta
import matplotlib.pyplot as plt

conn = sqlite3.connect('stock.db')
cursor = conn.cursor()


def historical_to_db(symbol, start, end):
	stock = Share(symbol)
	historical = stock.get_historical(start, end)
	for i in historical:
		try:
			conn.execute('INSERT INTO SharePrice VALUES (?,?,?,?,?,?,?);', (i['Date'], i['Symbol'], i['Open'], i['Close'], i['High'], i['Low'], i['Volume']))
		except sqlite3.IntegrityError:
			pass

	conn.execute("UPDATE Stock SET End = (?) WHERE Symbol = (?) ", (end, symbol))
	print(symbol + " SharePrice update finish")


def add_stock_to_db(symbol):
	stock = Share(symbol)
	info = stock.get_info()
	print ('The stock you add ', info)
	try:
		print
		conn.execute('INSERT INTO Stock VALUES (?,?,?,?);', (info['symbol'], info['start'], info['end'], info['CompanyName']))
		historical_to_db(info['symbol'], info['start'], info['end'])
	except sqlite3.IntegrityError:
		print ("The stock already exist")
	

def update_price_to_db():
	for row in cursor.execute("SELECT Symbol, End FROM Stock;"):
		historical_to_db(row[0], row[1], Share(row[0]).get_info()['end'])


def get_moving_avg(symbol, avg_day, date = date.today()):
	cursor.execute('SELECT Close FROM SharePrice WHERE Symbol = (?) and Date <= (?) ORDER BY DATE DESC', (symbol,date))
	sigma = .0
	for row in cursor.fetchmany(avg_day):
		sigma += float(row[0])
	return sigma/avg_day


if __name__ == '__main__':
	#update_price_to_db()
	all_avg = []
	index = []
	for i in range(1000):
		avg = get_moving_avg('0050.TW', 120, date.today()-timedelta(days=i))
		index.append(i)
		all_avg.append(avg)

	all_avg.reverse()
	plt.plot(all_avg)
	plt.grid(True)
	plt.title('Moving Average')
	plt.xlabel('Time')
	plt.ylabel('Price')
	#plt.ylim([50,75])
	plt.xticks()
	plt.show()



conn.commit() 
conn.close()

