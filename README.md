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
