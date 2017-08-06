# Description:
This program takes a user's twitter search query where it then scrapes tweets up to a certain
point. It is then ungoes sentiment analysis and is aggregated into an sqLite database. These tweets
are then displayed on a python webserver where the sentiment over time is displayed.

# How to Run Project:
## Running the program driver
    python3 main.py

## Running the webserver
    python3 webserver.py

## How to Run Web Crawler Directly:
In order to deploy the scrapy crawler directly... first cd into scrapy project "TwitterScraper/"
directory and type:
    
    scrapy crawl twitter
