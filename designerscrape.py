#Christian Vartanian
#Batch Scraper Decently Unstable
#Current Record: Ralph
#ConnectionError: HTTPSConnectionPool(host='auctions.yahoo.co.jp', port=443): Max retries exceeded with url: /search/search?p=Ralph%20Lauren%0A&va=Ralph%20Lauren%0A&fixed=2&exflg=0&b=7301&n=100&43.225.192.225:50878 (Caused by NewConnectionError('<urllib3.connection.VerifiedHTTPSConnection object at 0x121369650>: Failed to establish a new connection: [Errno 60] Operation timed out'))
import scrape
import database
import time
import random
import requests


proxies = [] 
    
scrape.get_free_proxies(proxies)
    
database = database.jock_data_base()

start_time = time.time()

f = open("designers2.txt", "r")
for SEARCH in f:  
    
    scrape.get_free_proxies(proxies)

    proxy = random.choice(proxies)
    
    scrape.session = requests.Session()
        
    scrape.get_session(proxies)
            
    auctionmaxint, binmaxint = scrape.auction_search_(SEARCH,proxy)
    
    functamax, functbmax = scrape.set_funct_max(auctionmaxint, binmaxint)

    scrape.auction_only_parse(database, functamax, SEARCH, proxy)

    scrape.auction_bin_parse(database, functbmax, SEARCH, proxy)
    
    elapsed_time = time.time() - start_time
    
    time.sleep(random.randint(10,30))
    
    print(elapsed_time)
    
    print("\n")
    
