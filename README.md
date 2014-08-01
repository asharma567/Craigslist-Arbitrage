Craiglist Arbitrage
------------------
Capstone project - Zipfian Academy
[ArbCraig.com](https://www.arbcraig.com)

Basic idea: finding arbitrage opportunities on Craigslist at the snap of your fingers. Good deals go fast, so should you.

#Proof-of-concept

ArbCraig is website app which grabs all the Craigslist Macbook Air 13" postings in the New York City Area and automatically shows you the best deals. Deals so good they could be sold for a profit on eBay. It knows how much each Macbook should be priced, based on the model year and other features. Macbooks which are priced abnormally low and undervalued given their specs are shown on a google map, so that one could have perspective of how much time and effort they'd have to put in to gain a profit.


eg:
	If there are two Macbooks that yield $30 in profit and one of them is 1.5 miles away vs 0.5 miles. Clearly the closer one is a better deal consider the amount effort(travel).

##Usage

#Installation

Clone git repo
> https://github.com/asharma567/Craigslist-Arbitrage.git

Run

> sudo python app.py
ArbCraig will be running at http://localhost:80

Scrape

> python scraper/periodic_scraper.py

* Please note the periodic_scraper is designed to run at whatever frequency preferred. Ideally you'd want to everyday.

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

