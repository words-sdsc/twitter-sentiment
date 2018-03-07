from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import sys, re, sqlite3

FLAGS = re.MULTILINE | re.DOTALL

def cleanTweet( tweet ):
    return tokenize1(tweet).replace("don't", "do not")

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
    sid = SentimentIntensityAnalyzer()
    tweet = cleanTweet(tweet)
    sent = 0.0
    count = 0
    sentList = tokenize.sent_tokenize(tweet)

    # Go through each sentence in tweet
    for sentence in sentList:
        count += 1
        ss = sid.polarity_scores(sentence)
        sent += ss['compound']  # Tally up the overall sentiment

    if count != 0:
        sent = float(sent / count)
        
    return sent
