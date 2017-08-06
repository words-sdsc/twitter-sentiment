from flask import Flask, render_template
from datetime import datetime
from flask import request

import time
import json

import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('sql/TweetInfo.db')
    tableNamesList = conn.execute("select name from sqlite_master where type = 'table'")
    return render_template("index.html", tableNamesList=tableNamesList)

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
            #if(index < 20 and len(row) > 150): continue

            timeMS = row[1] * 1000      # Micro -> MiliSeconds
            sentiment = row[3] * 100   
            tweetId = row[0]
            tweetsList.append({ 'x': timeMS, 
                                'y' : sentiment, 
                                'tweetId' : tweetId,
                                'tweetText' : row[2]})


            #tweetsList.append([timeMS, sentiment])


        # Must sort becuase tweets can come out of order. FIXME Fix this at an earlier
        # part

        print(tweetsList)
        tweetsList = sorted(tweetsList, key=lambda k: k['x'])
        print(len(tweetsList))


        return render_template("results.html", tweetsList=tweetsList,\
                table_choice=table_choice[2:-3])
    except:
        return render_template("error.html")

# Starts up the webserver
if __name__ == "__main__":
    app.run()
