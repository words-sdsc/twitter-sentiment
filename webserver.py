from flask import Flask, render_template
from flask import request

import time
import json

import sqlite3

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    conn = sqlite3.connect('sql/TweetInfo.db')

    cursor = conn.execute("SELECT * from Test_run")
    tweetsList = []
    for row in cursor:
        tweetsList.append(row[3])
    return render_template("results.html", tweetsList=tweetsList)
    

