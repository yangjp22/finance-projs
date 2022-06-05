import pandas
import datetime
import requests
import io
import os
import pandas_datareader.data as web
import gevent
from gevent import monkey

'''
Get shares data from Web: alpha vantage

Url: https://www.alphavantage.co/documentation/

'''

# def dataFrameFromUrl(url):
#     '''
#     Parameters: 
#         Required: function
#             The time series of your choice. In this case, function=TIME_SERIES_INTRADAY

#         Required: symbol
#             The name of the equity of your choice. For example: symbol=MSFT
        
#         Required: interval
#             Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min
        
#         Optional: outputsize
#             By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call.
       
#         Optional: datatype
#             By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file.
        
#         Required: apikey
#             Your API key. Claim your free API key here.

#     Returns :daily time series (date, daily open, daily high, daily low, daily close, daily volume) of the global equity specified, covering 20+ years of historical data.

#     '''

#     dataString = requests.get(url).content
#     parseResult = pandas.read_csv(io.StringIO(dataString.decode('utf-8')), index_col = 0)
#     return parseResult


# Step 1. get the stock tickers
def getTickers():
    # step 1. get stock tickers online 
    url = 'https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
    dataString = requests.get(url).content
    tickerRawData = pandas.read_csv(io.StringIO(dataString.decode('utf-8')))
    tickers = tickerRawData['Symbol'].tolist()

    # step 2. save the ticker list to a local file
    dateToday = datetime.datetime.today().strftime('%Y%m%d')
    file = '../Data/tickerListUS/TickerList_' + dateToday +'.csv'
    tickerRawData.to_csv(file, index = False)

    return tickers


# step 2. get the intraday data for each ticker
def stockPriceIntraday(ticker, folder):
    # step 1. get intraday data online
    # url = 'https://www.alphavantage.co/query?&apikey=F5THS9QV97FEQ6YJ&function=TIME_SERIES_DAILY&symbol={ticker}&interval=1min&outputsize=full&datatype=csv'.format(
        # ticker = ticker)

    # intraday = dataFrameFromUrl(url)
    intraday = web.get_data_yahoo(ticker)

    # step 2. If the history exists, append
    file = folder + '/' + ticker + '.csv'
    if os.path.exists(file):
        history = pandas.read_csv(file, index_col = 0)
        intraday.append(history)

    # step 3. Inverse based on index
    intraday.sort_index(inplace = True)
    intraday.index.name = 'timestamp'

    # step 4. Save
    intraday.to_csv(file)


# step 3. downloading the intraday infos
def Downloader(tickers):
    for i, ticker in enumerate(tickers):
        try:
            stockPriceIntraday(ticker, folder = '../Data/tickerListUS/Intraday')
            if i % 10 == 0:
                print('Intraday for [%s] got' % str(i))
        except:
            pass


def main():
    tickers = getTickers()
    # runTh(tickers, 10)
    monkey.patch_all()

    gens = [gevent.spawn(Downloader, tickers[100 * j: 100 * (j + 1)]) for j in range(len(tickers) // 100)]
    gevent.joinall(gens)

if __name__ == "__main__":
    main()
    print('Intraday for all stocks got.')
