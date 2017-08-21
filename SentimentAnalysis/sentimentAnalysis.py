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

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "")
    text = re_sub(r"/"," / ")
    text = re_sub(r"@\w+", "")
    text = re_sub(r"#\S+", hashtag)

    #text = re_sub(r"([!?.]){2,}", r"\1 <repeat>")
    #text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 <elong>")

    ## -- I just don't understand why the Ruby script adds <allcaps> to everything so I limited the selection.
    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", allcaps)
    #text = re_sub(r"([A-Z]){2,}", allcaps)

    return text.lower()

ID_INDEX = 0
TWEET_INDEX = 2

def updateSentiment(dbLoc, tableName):
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

def getSentiment(tweet):
    tweet = cleanTweet(tweet)
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
        
    return sent

# Update the sentiment
"""
TESTING CLEANER
"""
"""
tweets = []
tweets.append("RT @KirkKus: Indirect cost of the UK being in the EU is estimated to be costing Britain £170 billion per year! #BetterOffOut #UKIP")
tweets.append("VIDEO: Sturgeon on post-election deals http://t.co/BTJwrpbmOY")
tweets.append("RT @LabourEoin: The economy was growing 3 times faster on the day David Cameron became Prime Minister than it is today.. #BBCqt http://t.co…")
tweets.append("RT @GregLauder: the UKIP east lothian candidate looks about 16 and still has an msn addy http://t.co/7eIU0c5Fm1")
tweets.append("RT @thesundaypeople: UKIP's housing spokesman rakes in £800k in housing benefit from migrants.  http://t.co/GVwb9Rcb4w http://t.co/c1AZxcLh…")
tweets.append("RT @Nigel_Farage: Make sure you tune in to #AskNigelFarage tonight on BBC 1 at 22:50! #UKIP http://t.co/ogHSc2Rsr2")
tweets.append("RT @joannetallis: Ed Milliband is an embarrassment. Would you want him representing the UK?!  #bbcqt vote @Conservatives")
tweets.append("RT @abstex: The FT is backing the Tories. On an unrelated note, here's a photo of FT leader writer Jonathan Ford (next to Boris) http://t.c…")
tweets.append("RT @NivenJ1: “@George_Osborne: Ed Miliband proved tonight why he's not up to the job” Tbf you've spent 5 years doing that you salivating do…")
tweets.append("LOLZ to Trickle Down Wealth. It's never trickling past their own wallets. Greed always wins $$$ for the greedy.  https://t.co/X7deoPbS97")
tweets.append("SNP leader faces audience questions http://t.co/TYClKltSpW")
tweets.append("RT @cononeilluk: Cameron 'Ed Milliband hanging out with Russell Brand. He is a joke. This is an election. This is about real people' http:/…")
tweets.append("RT @politicshome: Ed Miliband: Last Labour government did not overspend http://t.co/W9RJ2aSH6o http://t.co/4myFekg5ex")
tweets.append("If Miliband is refusing to do any deal with the SNP, how does he plan on forming a government?")
tweets.append("RT @scotnotbritt: Well thats it. LABOUR would rather have a TORY government rather than work with the SNP. http://t.co/SNMkRDCe9f")

for tweet in tweets:
    print("Old tweet: %s" % tweet)
    print("Cleaned tweet: %s\n" % cleanTweet(tweet))
"""
