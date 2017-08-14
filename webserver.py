from flask import Flask, render_template
from datetime import datetime
from flask import request

import time
import json

import sqlite3

app = Flask(__name__)

""" Default home page.

Allows user to choose a table to display or view a live stream of a 
pre-determiend query.

"""
@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('sql/TweetInfo.db')

    # Grab list of table names
    tableNamesList = conn.execute("select name from sqlite_master where type = "
                                    "'table'")

    return render_template("index.html", tableNamesList=tableNamesList)

""" Page with graphs of user-specified table.

Results page that shows graphs of a specified query. The page is generated based
on user table choice (POST requet). 

"""
@app.route('/results', methods=['POST','GET'])
def results():
    # Dispaly results
    try:
        # Connect to database
        conn = sqlite3.connect('sql/TweetInfo.db')

        # Get the chosen table
        table_choice = request.form.get('table_choice')

        # Select chosen table
        cursor = conn.execute("SELECT * FROM " + str(table_choice[2:-3]))

        # Format data for highCharts
        tweetsList = []
        index = -1
        for row in cursor:
            index += 1

            # Ignore the highlighted tweets
            if(index < 20 and len(row) > 150): continue

            timeMS = row[1] * 1000      # Micro -> MiliSeconds
            sentiment = row[3] * 100   
            tweetId = row[0]
            tweetsList.append({ 'x': timeMS, 
                                'y' : sentiment, 
                                'tweetId' : tweetId,
                                'tweetText' : row[2]
                             })

        # FIXME do this sorting later
        # Must sort, tweets can be scraped out of order. 
        tweetsList = sorted(tweetsList, key=lambda k: k['x'])


        return render_template("results.html", tweetsList=tweetsList,
                table_choice=table_choice[2:-3])
    except:
        return render_template("error.html")

""" Streaming page with live graph.

Displays a live graph of sentiment over time with a pre-determined selection of
search queries. (Typically updated with trending tweets)

"""
@app.route('/stream', methods=['POST','GET'])
def stream():
    print("Streaming!")

# Starts up the webserver
if __name__ == "__main__":
    app.run()
