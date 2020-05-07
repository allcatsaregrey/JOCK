# Author: Christian Vartanian, Matthew Mcfee
# Description: General Scraper tailored for Yahoo Japan Auction Search Results
# Current Feature Set: Price, Title, Time Remaining, Current Bidders,
# Optional Translator, CSV Output
# TODO: Scrape more data into CSV, stabilize system past 15000 results
#       Generate a function parsing class and the buy out can inherit
#       the general parsers stuff.

# import html5lib
# import bs4 as bs
from bs4 import BeautifulSoup
import requests
# from googletrans import Translator
# import time
import database

# Translator Flag, will crash if turned on and running 10K+ results

TFlag = 0


def get_search_():

    SEARCH = input("Select a brand to search for: ")

    return SEARCH


SEARCH = input("Select a brand to search for: ")


def auction_search_():

    # PARSE AUCTIONS FIRST
    URL = "https://auctions.yahoo.co.jp/search/search?p=" + \
        SEARCH + "&va="+SEARCH+"&fixed=2&exflg=0&b=1&n=100"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    searchtab = soup.find_all("span", {"class": "Tab__subText"})
    auctionmax = searchtab[1]
    binmax = searchtab[2]
    binmaxint = int(binmax.text.replace("件", "").replace(",", ""))
    auctionmaxint = int(auctionmax.text.replace("件", "").replace(",", ""))
    print(auctionmaxint)
    print(binmaxint)


def set_funct_max(auctionmaxint, binmaxint):

    if auctionmaxint >= 15000:
        functamax = 15000
    else:
        functamax = auctionmaxint

    if binmaxint >= 15000:
        functbmax = 15000
    else:
        functbmax = binmaxint

    return functamax, functbmax


def auction_only_parse(database, functamax, SEARCH):

    # Initialize page shift index variable
    page = 1
    # Begin Auction Only Parse
    while page < functamax:
        pagestr = str(page)
        URL = "https://auctions.yahoo.co.jp/search/search?p=" + SEARCH + \
            "&va="+SEARCH+"&fixed=2&exflg=0&b=" + pagestr + "&n=100"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        products = soup.find_all("li", {"class": "Product"})
        # titles = soup.find_all("a", {"class": "Product__titleLink"})

        # translator = Translator()

        for entry in products:
            if page >= functamax-100 and functamax % 100 != 0:
                break

            # hunt price
            price = entry.find_all("span",
                                   {"class": "Product__priceValue u-textRed"})

            pricec = price[0]

            # hunt price
            # bprice = entry.find_all("span", {"class": "Product__priceValue"})
            # bpricec = bprice[0]

            # hunt title
            title = entry.find_all("a", {"class": "Product__titleLink"})
            titlec = title[0]

            # hunt time remaining
            # timel = entry.find_all("span", {"class": "Product__time"})
            # timec = timel[0]

            # hunt bidders
            # bids = entry.find_all("span", {"class": "Product__bid"})
            # bidc = bids[0]

            # Prep for output
            Pout = pricec.text
            Tout = titlec["title"]
            Lout = titlec["href"]
            IdOut = Lout.replace("https://page.auctions.yahoo.co.jp/jp/auction/",
                                 "")  # Auction ID Output Only

            database.add_(IdOut, Tout, Pout)

            page += 100


def auction_bin_parse(database, functbmax, SEARCH):
    # Reinitialize page
    page = 1

# PARSE BUY IT NOW SECOND

    while page < functbmax:

        pagestr = str(page)
        URL = "https://auctions.yahoo.co.jp/search/search?p=" + SEARCH + \
            "&va="+SEARCH+"&fixed=3&exflg=0&b=" + pagestr + "&n=100"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        products = soup.find_all("li", {"class": "Product"})
        # titles = soup.find_all("a", {"class": "Product__titleLink"})

        # translator = Translator()

        for entry in products:
            if page >= functbmax-100 and functbmax % 100 != 0:
                break
            # hunt price
            price = entry.find_all("span", {"class": "Product__priceValue u-textRed"})
            pricec = price[0]

            # hunt price
            # bprice = entry.find_all("span", {"class": "Product__priceValue"})
            # bpricec = bprice[0]

            # hunt title
            title = entry.find_all("a", {"class": "Product__titleLink"})
            titlec = title[0]

            # Prep for output
            Pout = pricec.text
            Tout = titlec["title"]
            Lout = titlec["href"]
            IdOut = Lout.replace("https://page.auctions.yahoo.co.jp/jp/auction/",
                                 "")  # Auction ID Output Only

            database.add_(IdOut, Tout, Pout)

            page += 100


if __name__ == "__main__":

    database = database.jock_data_base()

    SEARCH = get_search_()

    functamax, functbmax = set_funct_max()

    auction_only_parse(database, functamax, SEARCH)

    auction_bin_parse(database, functbmax, SEARCH)
