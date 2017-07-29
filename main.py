import os
import sqlite3

import settings
from TwitterScraper.TwitterScraper.spiders.searchMiner import *
from SentimentAnalysis.cleanTweets import *
from SentimentAnalysis.sentimentAnalysis import *

#from settings import *
# Main driver for the program

index = 0
dbLoc = "sql/TweetInfo.db"
urlQuery = ""

settings.init()

# 
# Helper methods
#
def urlify( string ):
    string = string.replace(" ", "%20")
    string = string.replace("#", "%23")
    baseURL = "https://twitter.com/search?q="
    baseURL += string

    return baseURL

def tablify( string ):
    string = string.replace("\n","")
    string = string.replace(" ","_")
    string = string.replace("#","_H_")
    return string.upper()

def getTableName():
    return settings.tableName
def getUrlQuery():
    return settings.url

if __name__ == "__main__":
    #
    # Get user search query
    #
    while(True):
        settings.searchQuery = input("What search query would you like to track?\n")
        confirm = input("Is this query: \"%s\" correct? (y/n): " % settings.searchQuery)

        # Confirm user search query
        if confirm == "y" or confirm == "Y":
            settings.url = urlify( settings.searchQuery )
            settings.tableName = tablify( settings.searchQuery ) 

            print("Table name is: %s" % settings.tableName)
            confirm = input("Does this look correct? (y/n): ")
            
            # Confirm generated table name
            if confirm == "y" or confirm == "Y":
                break

    #
    # Create table inside DB 
    #

    conn = sqlite3.connect("sql/TweetInfo.db")

    print( settings.tableName )
    conn = conn.cursor()
    try:
        # Create table
        conn.execute('''CREATE TABLE %s
                 (ID            INT PRIMARY KEY UNIQUE  NOT NULL,
                 DATE           INT                     NOT NULL,
                 TWEET          CHAR(250)               NOT NULL,
                 SENTIMENT      REAL);''' % settings.tableName)

    except:
        print("Table: %s already exists in Database: %s" % (settings.tableName, dbLoc) )  

    conn.close()

    # Deploy scrapy crawler
    startCrawler()

    # Update the sentiment
    updateSentiment(dbLoc, getTableName())
