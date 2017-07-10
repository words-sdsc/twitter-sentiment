# Description:
This project will run a webcrawler onto twitter looking for a specific searchable term and 
scrape all the tweets with the given phrase. Then it will write each tweet to a file where
it is piped into Stanford's sentiment analysis server coreNLP to rate each sentence.

# How to Run Project:
## How to Run Web Crawler:
In order to deploy the scrapy crawler... first cd into scrapy project
folder and then type:
    
    scrapy crawl [name of crawler]


## How to Run NLP Server:
In order to run the stanford NLP server... first cd into the stanford
project fold and then type:
    
    cd stanford-corenlp-full-2016-10-31
    java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

#Misc
## What is geckodriver?
Gecko Driver is the link between your tests in Selenium and the Firefox browser. GeckoDriver is a proxy for using W3C WebDriver-compatible clients to interact with Gecko-based browsers i.e. Mozilla Firefox in this case. As Selenium 3 will not have any native implementation of FF, we have to direct all the driver commands through Gecko Driver. Gecko Driver is an executable file that you need to have in one of the system path before starting your tests.
