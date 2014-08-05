from scraper.periodic_scraper import scrape_craig_ebay
from utils_app import display_pipeline_arb
import cPickle

def full_routine(metro, rec_size):
    '''
    Run the routine Scrape -> Recommend -> clean deadlinks -> Pickle
    USE later by the app, saves time to do this as a scheduled task
    '''
    
    #Running periodic scraper to grab the data
    scrape_craig_ebay(metro)

    #Run pricing routine
    #NOTE - only return arbitrage opportunities currently
    df = display_pipeline_arb(metro, rec_size)
    
    #Pickle recs
    #NOTE - it continually overwrites any pre-existing pickle
    cPickle.dump(df, open('recs.pkl','wb')) 

if __name__ == '__main__':
    metro = 'USA-NYM'
    rec_size = 30
    full_routine(metro, rec_size)