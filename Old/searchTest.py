import tweepy
from keys import *

keyword="lol"
numOfTweets=10

auth = tweepy.OAuthHandler(consumer_key(), consumer_secret())
auth.set_access_token(access_token(), access_token_secret())

api = tweepy.API(auth)

public_tweets = api.home_timeline()
"""
for tweet in public_tweets:
    print( tweet.text )
    print()
"""

print( "---- START PRINTING ----\n" )
# , geocode="33.1137,117.1599,30km"
count = 0
for tweet in tweepy.Cursor(api.search, q=keyword).items(numOfTweets):
    #print( tweet.text )
    #print( tweet.created_at )
    #print( type(tweet.coordinates) )
    #print()
    print( tweet.user.location )
print( "---- STOP  PRINTING ----" )
