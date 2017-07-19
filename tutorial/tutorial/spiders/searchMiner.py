# Scraping imports
import scrapy
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

# Local imports
from insertTweetInfo import insertTweetInfo

SPIDER_NAME = "twitter"

# Data base info
dbLocation = "../../../sql/TweetInfo.db"
dbName = "TWEET_INFO_LOL" 

class QuotesSpider(scrapy.Spider):
    name = SPIDER_NAME

    # Initialize to front as a Firefox() browser; selenium
    def __init__(self):
        """ Set up selenium driver """
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://twitter.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    # Begin making requests from select URLS
    def start_requests(self):
        urls = [
            'https://twitter.com/search?q=%23WhittierFire&src=tyah',
        ]

        # Make a request for each url to be parsed below
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Method called after each scrapy request
    def parse(self, response):
        # Load page for selenium
        self.driver.get(url)

        # Scroll down the webpage via Selenium (infinite scrolling)
        for i in range(1,20):
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
                

        # Write down db info
        for tweet, tweetId, unixTime in zip(tweetTextsList, tweetIdList, unixTimesList):
            tweet = ''.join(tweet.findAll(text=True))
            tweet = tweet.replace('\n', '')
            tweetId = str(tweetId)
            unixTime = str(unixTime)
            
            # Insert information to DB
            insertTweetInfo( dbName, dbLocation, tweetId, unixTime, tweet, -1 )
        
        self.driver.close() # Close web page
