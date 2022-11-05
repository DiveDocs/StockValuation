import pandas as pd
import yfinance as yf

def getStockData(symbol):
    ticker = yf.Ticker(symbol)
    #print(ticker)
    print(symbol)
    print('CurrentPrice:',ticker.info['currentPrice'])
    #print(ticker.info['zip']
    df=ticker.earnings
    revenueList = df['Revenue']
    print('Revenue')
   #print(df['Revenue'])
    for i in range(4):
        revnow = revenueList.iloc[i]
        #print(revnow)
        if (i > 0):
            revpast = revenueList.iloc[i-1]
            print('Revenue: ', revnow, 'Growth: ', ((revnow/revpast)-1)*100, '%')
        else:
            print('Revenue: ', revnow)
    print('------------------------------------------------------------------------------------')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to the Franks Stock tool')
    print('\n------------------------------------------------------------------------------------------------')
    for symbol in ['AAPL', 'SNPS', 'GOOG']:
        getStockData(symbol)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
