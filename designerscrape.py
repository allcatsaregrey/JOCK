#Christian Vartanian
#Batch Scraper Decently Unstable
import scrape
import database
import time
import random


database = database.jock_data_base()

start_time = time.time()

f = open("designers.txt", "r")
for SEARCH in f:  
    
    
    
    auctionmaxint, binmaxint = scrape.auction_search_(SEARCH)
    
    functamax, functbmax = scrape.set_funct_max(auctionmaxint, binmaxint)

    scrape.auction_only_parse(database, functamax, SEARCH)

    scrape.auction_bin_parse(database, functbmax, SEARCH)
    
    database.write_csv()
    
    elapsed_time = time.time() - start_time
    
    time.sleep(random.randint(10,100))
    
    print(elapsed_time)
    
    print("\n")
    
