from scraper import get_training_data, get_ebay_data


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
    get_training_data(2, metro, True)
    
    print 'Success! Craigslist'
    get_ebay_data()
    print 'Success! eBay'


if __name__ == '__main__':
    metro = 'USA-NYM'
    scrape_craig_ebay(metro)


