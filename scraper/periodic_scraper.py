from scraper import get_training_data, get_ebay_data
import datetime

def scrape_craig_ebay(metro):
    '''
    Runs eBay and Craigslist scraper
    Auto scheduled to refresh listings once a day @ 11p
    '''
    
    #Get the latest postings past few hours
    get_training_data(0, metro, False)

    #Get the past week
    get_training_data(1, metro, True)
    
    #Get the past two weeks
    # get_training_data(2, metro, True) 
    print 'Success! Craigslist'
    
    #Note - pulls pricing data for the feature set we've created
    #then pickles the output later used in Gridsearch
    get_ebay_data()
    print 'Success! eBay'
    print 'current time - ', datetime.datetime.now()


if __name__ == '__main__':
    metro = 'USA-NYM'
    scrape_craig_ebay(metro)


