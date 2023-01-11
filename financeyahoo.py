from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import yfinance as yf

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


def write_file(fname: object, str: object) -> object:
    file = open(fname, 'w')
    file.write(str)
    file.close()

def get_html_str(ticker, substr):
    url = 'https://finance.yahoo.com/quote/'+ticker+'/'+substr
    print(url)
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')

    #print(soup)
    return(soup)

def get_stock_summary(soup):
    main_header = soup.find('div', id = "quote-summary")
    tables = main_header.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
                #print(row.text)
                datasets = row.find_all('td')
                i=0

                #How to define two strings so that they have scope in both if and else branch below
                #ToDo: I could not find any other way to seperate the title from the value in row.text other than using a counter of i ni 0,1
                title = ""
                value = ""
                for data in datasets:
                    if (i == 0):
                        title = data.text
                        i= i + 1
                    else:
                        value = data.text
                        print (title + ': \t\t' +  value)
                        i = 0


def get_stock_financials(soup):
#get revenue for pas 5 years
    #navigate to the Income Statement table
    income_statement = soup.find('span', string = 'Income Statement')
    financial_table_header = income_statement.find_next('div', class_ = 'D(tbhg)')
    #print(financial_table_header.text)
    financial_table_contents = financial_table_header.find_all_next('div', class_ = 'D(tbr)')
    for row in financial_table_contents:
        entries=row.find_all_next('span', limit=6)
        for entry in entries:
            if (entry):
                print(entry.text, end=' ')
        print()
    #Some statistics
    headings = soup.find_all('div', class_='D(tbhg)')
    rows     = soup.find_all('div', class_='D(tbrg)')
    print(len(headings))
    print(len(rows))

def get_stock_financials_1(soup):
#get revenue for past 5 years
    headings = soup.find_all('div', class_='D(tbhg)')
    for heading in headings:
        print(heading.find_next('span').text)
    rows     = soup.find_all('div', 'fin-row')
    print(len(rows))


def get_stock_balance(soup):
#get revenue for pas 5 years
    #navigate to the Income Statement table
    income_statement = soup.find('span', string = 'Balance Sheet')
    financial_table_header = income_statement.find_next('div', class_ = 'D(tbhg)')
    #print(financial_table_header.text)
    financial_table_contents = financial_table_header.find_all_next('div', class_ = 'D(tbr)')
    for row in financial_table_contents:
        entries=row.find_all_next('span', limit=5)
        for entry in entries:
            if (entry):
                print(entry.text, end=' ')
        print()


def get_value_pair(soup, search_string, len_data):
    entry = soup.find('span', string = search_string)
    print(entry)
    if (entry):
        datas = entry.find_all_next('td', limit=len_data)
        for data in datas:
            print (entry.text +': '+ data.text)

def getTickerData(symbol):
    ticker = yf.Ticker(symbol)
    print(ticker.info)


#This is the main routine
ticker = 'SNPS'
soup = get_html_str(ticker,'summary')
write_file(ticker + '.txt', soup.text)
get_stock_summary(soup)
get_value_pair(soup, 'Previous Close', 1)
soup = get_html_str(ticker,'financials')
get_stock_financials(soup)
#soup = get_html_str('SNPS','balance-sheet')
#get_stock_balance(soup)

getTickerData(ticker)

#create a random list of 10 numbers
nums = [0,1,2,3,4,5,6,7,8,9]