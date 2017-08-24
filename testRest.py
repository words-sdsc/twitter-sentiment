# Twitter api
import tweepy

# Used for parsing
import json
import time
import datetime

# Parsing tweet dates specifically
import moment

# Auth keys
from keys import * 

import sqlite3

#Set up Twitter Authentication
auth = tweepy.OAuthHandler(consumer_key(), consumer_secret())
auth.set_access_token(access_token(), access_token_secret())

api = tweepy.API(auth)

""" Appends a list of tweets by given keyword and amount

    Args:
        listOfTweets: List containing tweets that will be added with tweets
            containing the keyword
        keyword: Search query to find tweets containing this word
        numOfTweets: Number of tweets to be added to the list

    Returns:
        A list of tweets containing the newly added tweets, where each element
        is a dictionary containing information about the specified tweet.
"""
def get_tweets(listOfTweets, keyword, numOfTweets):
    # Iterate through all tweets containing the given word, api search mode
    for tweet in tweepy.Cursor(api.search, q=keyword).items(numOfTweets):
        # Add tweets in this format
        dict_ = {'Screen Name': tweet.user.screen_name,
                'User Name': tweet.user.name,
                'Tweet Created At': unicode(tweet.created_at),
                'Tweet Text': tweet.text,
                'User Location': unicode(tweet.user.location),
                'Tweet Coordinates': unicode(tweet.coordinates),
                'Retweet Count': unicode(tweet.retweet_count),
                'Retweeted': unicode(tweet.retweeted),
                'Phone Type': unicode(tweet.source),
                'Favorite Count': unicode(tweet.favorite_count),
                'Favorited': unicode(tweet.favorited),
                'Replied': unicode(tweet.in_reply_to_status_id_str)
                }
        listOfTweets.append(dict_)   
    return listOfTweets

# Connect to DB
conn = sqlite3.connect('sql/TweetInfo.db')
tableName = "_H_CORGIS"

# Add new Column
conn.execute("ALTER TABLE " + tableName + " ADD COLUMN RETWEET INT")

# Get list of rows
cursor = conn.execute("SELECT * FROM " + tableName) 

index = 0
# Update each row
for row in cursor:
    statusList = api.statuses_lookup([row[0]])

    # Is a retweet
    if (len(statusList) > 0 ) and ('quoted_status' in statusList[0]._json):
        print( "Retweet" )
        # Update into DB
        conn.execute("UPDATE " + tableName + " set RETWEET = ? where ID = ?", \
                (1, row[0]))

    # Not a retweet
    else:
        print("Not Retweet")
        conn.execute("UPDATE " + tableName + " set RETWEET = ? where ID = ?", \
                (0, row[0]))
    print()

conn.commit()
conn.close()
