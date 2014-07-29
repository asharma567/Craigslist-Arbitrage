from scraper import get_training_data, get_postings


def main():
     
    #Tristate
    metro = 'USA-NYM'
    
    #call scraper and parser
    get_training_data(0, metro, False)
    get_training_data(1, metro, True)

if __name__ == '__main__':
    main()

    

