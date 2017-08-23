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

statusList = api.statuses_lookup([897208601319690240])
for status in statusList:
    if 'quoted_status' in status._json:
        print( "Retweet" )
    else:
        print( "Not retweet" )
    #print(status.retweeted_status)

statusList = api.statuses_lookup([766964808885284864])
for status in statusList:
    # ._json is actually just a dictionary
    ##print(json.dumps(status._json))
    if 'quoted_status' in status._json:
        print( "Retweet" )
    else:
        print( "Not retweet" )
    #print(status._json['retweeted_status')
