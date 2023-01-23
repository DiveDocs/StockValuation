""" 
Use alphavantage api to extract for a given ticker symbol fundamental stock data
earnings over the last 5 years and growth rate
revenue over the last 5 years and growth rate
cash flow over the last 5 years and growth rate
debt over the last 5 years and growth rate
return on equity (roe) over the last 5 years and growth rate
return on invested capital (roic) over the last 5 years and growth rate
current p/e ratio
forward p/e ratio
peg ratio
price to book ratio
current price
margin of safety
dividend yield
insider holding

https://www.alphavantage.co/documentation/#fundamental-data

3 input methods for ticker symbol
argv
file
interactive command line input


alphavantage allows for only 5 calls per minute and 500 calls per day
create a timer and every time the api is called, check the time and if it is less than 12 seconds, wait until 12 seconds have passed


create two modes for creating the pandas data frames
1. extract from internet via alphavantage api
2. read in pre-configured .csv files for testing of consecutive data processing
"""


import sys as sys
import time
import csv
import requests
import pandas as pd
import time as time 
import datetime
import xlsxwriter
import os

#OVERVIEW : dict_keys(['Symbol', 'AssetType', 'Name', 'Description', 'CIK', 'Exchange', 'Currency', 'Country', 'Sector', 'Industry', 'Address', 'FiscalYearEnd', 'LatestQuarter', 'MarketCapitalization', 'EBITDA', 'PERatio', 'PEGRatio', 'BookValue', 'DividendPerShare', 'DividendYield', 'EPS', 'RevenuePerShareTTM', 'ProfitMargin', 'OperatingMarginTTM', 'ReturnOnAssetsTTM', 'ReturnOnEquityTTM', 'RevenueTTM', 'GrossProfitTTM', 'DilutedEPSTTM', 'QuarterlyEarningsGrowthYOY', 'QuarterlyRevenueGrowthYOY', 'AnalystTargetPrice', 'TrailingPE', 'ForwardPE', 'PriceToSalesRatioTTM', 'PriceToBookRatio', 'EVToRevenue', 'EVToEBITDA', 'Beta', '52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage', 'SharesOutstanding', 'DividendDate', 'ExDividendDate'])
OVERVIEW_keys = ['Symbol', 'EBITDA', 'PERatio', 'PEGRatio', 'BookValue', 'DividendYield', 'EPS', 'RevenuePerShareTTM', 'ProfitMargin', 'OperatingMarginTTM', 'ReturnOnAssetsTTM', 'ReturnOnEquityTTM', 'AnalystTargetPrice', 'TrailingPE', 'ForwardPE', 'PriceToBookRatio', '52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage']
#BALANCE_SHEET : dict_keys(['symbol', 'annualReports', 'quarterlyReports'])
#   annualReports(['fiscalDateEnding', 'reportedCurrency', 'totalAssets', 'totalCurrentAssets', 'cashAndCashEquivalentsAtCarryingValue', 'cashAndShortTermInvestments', 'inventory', 'currentNetReceivables', 'totalNonCurrentAssets', 'propertyPlantEquipment', 'accumulatedDepreciationAmortizationPPE', 'intangibleAssets', 'intangibleAssetsExcludingGoodwill', 'goodwill', 'investments', 'longTermInvestments', 'shortTermInvestments', 'otherCurrentAssets', 'otherNonCurrentAssets', 'totalLiabilities', 'totalCurrentLiabilities', 'currentAccountsPayable', 'deferredRevenue', 'currentDebt', 'shortTermDebt', 'totalNonCurrentLiabilities', 'capitalLeaseObligations', 'longTermDebt', 'currentLongTermDebt', 'longTermDebtNoncurrent', 'shortLongTermDebtTotal', 'otherCurrentLiabilities', 'otherNonCurrentLiabilities', 'totalShareholderEquity', 'treasuryStock', 'retainedEarnings', 'commonStock', 'commonStockSharesOutstanding'])
BALANCE_keys = ['totalAssets', 'currentDebt', 'totalShareholderEquity', ]
#CASH_FLOW : dict_keys(['symbol', 'annualReports', 'quarterlyReports'])
#dict_keys(['fiscalDateEnding', 'reportedCurrency', 'operatingCashflow', 'paymentsForOperatingActivities', 'proceedsFromOperatingActivities', 'changeInOperatingLiabilities', 'changeInOperatingAssets', 'depreciationDepletionAndAmortization', 'capitalExpenditures', 'changeInReceivables', 'changeInInventory', 'profitLoss', 'cashflowFromInvestment', 'cashflowFromFinancing', 'proceedsFromRepaymentsOfShortTermDebt', 'paymentsForRepurchaseOfCommonStock', 'paymentsForRepurchaseOfEquity', 'paymentsForRepurchaseOfPreferredStock', 'dividendPayout', 'dividendPayoutCommonStock', 'dividendPayoutPreferredStock', 'proceedsFromIssuanceOfCommonStock', 'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet', 'proceedsFromIssuanceOfPreferredStock', 'proceedsFromRepurchaseOfEquity', 'proceedsFromSaleOfTreasuryStock', 'changeInCashAndCashEquivalents', 'changeInExchangeRate', 'netIncome'])
CASHFLOW_keys = ['operatingCashflow']
#INCOME_STATEMENT : dict_keys(['symbol', 'annualReports', 'quarterlyReports'])
#dict_keys(['fiscalDateEnding', 'reportedCurrency', 'grossProfit', 'totalRevenue', 'costOfRevenue', 'costofGoodsAndServicesSold', 'operatingIncome', 'sellingGeneralAndAdministrative', 'researchAndDevelopment', 'operatingExpenses', 'investmentIncomeNet', 'netInterestIncome', 'interestIncome', 'interestExpense', 'nonInterestIncome', 'otherNonOperatingIncome', 'depreciation', 'depreciationAndAmortization', 'incomeBeforeTax', 'incomeTaxExpense', 'interestAndDebtExpense', 'netIncomeFromContinuingOperations', 'comprehensiveIncomeNetOfTax', 'ebit', 'ebitda', 'netIncome'])
INCOME_keys = ['grossProfit', 'totalRevenue', 'operatingIncome', ]
#EARNINGS : dict_keys(['symbol', 'annualEarnings', 'quarterlyEarnings'])
#dict_keys(['fiscalDateEnding', 'reportedEPS'])
EARNINGS_keys = ['reportedEPS']

