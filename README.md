##Craiglist Arbitrage
------------------
Capstone project - Zipfian Academy
[ArbCraig.com](http://ArbCraig.com)

Basic idea: finding arbitrage opportunities on Craigslist at the snap of your finger. Good deals go fast, so should you.

#Web-app

ArbCraig is a web-app which grabs all the Craigslist Macbook Air 13" postings in the New York City Area and automatically shows you the best deals. Deals so good they could be sold for a profit on eBay. 

The algorithm knows how much each Macbook should be priced, based on the model year and other features. Macbooks which are priced abnormally low and undervalued given their specs are shown on a google map, so that one could have perspective of how much time and effort they'd be willing to put in.

The algorithm exploits the opportunity of the pricing opacity on Craigslist. People often don't have a sharp eye on what price to post for thier listing. They don't even know if it's competitve to other listings. This creates a perfect enviroment to profit of mispricings.


* eg
	* If there are two Macbooks that yield $30 in profit and one of them is 1.5 miles away vs 0.5 miles. Clearly the closer one is a better deal consider the amount effort(travel).

##Usage

#Installation

Clone git repo
> git clone https://github.com/asharma567/Craigslist-Arbitrage.git

Run

> sudo python app.py
ArbCraig will be running at http://localhost:80

Scrape

> sudo python main.py

main.py runs the full pricing recommendation routine:
Scrape -> price -> pickle recommendations

app.py opens the pickle and uses Google Maps API to plot latitude and longitude points

* Please note the main.py is designed to run at whatever frequency preferred. Ideally you'd want to everyday.

#Technologies

* Python packages:

	* NumPy
	* scikit
	* Pandas
	* Flask
	* SQL Alchemy
	* cPickle
	* Requests
	* Ast

* 3taps api: 3taps.com/developers-overview.php
* eBay scraper: API Providerhttp://www.bidvoy.net

* Front end:

	* Javascript
	* Jinja
	* HTML

