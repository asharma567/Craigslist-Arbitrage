#!/usr/bin/env python
from scraper import get_training_data, get_ebay_data


def main():
    '''
    Runs eBay and Craigslist scraper
    Auto scheduled to refresh listings once a day @ 11p
    '''
    metro = 'USA-NYM'
    
    #Get the latest postings past few hours
    get_training_data(0, metro, False)

    #Get the past week
    get_training_data(1, metro, True)
    
    #Get the past two or so weeks
    # get_training_data(2, metro, True)
    
    print 'Success! Craigslist'
    get_ebay_data()
    print 'Success! eBay'


if __name__ == '__main__':
    main()


