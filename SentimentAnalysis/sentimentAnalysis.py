#from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
#from SentimentAnalysis.cleanTweets import *
import sqlite3

def cleanTweet( tweet ):
    return tokenize1(tweet).replace("don't", "do not")

import sys
import re

FLAGS = re.MULTILINE | re.DOTALL

def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = "<hashtag> {} <allcaps>".format(hashtag_body)
    else:
        result = " ".join(["<hashtag>"] + re.split("r(?=[A-Z])", hashtag_body, flags=FLAGS))
    return result

def allcaps(text):
    text = text.group()
    return text.lower() + " <allcaps>"


def tokenize1(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "<url>")
    text = re_sub(r"/"," / ")
    text = re_sub(r"@\w+", "<user>")
    text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), "<smile>")
    text = re_sub(r"{}{}p+".format(eyes, nose), "<lolface>")
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), "<sadface>")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "<neutralface>")
    text = re_sub(r"<3","<heart>")
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "<number>")
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 <elong>")

    ## -- I just don't understand why the Ruby script adds <allcaps> to everything so I limited the selection.
    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", allcaps)
    text = re_sub(r"([A-Z]){2,}", allcaps)

    return text.lower()

ID_INDEX = 0
TWEET_INDEX = 2

def updateSentiment( dbLoc, tableName):
    sid = SentimentIntensityAnalyzer()
    conn = sqlite3.connect(dbLoc)

    cursor = conn.execute("SELECT * from %s" % tableName)

    # Go through every sentence
    for row in cursor:
        text = cleanTweet(row[TWEET_INDEX])
        #blob = TextBlob(text)

        sent = 0.0
        count = 0
        sentList = tokenize.sent_tokenize(text)

        # Go through each sentence in tweet
        for sentence in sentList:
            count += 1
            ss = sid.polarity_scores(sentence)
            sent += ss['compound']  # Tally up the overall sentiment

        if count != 0:
            sent = float(sent / count)

        # Update into DB
        conn.execute("UPDATE " + tableName + " set SENTIMENT = ? where ID = ?", \
                (sent, row[ID_INDEX]))


    conn.commit()
    conn.close()

# Update the sentiment
