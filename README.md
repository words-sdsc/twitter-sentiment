# Description:
This program takes a user's twitter search query where it then scrapes tweets up to a certain
point. It is then ungoes sentiment analysis and is aggregated into an sqLite database. These tweets
are then displayed on a python webserver where the sentiment over time is displayed.

# How to Run Project:
## Running the program driver
    python3 main.py

## Running the webserver
1. Install project dependencies

    ```
    $ python3 setup.py install
    ```
2. Create a Twitter application (https://apps.twitter.com)
3. Get your API Key, API Secret, Access Token, and Access Token Secret
4. Configure your Twitter API keys on the Flask app

    ```
    $ export FLASK_APP=app.py
    $ flask configure
    ```
5. Run the Flask app
    ```
    $ python3 app.py
    ```
## How to Run Web Crawler Directly:
In order to deploy the scrapy crawler directly... first cd into scrapy project "TwitterScraper/"
directory and type:
    
    scrapy crawl twitter

# Built With
- Flask - Lightweight python Web framework library
- Selenium, Scrapy, BeautifulSoup - Used for scraping and parsing tweets)  
- Highcharts - Displaying sentiment over time
