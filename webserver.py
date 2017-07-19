from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    conn = sqlite3.connect('sql/TweetInfo.db')

    cursor = conn.execute("SELECT * from TWEET_INFO_LOL")
    dog = []
    for row in cursor:
        print( row[2] )
        dog.append(row[2])

    return str(dog)
    

