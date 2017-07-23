import os
import sqlite3

import settings
from TwitterScraper.TwitterScraper.spiders.searchMiner import *
#from settings import *
# Main driver for the program

index = 0
searchQuery = ""
dbName = "sql/TweetInfo.db"
urlQuery = ""
tableName = ""


settings.init()

# 
# Helper methods
#
def urlify( string ):
    string.replace(" ", "%20")
    baseURL = "https://twitter.com/search?q="
    baseURL += string

    return baseURL

def tablify( string ):
    string.replace("\n","")
    string.replace(" ","_")
    return string.upper()

def getTableName():
    return tableName

def getUrlQuery():
    return settings.url

if __name__ == '__main__':
    #
    # Get user search query
    #
    while(True):
        searchQuery = input("What search query would you like to track?\n")
        confirm = input("Is this query: \"%s\" correct? (y/n): " % searchQuery)

        # Confirm user search query
        if confirm == "y" or confirm == "Y":
            settings.url = urlify( searchQuery )
            tableName = tablify( searchQuery ) 

            print("Table name is: %s" % tableName)
            confirm = input("Does this look correct? (y/n): ")
            
            # Confirm generated table name
            if confirm == "y" or confirm == "Y":
                break

    #
    # Create table inside DB 
    #

    conn = sqlite3.connect("sql/TweetInfo.db")

    print( tableName )
    conn = conn.cursor()
    try:
        # Create table
        conn.execute('''CREATE TABLE %s
                 (ID            INT PRIMARY KEY UNIQUE  NOT NULL,
                 DATE           INT                     NOT NULL,
                 TWEET          CHAR(250)               NOT NULL,
                 SENTIMENT      REAL);''' % tableName)

    except:
        print("Table: %s already exists in Database: %s" % (tableName, dbName) )  

    conn.close()

    print( "URL ISISISISIS: %s " % getUrlQuery() )
    #
    # Deploy scrapy crawler
    #
    #os.system(' cd TwitterScraper/TwitterScraper/spiders && scrapy crawl twitter')
    startCrawler()
