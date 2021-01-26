# DBbuilder 

Fetches a stocks lalance sheet data for a number of years specified using the Financial Modelling API and builds a database with the fetched information

Program helper methods will search for a stock when given the Ticker Symbol for that stock(ex: MSFT-microsoft, TD - Toronto Dominion Bank)

APi limits data for any individual stock to 5 years prior. A maximum of 250 calls may be made per day 

The API key i used has been removed and before running code you will need to recieve your own api key from

    https://financialmodelingprep.com/developer/docs/#Company-Financial-Statements
    
The API data is returned as a list of dictionaries and must be indexed as follows data[i]['key']
where I corresponds to years with the 0 index being the most recent year.

The helper methods work by creating sqlite3 query strings for CREATE and INSERT statements and then executing those statements 

Problems Encountered:
Balance sheet items are limited to the keys set by the API designers. 

Depending on the company sector and its domestic or foreign standing keys used in API may not match the line items used in balance sheets
by companies this will lead to zero entries for key financial items that are listed by a different name. 