strlist =['OVERVIEW', 'CASH_FLOW', 'BALANCE_SHEET', 'INCOME_STATEMENT', 'EARNINGS']
annualkey = ['','annualReports', 'annualReports', 'annualReports', 'annualEarnings']


#global variables to control whether data is 
# extract_mode == 1: extracted via api calls, else read from file
# process_mode == 1: processed to create rule1 data else do nothing
# write_mode == 1: write_to_excel else write to csv
extract_mode = 'FILE'  #'FILE', 'ALPHA'
process_mode = 'RULE1' #'RULE1, NOTHING ELSE FOR NOW
write_mode = 'EXCEL'   #'EXCEL', 'CSV'

current_time = 0
last_call = time.time() - 12
sleep_intervals =[12,60]

def sleep():
    #this is a helper function to ensure that alphavantage API is only called 5 times / minute
    # 
    """global current_time
    global last_call
    current_time = time.time()
    if current_time - last_call < 12:
        time.sleep(12 - (current_time - last_call))
    last_call = time.time()
    """

def prefix_year(annReport):
    year = annReport['fiscalDateEnding'][0:4]
    return year

def request_ticker_information(symbol, key):
    url = 'https://www.alphavantage.co/query?function=' + key + '&symbol='+symbol+'&apikey=OZ8L0D3VDYVAOPGO'
    
    #continuously request data from API until error code 200 is returned
    while(True):
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            print(f'Error: {response.status_code}, Message: {response.text}')
            exit()
        elif "Note" in data:
            status = data["Note"]
            print(f'Sleeping for 12 seconds due to alphavantage timout error! {status}')
            time.sleep(12)
        else:
            break

    return data

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
def print_current_stock_price(symbol, df):
    sleep()
    data= request_ticker_information(symbol, 'GLOBAL_QUOTE')
    df.at['CurrentPrice', 'Overview'] = data['Global Quote']['05. price']

