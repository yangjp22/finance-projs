import pandas
import datetime
import tushare

# Step 1. get the stock tickers
tickerRawData = tushare.get_stock_basics()
tickers = tickerRawData.index.tolist()

# Step 2. save the ticker list to a local file
dateToday = datetime.datetime.today().strftime('%Y%m%d')
file = '../Data/tickerListCN/TickerList_' + dateToday +'.csv'
tickerRawData.to_csv(file)

print(tickers)