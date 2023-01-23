#import csv
#import requests
#import pandas as pd

"""
# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=MSFT&apikey=OZ8L0D3VDYVAOPGO'
r = requests.get(url)
data = r.json()

print ('----------------------------------- F U N D A M E N T A L   D A T A --------------------------------------------------')
print(data)

url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=OZ8L0D3VDYVAOPGO'
r = requests.get(url)
data = r.json()

print ('------------------------------ C A S H F L O W --------------------------------------------------')
print(data)
"""
"""url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=OZ8L0D3VDYVAOPGO'
r = requests.get(url)
#print(r)
data = r.json()
print(data.keys())
#print(data.values())
#print(data['annualReports'])
#with open('mycsvfile.csv', 'wb') as f:
"""
"""
    writer = csv.writer(f)
    writer.writerow(['key', 'value'])
    for annReport in data['annualReports']:
    #print(annReport)
    #print(annReport.keys())
    #print(annReport.values())
        print ('--------------------------------------------------------------------------------')
        for key, value in annReport.items():
            print(key, ':', value)
            writer.writerow([key, value]) 

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