from flask import Flask, render_template
from datetime import datetime
from flask import request

import time
import json

import sqlite3

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    conn = sqlite3.connect('sql/TweetInfo.db')

    cursor = conn.execute("SELECT * FROM _H_UNITEDAIRLINES")
    tweetsList = []
    index = 0
    for row in cursor:
        tweetsList.append([row[1], 100*row[3]])
        index += 1
    tweetsList.reverse()
    tableNameList = conn.execute("SELECT * FROM sys.Tables")
    return render_template("results.html", tweetsList=tweetsList, \
            tableNamesList=TableNamesList)
