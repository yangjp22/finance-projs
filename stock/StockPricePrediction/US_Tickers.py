import pandas
import datetime
import requests
import io


# step 1. get stock tickers online 
url = 'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
dataString = requests.get(url).content
tickerRawData = pandas.read_csv(io.StringIO(dataString.decode('utf-8')))
tickers = tickerRawData['Symbol'].tolist()

# step 2. save the ticker list to a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../Data/tickerListUS/TickerList_' + dateToday +'.csv'
tickerRawData.to_csv(file, index = False)

print(tickers)

