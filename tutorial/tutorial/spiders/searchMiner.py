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

class QuotesSpider(scrapy.Spider):
    name = "twitter"

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
            'https://twitter.com/search?q=%23cocos%20fire&src=typd',
            #'https://twitter.com/',
            #'http://www.karlrummler.com',
        ]

        # Make a request for each url to be parsed below
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Method called after each scrapy request
    def parse(self, response):
        print("------------------------")
        print("INDICIATING IF TEXT WAS FOUND: \n\n")

        # Check if tag is found
        if response.xpath('//div[@class="js-tweet-text-container"]//text()').extract() is None:
            print("Text container not found")
        else:
            print("Text container is found")

        # Get the URL
        #self.driver.get(self.base_url + "/search?q=stckoverflow&src=typd")
        self.driver.get('https://twitter.com/search?q=%23cocos%20fire&src=typd')

        # Scroll down the URL via Selenium
        for i in range(1,5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.5)
        
        # Get teh raw HTML source after scrolling via selenium
        raw_html = self.driver.page_source

        # Convert raw html (string) to List via Selector (from Scrapy)
        tweetTextsList = Selector(text=raw_html).xpath('//div[@class="js-tweet-text-container"]//text()').extract()
        print("\n\n\n")
        print(tweetTextsList)
        print("\n\n\n")
        
        """
        # NOTE: This is the scrapy way, you can't execute a script through
        # Must use //text() to indicate grabbing all text from all children as well
        tweetTextsList = response.xpath('//div[@class="js-tweet-text-container"]//text()').extract()
        print( response )
        """

        # Convert to string and then split into list based on new lines
        tweetText = ''.join(tweetTextsList)
        tweetTextsList = tweetText.split('\n')

        # Write each tweet to text file
        count = 0
        thefile = open("Words.txt", 'w')
        for tweet in tweetTextsList:
            #print( str(count) + ': ' + tweet ) 
            # Ignore empty tweets
            if tweet != "":
                thefile.write("%s\n" % tweet )
            count += 1

        # Write entire html to File
        filename = "twitterSearchContent.html"
        with open(filename, 'wb') as f:
            f.write(response.body)

        print("\n\n")

        self.log('Saved file %s' % filename)

        self.driver.close() # Quit the browser after completion

