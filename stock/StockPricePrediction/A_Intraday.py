import pandas
import tushare
import datetime
import os
import gevent
from gevent import monkey


# Step 1. get the stock tickers
def getTickers():
    tickerRawData = tushare.get_stock_basics()
    tickers = tickerRawData.index.tolist()

    # Step 2. save the ticker list to a local file
    dateToday = datetime.datetime.today().strftime('%Y%m%d')
    file = '../Data/tickerListCN/TickerList_' + dateToday +'.csv'
    tickerRawData.to_csv(file)
    return tickers


# step 2. get the intraday data for each ticker
def stockPriceIntraday(ticker, folder):
    # step 1. get intraday data online
    intraday = tushare.get_hist_data(ticker, ktype = '5') # 5mins data

    # step 2. If the history exists, append
    file = folder + '/' + ticker + '.csv'
    if os.path.exists(file):
        history = pandas.read_csv(file, index_col = 0) # 第0列作為索引列
        intraday.append(history) 

    # step 3. Inverse based on index
    intraday.sort_index(inplace = True)
    intraday.index.name = 'timestamp'

    # step 4. Save to the file
    intraday.to_csv(file)


# step 3. downloading the intraday infos
def Downloader(tickers):

    for i, ticker in enumerate(tickers):
        try:
            stockPriceIntraday(ticker, folder = '../Data/tickerListCN/Intraday')
            if i % 10 == 0:
                print('Intraday for [%s] got' % str(i))
        except:
            pass

# step 3. get the stock price (intraday) for all using threading
# class thStickers(threading.Thread):

#     def __init__(self, parameters):
#         threading.Thread.__init__(self)
#         self.parameters = parameters

#     def run(self):
#         for i, ticker in enumerate(self.parameters):
#             try:
#                 stockPriceIntraday(ticker, folder = '../Data/tickerListCN/Intraday')
#                 if i % 100 == 0:
#                     print('Intraday for [%s] got' % str(i))
#             except:
#                 pass

# def runTh(tickers, number):
    
#     length = len(tickers)
#     numbers = length // number

#     threads = []

#     for j in range(numbers):
#         threads.append(thStickers(tickers[10 * j: 10 * (j + 1)]))

#     for each in threads:
#         each.start()

#     for each in threads:
#         each.join()

def main():
    tickers = getTickers()
    # runTh(tickers, 10)
    monkey.patch_all()

    gens = [gevent.spawn(Downloader, tickers[100 * j: 100 * (j + 1)]) for j in range(len(tickers) // 100)]
    gevent.joinall(gens)

if __name__ == "__main__":
    main()
    print('Intraday for all stocks got.')