def print_overview_data(symbol, df):
    print('Extracting ' + 'OVERVIEW:')
    sleep()

    data =  request_ticker_information(symbol, 'OVERVIEW')
    for key in OVERVIEW_keys:
        #add a key-value pair
        df.at[key, 'Overview'] = data[key]
        #print(key, ":", data[key])
    
def print_balance_data(symbol, df):
    print('Extracting ' + 'BALANCE SHEET:')
    #print('B A L A N C E    S H E E T:')
    sleep()
    data = request_ticker_information(symbol, 'BALANCE_SHEET')

    for annReport in data['annualReports']:
        year = prefix_year(annReport)
        #print(year)
        for key in BALANCE_keys:
            df.at[key, year] = annReport[key]
            #print(key, ":", annReport[key])

def print_income_data(symbol, df):
    print('Extracting ' + 'INCOME STATEMENT:')
    #print('I N C O M E   S T A T E M E N T:')
    sleep()
    data= request_ticker_information(symbol, 'INCOME_STATEMENT')
    
    for annReport in data['annualReports']:
        #extract the year out of the key value pair 'fiscalDateEnding'
        year = prefix_year(annReport)
        #print(year)
        for key in INCOME_keys:
            df.at[key, year] = annReport[key]
            #print(key, ":", annReport[key])

def print_cashflow_data(symbol, df):
    print('Extracting ' + 'CASHFLOW:')
    #print('C A S H   F L O W:')
    sleep()
  
    data = request_ticker_information(symbol, 'CASH_FLOW')   
    
    for annReport in data['annualReports']:
        year = prefix_year(annReport)
        #print(year)
        for key in CASHFLOW_keys:
            df.at[key, year] = annReport[key]
            #print(key, ":", annReport[key])

def print_earnings_data(symbol, df):
    print('Extracting ' + 'CASHFLOW:')
    #print('E A R N I N G S:')

    data = request_ticker_information(symbol, 'EARNINGS')
    
    for annReport in data['annualEarnings']:
        year = prefix_year(annReport)
        #print(year)
        for key in EARNINGS_keys:
            df.at[key, year] = annReport[key]
            #print(key, ":", annReport[key])
    
def initialize_pandas_data_frame():
    #columns = ['Overview', '2022', '2021', '2020', '2019', '2018']
    columns = ['Overview']
    df = pd.DataFrame(columns=columns)
    #print (df)
    #print (df)
    return df

def write_fundamental_data_to_excel(symbol_data):
    # Create an Excel writer object
    #make the file name unique by adding the current time

    file_prefix = "fundamentals"
    directory = "stockdata"

    if not os.path.exists(directory):
        print('Cannot find local directory '+directory+', creating it!!!')    
        os.makedirs(directory)

    # do something with the file
    # Get the current time
    now = datetime.datetime.now()

    # Format the time as a string
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")

    file_path = os.path.join(directory, file_prefix + '_' + timestamp + '.xlsx')
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter')

    # Write each DataFrame in the dictionary to a separate worksheet/tab in the Excel file
    for symbol, df in symbol_data.items():
        df.to_excel(writer, sheet_name=symbol)

    # Save the Excel file
    writer.close()

def write_fundamental_data_to_csv(symbol_data):
    # Create an Excel writer object
    #make the file name unique by adding the current time

    directory = "stockdata"

    if not os.path.exists(directory):
        print('Cannot find local directory '+directory+', creating it!!!')    
        os.makedirs(directory)

    # write each dictionary item (symbol, df) to its own csv file named symbol.csv in the directory
    for symbol, df in symbol_data.items():
        file_path = os.path.join(directory, symbol + '.csv')
        df.to_csv(file_path)

