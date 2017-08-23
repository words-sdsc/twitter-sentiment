# Scraping imports
import scrapy
import sqlite3
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

from bs4 import BeautifulSoup

# General imports
import unittest, time, re
import sys

# Run scrapy from script
from scrapy.crawler import CrawlerProcess

# Import Global Variables
sys.path.append("../../..")
import settings
from main import *


SPIDER_NAME = "twitter"

# Data base info
dbLocation = "sql/TweetInfo.db"
dbTableName = getTableName()

def insertTweetInfo( dbName, dataBaseLoc, tweetId, epoch, tweet, sent ):
    """ Inserts pack of tweet information into the SQLite database. 
    
    Arguments:
        string  dbName: Name of the databse 
        string  dataBaseLoc: Path of the database (relative to location of 
                             method caller is being called)
        int     tweetId: Tweet ID code
        int     epoch: Unix timestamp
        string  tweet: Text of tweet
        int     sent: Sentiment score

    Return: None
    """
    # Connect to specified DB
    c = sqlite3.connect(dataBaseLoc)
    
    print("Inserting tweet info...")
    # Insert a row of data
    try:
        c.execute("INSERT INTO " + dbName + " (ID, DATE, TWEET, SENTIMENT) "
            "VALUES ( ?, ?, ?, ? )", ( (tweetId, epoch, tweet, sent) ))
        c.commit()   
    except:
        print("Error inserting into dataBase %s\nID for reference: %s" % dbName, tweetId)


""" Scrapy spider class """
class TwitterSpider(scrapy.Spider):
    name = SPIDER_NAME

    def __init__(self):
        """ Set up selenium driver """

        self.driver = webdriver.Firefox()       # Open firefox browser to see
        #self.driver = webdriver.PhantomJS()    # Run scraping headless (faster) but can't see

        self.driver.implicitly_wait(30)
        self.base_url = "https://twitter.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    # Begin making requests from select URLS
    def start_requests(self):
        """ Set up URL Requests to be parsed. Note: we don't really utilize this
            for its proper usage since we use global variables for the URLs 
            instead.
        
        Arguments: None

        Return: None
        """
        # URLs to scrape.
        urls = [
            'https://twitter.com'
        ]

        # Make a request for each url and call to be parsed after
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Method called after each scrapy request
    def parse(self, response):
        """ Parses the request made from a specified URL. 
        
            *Note, we don't use much of the tools Scrapy provides and use 
            selenium instead. E.g. instead of using response we use 
            driver.get(getUrlQuery()). Scrapy just laid out good structure, 
            and we needed selenium for more advanced page scraping.
        
        Arguments:
            response: This response refers to the response of the Request in
                      start_requests. This is the response from the specific
                      HTML request.

        Return: None
        """

        # Load page for selenium
        print( "Parsing url: \"%s\"" % getUrlQuery() )
        self.driver.get( getUrlQuery() )

        # Attempt to scrape page
        try:
            # Scroll down the webpage via Selenium (infinite scrolling page)
            for i in range(1,150):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(.5)
            
            # Get the raw HTML source after scrolling via selenium
            raw_html = self.driver.page_source

            # extract ALL the innerHTML for each tweet
            soup = BeautifulSoup(raw_html, 'html.parser')
            tweetTextsList = soup.find_all("div", {"class":"js-tweet-text-container"})
            tweetDateList = soup.find_all("span", {"class":"_timestamp js-short-timestamp "})

            # Grab ALL tag with attr 'data-tweet-id'
            tweetIdTagList = soup.find_all(attrs={'data-tweet-id' : True}) 

            # Create list of containing all tweet ids
            tweetIdList = []
            for tweetId in tweetIdTagList:
                tweetIdList.append(tweetId['data-tweet-id'])
            
            # Grab all the exact unix-format times
            unixTimesTagList = soup.find_all(attrs={'data-time' : True})
            
            # Add all unix times
            unixTimesList = []
            for timeStamp in unixTimesTagList:
                unixTimesList.append(timeStamp['data-time'])
            
            # All list sizes should be the same
            print( len(tweetTextsList) )
            print( len(tweetIdList) )
            print( len(unixTimesList) )

            # Write down db info
            for tweet, tweetId, unixTime in zip(tweetTextsList, tweetIdList, unixTimesList):
                tweet = ''.join(tweet.findAll(text=True))
                tweet = tweet.replace('\n', '')
                tweetId = str(tweetId)
                unixTime = str(unixTime)

                # Insert information to DB
                insertTweetInfo( getTableName(), dbLocation, tweetId, unixTime, tweet, -1 )
            
            # Finished successfully, close driver process
            Print("Scraping Successful")
            self.driver.close()

        except:
            # Failed to scrape, close driver process
            self.driver.close() 

def startCrawler():
    """ Initiates process of the web crawler above.
    
    Arguments: None

    Return: None
    """

    # Starts a Twisted reactors to configure logs and set shutdown handlers
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(TwitterSpider)
    process.start()
