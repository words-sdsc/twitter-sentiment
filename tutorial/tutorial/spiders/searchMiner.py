import scrapy
from selenium import webdriver

class QuotesSpider(scrapy.Spider):
    name = "twitter"

    # Initialize to front as a Firefox() browser; selenium
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
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

        self.driver.find_element_by_link_text("All").click()
        for i in range( 1, 100 ):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)


        # Must use //text() to indicate grabbing all text from all children as well
        tweetTextsList = response.xpath('//div[@class="js-tweet-text-container"]//text()').extract()

        # Convert to string and then split into list based on new lines
        tweetText = ''.join(tweetTextsList)
        tweetTextsList = tweetText.split('\n')

        # Write each tweet to text file
        count = 0
        thefile = open("Words.txt", 'w')
        for tweet in tweetTextsList:
            print( str(count) + ': ' + tweet ) 
            # Ignore empty tweets
            if tweet != "":
                thefile.write("%s\n" % tweet )
            count += 1

        # Write entire html to File
        filename = "twitterSearchContent.html"
        with open(filename, 'wb') as f:
            f.write(response.body)

        print("\n\n")
        #print("DONE PRINTING THINGS FOUND")
        #print("------------------------")

        self.log('Saved file %s' % filename)

