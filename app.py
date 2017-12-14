from flask import Flask, render_template, request

from datetime import datetime
import time
import json
import sqlite3

# Imports for Web Sockets
from threading import Lock
from flask_socketio import SocketIO, emit 

# Local Imports
import settings
from streaming import TwitterStream, Credentials, CredentialsManager


test_arr = []

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

thread = None
thread_lock = Lock()
twitter_stream = TwitterStream(socketio)


@app.cli.command()
def configure():
    path = settings.CREDENTIALS_PATH
    manager = CredentialsManager(path)

    if path.exists():
        cred = manager.read()
    else:
        cred = Credentials()

    user_input = lambda msg: input(msg).strip()
    promptify  = lambda text: text.replace('_', ' ').title()

    for key in cred:
        val = user_input(promptify(key) + ' [' + cred[key] + ']: ')
        cred[key] = val

    manager.write(cred)


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
        posData = []
        negData = []
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
@app.route('/streaming', methods=['POST','GET'])
def stream():
    return render_template("streaming.html", async_mode=socketio.async_mode)


def background_thread(message):
    print("Stream is flowing...")
    twitter_stream.flow(message)


@socketio.on('stop_stream', namespace='/streaming')
def stop_stream():
    print("Stream flow is ending...")
    twitter_stream.end_flow()


@socketio.on('start_stream', namespace='/streaming')
def start_stream(message):
    global thread

    with thread_lock:
        if thread is None:
            print("Starting thread")
            thread = socketio.start_background_task(background_thread, message)


if __name__ == "__main__":
    print("Running server...")
    socketio.run(app, debug=True)
