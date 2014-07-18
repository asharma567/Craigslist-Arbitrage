from scraper import get_training_data


def main():
    #call scraper and parser
    #Tristate Trian Data
	metro = '*'
	print metro
	get_training_data(0,metro,False)
	#get_training_data(1,metro,True)
	#get_training_data(2,metro,True)
	#get_training_data(3,metro,True)
	#Reading the scraped and munged data from SQL
	NY_df = pd.read_sql_table('training' + metro + '_df', engine)

	#interesting -- seems like the subset of people that 
	# print NY_df[NY_df['negotiability'] == 'firm']['px'].mean()
	# print NY_df[NY_df['negotiability'] == 'obo']['px'].mean()

	#Craigslist is kinda like a thrift shop, I'd like to findout ideal key search words to limit time spent there
	#firm 
	#people tend to be selling mostly 2014.. wonder why?
	#df.year.hist()

	#notice prices are normally distributed
	#df['px'].hist()

if __name__ == '__main__':
    main()

    

