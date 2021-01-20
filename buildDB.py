try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import json
import sqlite3

conn = sqlite3.connect("FinancialModellingData.sqlite")
cur = conn.cursor()

#method to retrieve list of dictionary containing api data.
def get_jsonparsed_annual_data(ticker,years):
    numYears= years
    url ="https://financialmodelingprep.com/api/v3/balance-sheet-statement/"+ str(ticker.upper()) + "?limit="+ str(numYears) + "&apikey=f59b1e1e664a436b64c56f1acbca1725"
    response = urlopen(url)
    data = response.read().decode("utf-8")
    print('data retrieved from  ')
    print(url)
    #data=get_jsonParsed()
    return json.loads(data)                         #turning json into a list of dictionaries ;   data[0]["longTermDebt"]- index followed by key
#---------------------------------------------
# method used to change the 2000-01-11 format to 2000 
def dateToYear(year):
    ret = year[:4]
    return ret 
#----------------------
#creates and executes the query to make an annual Data Table for a given company organized by ticker symbol
def createQueryAnnual(data,ticker,years):
    quer='DROP TABLE IF EXISTS '+str(ticker.upper())+'AnnualData'
    cur.execute(quer)
    query= 'CREATE TABLE '+ str(ticker.upper())  + 'AnnualData(title Ticker, AccountName VARCHAR, '

    numYears = years
    i=numYears-1
    while i >= 0:
        if i == 0:
            query = query + '"' + dateToYear(str(data[i]['date'])) + '" VARCHAR)' 
        else:               
            query = query +'"'+ dateToYear(str(data[i]['date'])) + '" VARCHAR,'
        i= i-1
    cur.execute(query)
    print(query)
    print(" \n EXECUTED")
#------------------------------------------
def CreateInsertquery(ticker,years):
#    ["TotalAssets", "193468", "241086", "258848", "286556"],    
#creates the INSERT INTO query used to add data while preventing injection.    
    query = "INSERT INTO "+ str(ticker.upper())+ "AnnualData VALUES("
    i=0

    while i< years+2:          
        if i == years+1:
            query = query + "?)"
        else:
            query= query + "?,"
        i= i+1 

    print(query)
    return query
#--------------------------------------------------------------------------------
#return list of keys to pull data in createInsert()
def getList(dict): 
    return dict.keys() 
#- - - - - - - - - - - - - - - - - - - - - - - - - - 
def CreateInsert(data,ticker,years):
    data1 = data
    query= CreateInsertquery(ticker,years)
    rowlist= []
    keyrow= getList(data[0])
    kLen=len(keyrow) #39 3
    print(kLen)
    #adds Accounts as first item in row, append row to new row list
    for key in keyrow:
        row = []
        k=1
        row.append(str(ticker.upper()))
        row.append(key)      
        while k < years+1:     
            row.append(data1[years-(k+1)][key])             
            k=k+1
        
        rowlist.append(row)
    
    for row in rowlist:
        cur.execute(query, row)      #needs rows in proper format to take
#--------------------------------------------------------------------------------
def makeTable(ticker,years):
    

    data = get_jsonparsed_annual_data(ticker,years)             #get data from api                             
    createQueryAnnual(data,ticker,years)                       #execute create table query
    CreateInsert(data,ticker,years)                        #execute insert data statements
    
    conn.commit()
#--------------------------------------------------------------------------------

makeTable('MSFT',5)
