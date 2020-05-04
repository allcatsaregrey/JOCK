# Author: Christian Vartanian
# Description: General Scraper tailored for Yahoo Japan Auction Search Results
# Current Feature Set: Price, Title, CSV Output
# TODO: Scrape more data into CSV, potentially perform google translate on titles.

import html5lib
import bs4 as bs
from bs4 import BeautifulSoup
import requests
SEARCH = "rickowens"
URL = "https://auctions.yahoo.co.jp/search/search?auccat=&tab_ex=commerce&ei=utf-8&aq=-1&oq=&sc_i=&exflg=1&p=" + SEARCH + "&x=0&y=0"
r=requests.get(URL)
filename = "JOCKReport.csv"
f = open(filename,"w")
headers = "Product_Name, Price in Yen \n"
f.write(headers)

soup = BeautifulSoup(r.content, 'html5lib')
products = soup.find_all("li",{"class":"Product"})
titles = soup.find_all("a",{"class":"Product__titleLink"})

for entry in products:

  #hunt price
  price = entry.find_all("span", {"class":"Product__priceValue u-textRed"})
  pricec = price[0]

  #hunt title
  title = entry.find_all("a",{"class":"Product__titleLink"})
  titlec = title[0]
  Tout = titlec["title"]
  Pout = pricec.text
  # print outputs
  print(titlec["title"])
  print("Price in Yen " + pricec.text)
  print("\n")
  
  f.write(Tout.replace(",", "|") + "," + Pout.replace(",", "").replace("円","") + "\n")

f.close()

