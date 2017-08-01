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

        tweetsList = []
        index = 0
        for row in cursor:
            tweetsList.append([row[1]*1000, 100*row[3]])
            index += 1

        # Must sort becuase tweets can come out of order. FIXME Fix this at an earlier
        # part
        tweetsList.sort()
        #tweetsList.reverse()

        return render_template("results.html", tweetsList=tweetsList,\
                table_choice=table_choice[2:-3])
    except:
        return render_template("error.html")

# Starts up the webserver
if __name__ == "__main__":
    app.run()
