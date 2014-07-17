def main():
    #call scraper and parser
    #Tristate Trian Data
	metro = 'USA-NYM'
	get_training_data(0,metro,False)
	get_training_data(1,metro,True)
	get_training_data(2,metro,True)
	#Reading the scraped and munged data from SQL
	NY_df = pd.read_sql_table('training' + metro + '_df', engine)

if '__name__' == '__main__':
    main()

    #send gio link to repo