def read_fundamental_data(symbols, symbol_data):
    #read each csv file into a dataframe and add it to the dictionary
    for symbol in symbols:
        file_path = os.path.join('stockdata', symbol + '.csv')
        df = pd.read_csv(file_path, index_col=0)
        symbol_data[symbol] = df

def extract_fundamental_data(symbols, symbol_data):
    for symbol in symbols:
        print('Fundamental data for symbol: ' + symbol)
        ed = pd.DataFrame()
        ed = initialize_pandas_data_frame()
        print_current_stock_price(symbol, ed)
        print_overview_data(symbol, ed)
        print_balance_data(symbol, ed)
        print_income_data(symbol, ed)
        print_cashflow_data(symbol, ed)
        #print_earnings_data(symbol, ed)
        ed = ed.sort_index(axis=1, ascending=False)
        #print(ed)
        #ensure this iteration happens only once a minute
        #time.sleep(60)

        #add the data to a dictionary of 'Symbol': 'Dataframe'
        symbol_data[symbol] = ed
        #print(symbol_data)


def process_fundamental_data(symbol_data):
    return

def main(sys):
    #print ('Entering Main Function')
    #print (sys.argv, ' arguments passed in')
    symbols = []
    symbol_data = {}

    if len(sys.argv) == 1:
        symbol = 'AAPL'
        #add symbol to symbols
        symbols.append(symbol)
    else:
        #iterate through the list of symbols passed in as arguments
        #print(len(sys.argv))
        for i in range(1,len(sys.argv)):
            #print('Argv Iteration ', i)
            symbol = sys.argv[i]
            #print(symbol)
            symbols.append(symbol)
    
    print(symbols)
    if extract_mode == 1:
        extract_fundamental_data(symbols, symbol_data)
    else:
        read_fundamental_data(symbols, symbol_data)

    if process_mode == 1:
        process_fundamental_data(symbols, symbol_data)
    #else do nothing

    if write_mode == 1:
        write_fundamental_data_to_excel(symbol_data)
    else: write_fundamental_data_to_csv(symbol_data)

    

#------------------------------------------ MAIN ------------------------------------------

#call the main function
if __name__ == "__main__":
    main(sys)


"""
url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=OZ8L0D3VDYVAOPGO'
r = requests.get(url)
data = r.json()

print ('------------------------------ C A S H F L O W --------------------------------------------------')
print(data)

#Balance Sheet, I want: totalLiability, currentDept, 
for info in strlist:
    url = 'https://www.alphavantage.co/query?function=' + info + '&symbol=IBM&apikey=OZ8L0D3VDYVAOPGO'
    r = requests.get(url)
    #print(r)
    data = r.json()
    print(info, ":", data.keys())
    print(info, ":", data[annualkey[strlist.index(info)]])
    print ('--------------------------------------------------------------------------------')

    #print(data.values())
    #print(data['annualReports'])
    with open('mycsvfile.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["key", "value"])
        i= 0
        #print(r)
        for annReport in data['annualReports']:
            #print(annReport)
            if i == 0:
                print(annReport.keys()) 
            i=i+1
            #print(annReport.values())
   
        print ('--------------------------------------------------------------------------------')
        for key, value in annReport.items():
            print(key, ':', value)
            writer.writerow([key, value]) 
"""
#with open('mycsvfile.csv', 'wb') as f:  # You will need 'wb' mode in Python 2.x
#    w = csv.writer(f)
#    w.writerow(data.keys())
#    w.writerow(data.values())
#df = pd.read_json ("./test.json")
#df.to_csv ("./test.csv", index = None)

#data.to_csv("./test.csv")
#print ('----------------------------------- B A L A N C E   S H E E T --------------------------------------------------')
#print(data)

"""
url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=OZ8L0D3VDYVAOPGO'
r = requests.get(url)
data = r.json()

print ('----------------------------------- I N C O M E   S T A T E M E N T --------------------------------------------------')
print(data)

url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=MSFT&apikey=OZ8L0D3VDYVAOPGO'
r = requests.get(url)
data = r.json()

print ('----------------------------------- E A R N I N G S --------------------------------------------------')
print(data)
"""


"""
create a list of even numbers

"""
