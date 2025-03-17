import requests
from bs4 import BeautifulSoup as bs
from operator import itemgetter
import tkinter as tk
from tkinter import ttk

def gui(x):
    columns = ["Company","Stock Price", "Percent Gained"]
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

def price(price):
    if "," in price:
        price = price.replace(",","")
        return(float(price))
    else:
        return(float(price))

pages = []
for number in range(1,7):
    start = 'https://www.centralcharts.com/en/price-list-ranking/'
    end = 'ALL/desc/ts_19-us-nasdaq-stocks--qc_2-daily-change?p='
    link = start + end + str(number)
    pages.append(link)

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

sorted(values,key=itemgetter(2))
final = []
for x in values:
    temp = []
    temp.append(x[0])
    temp.append(x[1])
    temp.append(x[2])
    final.append(temp)

gui(final)