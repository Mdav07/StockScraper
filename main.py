import requests
from bs4 import BeautifulSoup as bs
from operator import itemgetter
import tkinter as tk
from tkinter import ttk
from yahooquery import search

#Makes the window
def gui(x):
    columns = ["Company","Ticker","Stock Price","Percent Gained","Market Cap (In Millions)"]
    root = tk.Tk()
    root.title("Stock Data")
    tree = ttk.Treeview(root,columns=columns,show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col,width=100)
    for row in x:
        tree.insert("",tk.END,values=row)
    tree.pack(expand=True,fill="both")
    root.mainloop()
#Gets rid of any stock under 25 million market cap
def checkMarketCap(text):
    if "M" in text:
        noM = text.replace("M","")
        clean = noM.replace(",","")
        if(int(clean)>=25):
            return clean
        else:
            return "fail"
    else:
        return "fail"
#Ensures that the stock is over 3 dollars
def price(price):
    if "," in price:
        price = price.replace(",","")
        return(float(price))
    else:
        return(float(price))
        
#Gets the webpages
pages = []
for number in range(1,8):
    start = 'https://www.centralcharts.com/en/price-list-ranking/'
    end = 'ALL/desc/ts_19-us-nasdaq-stocks--qc_2-daily-change?p='
    link = start + end + str(number)
    pages.append(link)

#Gets the ticker for the company
def getTicker(name):
    result = search(name)
    if 'quotes' in result and result['quotes']:
        return result['quotes'][0]['symbol']
    return None

#Gets the data from the website and adds it
values = []
for page in pages:
    web = requests.get(page)
    soup = bs(web.text,'html.parser')

    stocktable = soup.find('table', class_='tabMini tabQuotes')
    trlist = stocktable.find_all('tr')

    for rows in trlist[1:]:
        tdlist = rows.find_all('td')

        rowValues = []
        for td in tdlist[0:8]:
            newValue = td.text.strip()
            rowValues.append(newValue)
        if(price(rowValues[1])>3):
            if(checkMarketCap(rowValues[7])!="fail"):
                rowValues[2]= rowValues[2][1:]
                rowValues[7] = checkMarketCap(rowValues[7])
                values.append(rowValues)

#Sorts the list and then gets rid of excess values
sorted(values,key=itemgetter(2))
final = []
for x in values:
    temp = []
    temp.append(x[0])
    temp.append(str(getTicker(x[0])))
    temp.append(x[1])
    temp.append(x[2])
    temp.append(x[7])
    final.append(temp)
    
#Sends the list of lists to be fed into the window maker
gui(final)
