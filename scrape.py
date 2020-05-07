# Author: Christian Vartanian
# Description: General Scraper tailored for Yahoo Japan Auction Search Results
# Current Feature Set: Price, Title, Time Remaining, Current Bidders, Optional Translator, CSV Output
# TODO: Scrape more data into CSV, stabilize system past 15000 results

import html5lib
import bs4 as bs
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
import time


filename = "JOCKreport.csv"
f = open(filename,"w")

#Translator Flag, will crash if turned on and running 10K+ results

TFlag = 0
if TFlag == 1:
  headers = "Product_Name, Product_Name_English, Price_In_Yen, Time_Remaining, Bidders, ID, Link \n"
else:
  headers = "Product_Name, Price_In_Yen, Time_Remaining, Bidders, ID, Link \n"
  
f.write(headers)

SEARCH = "Comme Des Garcon"

#PARSE AUCTIONS FIRST
URL = "https://auctions.yahoo.co.jp/search/search?p=" + SEARCH + "&va="+SEARCH+"&fixed=2&exflg=0&b=1&n=100"
r=requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
searchtab = soup.find_all("span",{"class":"Tab__subText"})
auctionmax = searchtab[1]
binmax = searchtab[2]
binmaxint = int(binmax.text.replace("件","").replace(",",""))
auctionmaxint = int(auctionmax.text.replace("件","").replace(",",""))
print(auctionmaxint)
print(binmaxint)

if auctionmaxint >= 15000:
  functamax = 15000
else:
  functamax = auctionmaxint

if binmaxint >= 15000:
  functbmax = 15000
else:
  functbmax = binmaxint

#Initialize page shift index variable
page=1

#Begin Auction Only Parse
while page < functamax:
  pagestr=str(page)
  URL = "https://auctions.yahoo.co.jp/search/search?p=" + SEARCH + "&va="+SEARCH+"&fixed=2&exflg=0&b=" + pagestr + "&n=100"
  r=requests.get(URL)
  soup = BeautifulSoup(r.content, 'html5lib')
  products = soup.find_all("li",{"class":"Product"})
  titles = soup.find_all("a",{"class":"Product__titleLink"})

  translator = Translator()

  for entry in products:
    if page >= functamax-100  and functamax % 100 != 0:
      break 
    #hunt price
    price = entry.find_all("span", {"class":"Product__priceValue u-textRed"})
    pricec = price[0]

    #hunt price
    bprice = entry.find_all("span", {"class":"Product__priceValue"})
    bpricec = bprice[0]
    
    #hunt title
    title = entry.find_all("a", {"class":"Product__titleLink"})
    titlec = title[0]

    #hunt time remaining
    timel = entry.find_all("span", {"class":"Product__time"})
    timec = timel[0]

    #hunt bidders
    bids = entry.find_all("span", {"class":"Product__bid"})
    bidc = bids[0]

    #Prep for output
    Pout = pricec.text
    Tout = titlec["title"]
    Bout = bpricec.text
    BdOut = bidc.text
    TiOut = timec.text.replace('日'," Days").replace('時間'," Hours").replace('分'," Minutes ").replace('秒'," Seconds ")
    Lout = titlec["href"]
    IdOut = Lout.replace("https://page.auctions.yahoo.co.jp/jp/auction/","") #Auction ID Output Only
    
    if TFlag == 1:
    #Translate Titles
      EnOut = translator.translate(Tout, src='ja')
      EnOutStr = str(EnOut)
      EnOutStripped = EnOutStr.replace("Translated(src=ja, dest=en, text=","").replace(", pronunciation=None, extra_data=","").replace('"',"").replace("{'translat...)","").replace("Jippuappupaka","")

    # print outputs
    print(Tout)
    if TFlag == 1:
      print(EnOutStripped)
    print("Current Price in Yen " + pricec.text)
    

    print(TiOut)
    print(BdOut + " Bidders")
    print(Lout)
    print(page)
    
    
    print("\n")
    
    if TFlag == 1:
      f.write(Tout.replace(",", "|") + "," + EnOutStripped + "," + Pout.replace(",", "").replace("円","") + "," + IdOut + "," + Lout + "\n")
    else:
      f.write(Tout.replace(",", "|") + "," + Pout.replace(",", "").replace("円","") + "," + TiOut + "," + BdOut + "," + IdOut + "," + Lout + "\n")
  
  page += 100

# Reinitialize page
page = 1

#PARSE BUY IT NOW SECOND

while page < functbmax:
 
  pagestr=str(page)
  URL = "https://auctions.yahoo.co.jp/search/search?p=" + SEARCH + "&va="+SEARCH+"&fixed=3&exflg=0&b=" + pagestr + "&n=100"
  r=requests.get(URL)
  soup = BeautifulSoup(r.content, 'html5lib')
  products = soup.find_all("li",{"class":"Product"})
  titles = soup.find_all("a",{"class":"Product__titleLink"})

  translator = Translator()

  for entry in products:
    if page >= functbmax-100  and functbmax % 100 != 0:
      break
    #hunt price
    price = entry.find_all("span", {"class":"Product__priceValue u-textRed"})
    pricec = price[0]

    #hunt price
    bprice = entry.find_all("span", {"class":"Product__priceValue"})
    bpricec = bprice[0]
    
    #hunt title
    title = entry.find_all("a", {"class":"Product__titleLink"})
    titlec = title[0]

    #Prep for output
    Pout = pricec.text
    Tout = titlec["title"]  
    Lout = titlec["href"]
    IdOut = Lout.replace("https://page.auctions.yahoo.co.jp/jp/auction/","") #Auction ID Output Only
    
    if TFlag == 1:
    #Translate Titles
      EnOut = translator.translate(Tout, src='ja')
      EnOutStr = str(EnOut)
      EnOutStripped = EnOutStr.replace("Translated(src=ja, dest=en, text=","").replace(", pronunciation=None, extra_data=","").replace('"',"").replace("{'translat...)","").replace("Jippuappupaka","")

    # print outputs
    print(Tout)
    if TFlag == 1:
      print(EnOutStripped)
    print("Buy it Now Price in Yen " + pricec.text)
    print(Lout)
    print(page)
    
    
    print("\n")
    
    if TFlag == 1:
      f.write(Tout.replace(",", "|") + "," + EnOutStripped + "," + Pout.replace(",", "").replace("円","") + "," + IdOut + "," + Lout + "\n")
    else:
      f.write(Tout.replace(",", "|") + "," + Pout.replace(",", "").replace("円","") + "," + "Buy It Now" + "," + "Buy It Now" + "," + IdOut + "," + Lout + "\n")
  page += 100

f.close()
print("Parse Complete JOCK will now lift Heavy Rocks")