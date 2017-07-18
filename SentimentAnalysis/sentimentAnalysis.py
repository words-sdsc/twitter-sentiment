from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

from time import sleep
from cleanTweets import cleanTweets


import sqlite3

def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i)<128)

filename = "Tweets.txt"
myString = ""
stringArr = []
tweetId = []

TWEET_INDEX = 3
TWEET_ID_INDEX = 0

conn = sqlite3.connect('../sql/TweetInfo.db')

cursor = conn.execute("SELECT * from TWEET_INFO_2")

# Go through all tweets in DB
for row in cursor:

    # Get tweet
    thisString = row[ TWEET_INDEX ]

    # Tokenize strings
    thisString = cleanTweets(thisString)

    # Add to string batch

    tweetId.append(row[ TWEET_ID_INDEX ])
    
    stringArr.append(thisString)

index = 0

# Annotate the string using coreNLP
for string in stringArr:
    # Set up annotation 
    res = nlp.annotate(string,
                   properties={
                   'annotators': 'sentiment',
                   'outputFormat': 'json',
                   'timeout': 1000,
               })

    # Let nlp load
    sleep( .5 )

    # Print out the results!
    for s in res["sentences"]:
    # Prints( "Index: Words : Tokens : Sent Value : Sentiment (Pos/Neg/Neutral)" )
        print ( "%d: '%s': %s %s\n" % ( index, " ".join([t["word"] for t in s["tokens"]]),\
                s["sentimentValue"], s["sentiment"]) )
        
        # Connect to database

        str_ = "TWEET_INFO_2"

        # Insert a row of data
        conn.execute("UPDATE " + str_ + " set SENTIMENT = ? where ID = ?", \
                ( s["sentimentValue"] , tweetId[index] ))
        print( tweetId )
        

        index += 1

conn.commit()
conn.close()
