import scrapy

# Get selectors and extract html
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

# Selenium imports and time imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re

# Import Beautiful soup
from bs4 import BeautifulSoup

TARGET_URL = 'https://twitter.com/search?q=%23cocos%20fire&src=typd'

# Storage locations for tweets
tweetFile = "../../../Tweets.txt"
dateTweetFile = "../../../DateAndTweets.txt"

class QuotesSpider(scrapy.Spider):
    name = "twitter"    # Unique name for Scrapy to identify this crawler

    # Initialize to front as a Firefox() browser; selenium
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://twitter.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    # Begin making requests from select URLS
    def start_requests(self):
        # urls(keyword) 
        urls = [
            #'https://twitter.com/search?q=%23cocos%20fire&src=typd',
            'https://twitter.com/search?q=%23WhittierFire&src=tyah',
        ]

        # Make a request for each url to be parsed below
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Method called after each scrapy request
    def parse(self, response):
        # Get the URL
        #self.driver.get('https://twitter.com/search?q=%23cocos%20fire&src=typd')
        self.driver.get('https://twitter.com/search?q=%23WhittierFire&src=tyah')

        # TODO Have loop invariant be when the for loop hits the bottom
        # Scroll down the webpage via Selenium (infinite scrolling)
        for i in range(1,5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.5)
        
        # Get the raw HTML source after scrolling via selenium
        raw_html = self.driver.page_source

        # Use beautiful soup to extract ALL the innerHTML for each tweet
        soup = BeautifulSoup(raw_html, 'html.parser')
        tweetTextsList = soup.find_all("div", {"class":"js-tweet-text-container"})
        tweetDateList = soup.find_all("span", {"class":"_timestamp js-short-timestamp "})

        # Grabs all tags containing the attribute 'data-tweet-id', the True value means any
        tweetIdTagList = soup.find_all(attrs={'data-tweet-id' : True}) 

        # Create list of tweet ids
        tweetIdList = []
        for tweetId in tweetIdTagList:
            tweetIdList.append(tweetId['data-tweet-id'])
        
        print( tweetIdList )

        # Write each tweet to text file
        thefile = open(tweetFile, 'w')
        for tweet in tweetTextsList:
            # Grab tweet text
            tweetText = ''.join(tweet.findAll(text=True))

            # Ignore empty tweets
            if tweetText != "":
                thefile.write("%s\n" % tweetText )
                
        # Write file with both date and tweet
        thefile = open(dateTweetFile, 'w')
        for tweet, date, tweetId in zip(tweetTextsList, tweetDateList, tweetIdList):
            # Grab date/tweet text
            tweetText = ''.join(tweet.findAll(text=True))
            date = ''.join(date.findAll(text=True))
            tweetId = str(tweetId)

            # Ignore empty tweets
            if tweetText != "":
                thefile.write("Date: %s\nTweet ID: %s%s\n" % (date, tweetId, tweetText))

        # Write down db info
        

        # Quit the browser after completion
        self.driver.close() 
