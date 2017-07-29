from flask import Flask, render_template
from datetime import datetime
from flask import request

import time
import json

import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    tableNamesList = conn.execute("select name from sqlite_master where type = 'table'")
    return render_template("index.html", tableNamesList=tableNamesList)

@app.route('/resultsTest', methods=['POST','GET'])
def resultsTest():
    

@app.route('/results', methods=['POST','GET'])
def results():
    conn = sqlite3.connect('sql/TweetInfo.db')

    cursor = conn.execute("SELECT * FROM _H_UNITEDAIRLINES")
    tweetsList = []
    index = 0
    for row in cursor:
        tweetsList.append([row[1], 100*row[3]])
        index += 1
    tweetsList.reverse()
    return render_template("results.html", tweetsList=tweetsList)

# Starts up the webserver
if __name__ == "__main__":
    app.run()
