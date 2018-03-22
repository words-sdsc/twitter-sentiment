import sqlite3
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
from random import randint



conn = sqlite3.connect('TweetInfo.db')

dbLoc = "TweetInfo.db"
tableName = "_H_OAKLANDHILLSFIRE_OR__H_GRIZZLYPEAKFIRE_OR__H_GRIZZLYPEAK_FIRE"
conn = sqlite3.connect(dbLoc)

# Update into DB
conn.execute("DROP TABLE " + tableName )

conn.commit()
conn.close()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
#conn.close()
