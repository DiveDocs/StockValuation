
import pandas as pd
import yfinance as yf
def getFundamentals(df, str):
    dataList = df[str]  #type is of type string, either Revenue or Earnings

def printGrowthList(df, title):
    print(title)
    list =df[title]
    for i in range(4):
        now = list.iloc[i]
        if (i > 0):
            past = list.iloc[i - 1]
            if (past == 0):
                if now > 0: 
                    print(title, ': ', '${:,.2f}'.format(now),'Infinity')
                else: print(title, ': ', '${:,.2f}'.format(now),'-Infinity')
            elif past > 0:
                print(title, ': ', '${:,.2f}'.format(now), 'Growth: ', "{:.2%}". format((now / past) - 1))
            else:
                print(title,': ', '${:,.2f}'.format(now), 'Growth: ', "{:.2%}". format(1-(now / past)))
        else:
            print(title, ': ', '${:,.2f}'.format(now))


def getStockData(symbol):
    print(symbol)
    ticker = yf.Ticker(symbol)
    
    print(ticker)
    df = ticker.info
    print(df['fiftyTwoWeekLow'])
    #df = pd.DataFrame.from_dict(dict, orient='index')
    #df = df.reset_index()
    #print(df)

    #Now grab all kind of relevant information we need later on
    low52 = df['fiftyTwoWeekLow']
    high52 = df['fiftyTwoWeekHigh']
    curr = df['currentPrice']

    print('52L: ', low52,  '/ Current: ', curr, '/ 52H', high52)
    cf = df['operatingCashflow']
    dbt = df['totalDebt']
    tc = df['totalCash']
    fpe = df['forwardEps']
    tpe = df['trailingEps']
    print('CashFlow: ', '${:,.2f}'.format(cf),  'vs. Debt: ', '${:,.2f}'.format(dbt), ': ', "{:.2%}". format(cf/dbt))
    print('Cash: ', '${:,.2f}'.format(cf),  'vs. Debt: ', '${:,.2f}'.format(dbt), ': ', "{:.2%}". format(tc/dbt))
    fpe = df['forwardEps']
    tpe = df['trailingEps']
    print('forwardEps: ', fpe,  'vs. trailingEPS: ', tpe)
    ldv = df['lastDividendValue']
    if ldv:
        print('Dividend/CurrentPrice: ', "{:.2%}".format(ldv/curr))
    else:
        print('No Dividend reported')
    peg = df['pegRatio']
    print('PEG Ratio: ', peg)
    roe = df['returnOnEquity']
    print('ROE: ', roe)
    #roic = ticker.calculate_roic()
    #print('ROIC: ', roic)
    
    df=ticker.earnings
    #print(df)
    printGrowthList(df, 'Revenue')
    printGrowthList(df, 'Earnings')
    #df=ticker.get_cashflow()
    df=ticker.cashflow
    print(df)
    print(ticker.info['operatingCashFlow'])
    print(df['operatingCashFlow'])
    printGrowthList(ticker, 'OperatingCashFlow')

    print('-------------------------------------------------------------------------------------------')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Welcome to the Franks Stock tool')
    print('\n------------------------------------------------------------------------------------------------')
    for symbol in ['AAPL', 'SNPS', 'ZS']:
        getStockData(symbol)


"""
   revenueList = df['Revenue']
   print('Revenue')
#   # print(df['Revenue'])
#   for i in range(4):
#       revnow = revenueList.iloc[i]
#       # print(revnow)
#       if (i > 0):
#           revpast = revenueList.iloc[i - 1]
#           print('Revenue: ', '${:,.2f}'.format(revnow), 'Growth: ', "{:.2%}". format((revnow / revpast) - 1))
#       else:
#           print('Revenue: ', '${:,.2f}'.format(revnow))
#   
#    earningsList = df['Earnings']
#    print('Earnings')
#    # print(df['Earnings'])
#    for i in range(4):
#        earnnow = earningsList.iloc[i]
#        # print(revnow)
#        if (i > 0):
#            earnpast = earningsList.iloc[i - 1]
#            if (earnpast == 0):
#                if earnnow > 0: 
#                    print("Infinity"
#               else: print("-Infinity")
#           elif earnpast > 0:
#               print('Earning: ', '${:,.2f}'.format(earnnow), 'Growth: ', "{:.2%}". format((earnnow / earnpast) - 1))
#           else:
#               print('Earning: ', '${:,.2f}'.format(earnnow), 'Growth: ', "{:.2%}". format(1-(earnnow / earnpast)))
#       else:
#           print('Earning: ', '${:,.2f}'.format(earnnow))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""